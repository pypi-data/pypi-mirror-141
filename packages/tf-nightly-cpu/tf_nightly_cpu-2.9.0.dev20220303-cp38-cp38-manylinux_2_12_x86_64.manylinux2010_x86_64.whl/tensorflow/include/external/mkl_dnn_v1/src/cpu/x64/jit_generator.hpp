/*******************************************************************************
* Copyright 2016-2021 Intel Corporation
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*******************************************************************************/

#ifndef CPU_X64_JIT_GENERATOR_HPP
#define CPU_X64_JIT_GENERATOR_HPP

#include <limits.h>

#include "common/bit_cast.hpp"
#include "common/compiler_workarounds.hpp"
#include "common/type_helpers.hpp"
#include "common/utils.hpp"

#include "cpu/x64/cpu_isa_traits.hpp"

#include "cpu/jit_utils/jit_utils.hpp"

#if defined(_WIN32) && !defined(__GNUC__)
#define STRUCT_ALIGN(al, ...) __declspec(align(al)) __VA_ARGS__
#else
#define STRUCT_ALIGN(al, ...) __VA_ARGS__ __attribute__((__aligned__(al)))
#endif

#if defined(_WIN32)
#define OFFSET_SHADOWSPACE 0x28
#endif

#if GCC_WA_NO_TREE_DOMINATOR_OPTS
#define ATTRIBUTE_OPTIMIZE __attribute__((optimize("no-tree-dominator-opts")))
#else
#define ATTRIBUTE_OPTIMIZE
#endif

#define DECLARE_CPU_JIT_AUX_FUNCTIONS(jit_name) \
    const char *name() const override { return STRINGIFY(jit_name); } \
    const char *source_file() const override { return __FILE__; }

namespace dnnl {
namespace impl {
namespace cpu {
namespace x64 {

// TODO: move this to jit_generator class?
namespace {

typedef enum {
    MAX_CODE_SIZE = 256 * 1024,
} max_code_size_t;

// TODO: move this somewhere else? Although this is only used by jit kernels
// (Roma)
static inline int float2int(float x) {
    return utils::bit_cast<int>(x);
}

static inline void tc_configure_tile(
        palette_config_t *tc, int t, int rows, int cols) {
    const bool rows_ok = (size_t)t < sizeof(tc->rows) / sizeof(tc->rows[0]);
    const bool cols_ok = (size_t)t < sizeof(tc->cols) / sizeof(tc->cols[0]);
    if (rows_ok && cols_ok) {
        tc->rows[t] = rows;
        tc->cols[t] = cols;
    } else {
        assert(!"out of range");
    }
}

// TODO: A GPR class that hides ABI details from the JIT kernels and allows
// numbering registers from 0 to 14 (x86_64) / 6 (x32) (gpr0, gpr1, ...) and
// stack register (sr).
//
// This will allow using syntax like this:
//
// param = gpr0;
// reg_input = gpr0;
// reg_output =  gpr1;
// ...
//
// #ifndef XBYAK64
// mov(param, ptr[sr])
// #endif
//
// (Roma)

#ifdef XBYAK64
constexpr Xbyak::Operand::Code abi_save_gpr_regs[] = {
        Xbyak::Operand::RBX,
        Xbyak::Operand::RBP,
        Xbyak::Operand::R12,
        Xbyak::Operand::R13,
        Xbyak::Operand::R14,
        Xbyak::Operand::R15,
#ifdef _WIN32
        Xbyak::Operand::RDI,
        Xbyak::Operand::RSI,
#endif
};

#ifdef _WIN32
static const Xbyak::Reg64 abi_param1(Xbyak::Operand::RCX),
        abi_param2(Xbyak::Operand::RDX), abi_param3(Xbyak::Operand::R8),
        abi_param4(Xbyak::Operand::R9), abi_not_param1(Xbyak::Operand::RDI);
#else
static const Xbyak::Reg64 abi_param1(Xbyak::Operand::RDI),
        abi_param2(Xbyak::Operand::RSI), abi_param3(Xbyak::Operand::RDX),
        abi_param4(Xbyak::Operand::RCX), abi_param5(Xbyak::Operand::R8),
        abi_param6(Xbyak::Operand::R9), abi_not_param1(Xbyak::Operand::RCX);
#endif
#endif

} // namespace

class jit_generator : public Xbyak::CodeGenerator, public c_compatible {
public:
    using c_compatible::operator new;
    using c_compatible::operator new[];
    using c_compatible::operator delete;
    using c_compatible::operator delete[];

private:
    const size_t xmm_len = 16;
#ifdef _WIN32
    const size_t xmm_to_preserve_start = 6;
    const size_t xmm_to_preserve = 10;
#else
    const size_t xmm_to_preserve_start = 0;
    const size_t xmm_to_preserve = 0;
#endif

    const size_t num_abi_save_gpr_regs
            = sizeof(abi_save_gpr_regs) / sizeof(abi_save_gpr_regs[0]);

    const size_t size_of_abi_save_regs
            = num_abi_save_gpr_regs * rax.getBit() / 8
            + xmm_to_preserve * xmm_len;

public:
    enum {
        _cmp_eq_oq = 0u,
        _cmp_lt_os = 1u,
        _cmp_le_os = 2u,
        _cmp_neq_uq = 4u,
        _cmp_nlt_us = 5u,
        _cmp_nle_us = 6u,

        _op_floor = 1u,
        _op_mxcsr = 4u,
    };

    Xbyak::Reg64 param1 = abi_param1;
    const int EVEX_max_8b_offt = 0x200;
    const Xbyak::Reg64 reg_EVEX_max_8b_offt = rbp;

    inline size_t get_size_of_abi_save_regs() { return size_of_abi_save_regs; }

    void preamble() {
        if (xmm_to_preserve) {
            sub(rsp, xmm_to_preserve * xmm_len);
            for (size_t i = 0; i < xmm_to_preserve; ++i)
                uni_vmovdqu(ptr[rsp + i * xmm_len],
                        Xbyak::Xmm(xmm_to_preserve_start + i));
        }
        for (size_t i = 0; i < num_abi_save_gpr_regs; ++i)
            push(Xbyak::Reg64(abi_save_gpr_regs[i]));
        if (is_valid_isa(avx512_common)) {
            mov(reg_EVEX_max_8b_offt, 2 * EVEX_max_8b_offt);
        }
    }

    // This function returns the address on the stack of the fist argument
    // that is not passed by register
    // By default it assumes to be called after the prologue
    // Note: that we cannot use RBP inside as we override it in preamble
    // for address computation in EVEX instructions
    inline const Xbyak::RegExp get_stack_params_address(
            bool after_prolog = true) {
        int saved_regs_size = after_prolog ? get_size_of_abi_save_regs() : 0;
#ifdef _WIN32
        // Using stack layout described in MS ABI
        // (https://docs.microsoft.com/en-us/cpp/build/stack-usage?view=vs-2019)
        // here, the return address and the first 4 parameters are allocated
        // on the stack
        int first_params_and_return_addr_size = 40;
#else
        // In System V ABI, only the return address is stacked
        // before the arguments
        int first_params_and_return_addr_size = 8;
#endif
        return rsp + saved_regs_size + first_params_and_return_addr_size;
    }

    void mic_prefetcht0(Xbyak::Address a) {
        if (is_valid_isa(avx512_mic)) prefetcht0(a);
    }

    void mic_prefetcht1(Xbyak::Address a) {
        if (is_valid_isa(avx512_mic)) prefetcht1(a);
    }

    void mic_prefetcht2(Xbyak::Address a) {
        if (is_valid_isa(avx512_mic)) prefetcht2(a);
    }

    void uni_vzeroupper() {
        if (mayiuse(avx) && !mayiuse(avx512_mic)) vzeroupper();
    }

    void postamble() {
        for (size_t i = 0; i < num_abi_save_gpr_regs; ++i)
            pop(Xbyak::Reg64(abi_save_gpr_regs[num_abi_save_gpr_regs - 1 - i]));
        if (xmm_to_preserve) {
            for (size_t i = 0; i < xmm_to_preserve; ++i)
                uni_vmovdqu(Xbyak::Xmm(xmm_to_preserve_start + i),
                        ptr[rsp + i * xmm_len]);
            add(rsp, xmm_to_preserve * xmm_len);
        }
        uni_vzeroupper();
        ret();
    }

    template <typename T>
    Xbyak::Address EVEX_compress_addr(
            Xbyak::Reg64 base, T raw_offt, bool bcast = false) {
        using Xbyak::Address;
        using Xbyak::Reg64;
        using Xbyak::RegExp;
        using Xbyak::Zmm;

        assert(raw_offt <= INT_MAX);
        auto offt = static_cast<int>(raw_offt);

        int scale = 0;

        if (EVEX_max_8b_offt <= offt && offt < 3 * EVEX_max_8b_offt) {
            offt = offt - 2 * EVEX_max_8b_offt;
            scale = 1;
        } else if (3 * EVEX_max_8b_offt <= offt
                && offt < 5 * EVEX_max_8b_offt) {
            offt = offt - 4 * EVEX_max_8b_offt;
            scale = 2;
        }

        auto re = RegExp() + base + offt;
        if (scale) re = re + reg_EVEX_max_8b_offt * scale;

        if (bcast)
            return zword_b[re];
        else
            return zword[re];
    }

    Xbyak::Address make_safe_addr(const Xbyak::Reg64 &reg_out, size_t offt,
            const Xbyak::Reg64 &tmp_reg, bool bcast = false) {
        if (offt > INT_MAX) {
            mov(tmp_reg, offt);
            return bcast ? ptr_b[reg_out + tmp_reg] : ptr[reg_out + tmp_reg];
        } else {
            return bcast ? ptr_b[reg_out + offt] : ptr[reg_out + offt];
        }
    }

    Xbyak::Address EVEX_compress_addr_safe(const Xbyak::Reg64 &base,
            size_t raw_offt, const Xbyak::Reg64 &reg_offt, bool bcast = false) {
        if (raw_offt > INT_MAX) {
            return make_safe_addr(base, raw_offt, reg_offt, bcast);
        } else {
            return EVEX_compress_addr(base, raw_offt, bcast);
        }
    }

    void safe_add(const Xbyak::Reg64 &base, size_t raw_offt,
            const Xbyak::Reg64 &reg_offt) {
        if (raw_offt > INT_MAX) {
            mov(reg_offt, raw_offt);
            add(base, reg_offt);
        } else {
            add(base, raw_offt);
        }
    }

    void safe_sub(const Xbyak::Reg64 &base, size_t raw_offt,
            const Xbyak::Reg64 &reg_offt) {
        if (raw_offt > INT_MAX) {
            mov(reg_offt, raw_offt);
            sub(base, reg_offt);
        } else {
            sub(base, raw_offt);
        }
    }

    // Disallow char-based labels completely
    void L(const char *label) = delete;
    void L(Xbyak::Label &label) { Xbyak::CodeGenerator::L(label); }

    void L_aligned(Xbyak::Label &label, int alignment = 16) {
        align(alignment);
        L(label);
    }

    void uni_vpxor(const Xbyak::Xmm &x1, const Xbyak::Xmm &x2,
            const Xbyak::Operand &op) {
        if (is_valid_isa(avx512_core))
            vpxord(x1, x2, op);
        else if (is_valid_isa(avx))
            vpxor(x1, x2, op);
        else {
            assert(x1.isEqualIfNotInherited(x2));
            pxor(x2, op);
        }
    }
    void uni_vpxor(const Xbyak::Ymm &x1, const Xbyak::Ymm &x2,
            const Xbyak::Operand &op) {
        if (is_valid_isa(avx512_core))
            vpxord(x1, x2, op);
        else if (is_valid_isa(avx2))
            vpxor(x1, x2, op);
        else
            vxorps(x1, x2, op);
    }
    void uni_vpxor(const Xbyak::Zmm &x1, const Xbyak::Zmm &x2,
            const Xbyak::Operand &op) {
        vpxord(x1, x2, op);
    }

    void uni_vmovss(const Xbyak::Address &addr, const Xbyak::Xmm &x) {
        if (is_valid_isa(avx))
            vmovss(addr, x);
        else
            movss(addr, x);
    }
    void uni_vmovss(const Xbyak::Xmm &x, const Xbyak::Address &addr) {
        if (is_valid_isa(avx))
            vmovss(x, addr);
        else
            movss(x, addr);
    }
    void uni_vmovss(const Xbyak::Xmm &x1, const Xbyak::Xmm &x2) {
        if (is_valid_isa(avx))
            vmovss(x1, x1, x2);
        else
            movss(x1, x2);
    }
    void uni_vmovss(const Xbyak::Address &addr, const Xbyak::Ymm &x) {
        vmovss(addr, Xbyak::Xmm(x.getIdx()));
    }
    void uni_vmovss(const Xbyak::Ymm &x, const Xbyak::Address &addr) {
        vmovss(Xbyak::Xmm(x.getIdx()), addr);
    }
    void uni_vmovss(const Xbyak::Ymm &x1, const Xbyak::Ymm &x2) {
        vmovss(Xbyak::Xmm(x1.getIdx()), Xbyak::Xmm(x2.getIdx()));
    }

    void uni_vmovsd(const Xbyak::Address &addr, const Xbyak::Xmm &x) {
        if (is_valid_isa(avx))
            vmovsd(addr, x);
        else
            movsd(addr, x);
    }
    void uni_vmovsd(const Xbyak::Address &addr, const Xbyak::Ymm &x) {
        vmovsd(addr, x);
    }
    void uni_vmovsd(const Xbyak::Xmm &x, const Xbyak::Address &addr) {
        if (is_valid_isa(avx))
            vmovsd(x, addr);
        else
            movsd(x, addr);
    }
    void uni_vmovsd(const Xbyak::Ymm &x, const Xbyak::Address &addr) {
        vmovsd(x, addr);
    }

    void uni_vmovlps(const Xbyak::Address &addr, const Xbyak::Xmm &x) {
        if (is_valid_isa(avx))
            vmovlps(addr, x);
        else
            movlps(addr, x);
    }
    void uni_vmovlps(const Xbyak::Address &addr, const Xbyak::Ymm &x) {
        vmovlps(addr, x);
    }
    void uni_vmovlps(const Xbyak::Xmm &x, const Xbyak::Address &addr) {
        if (is_valid_isa(avx))
            vmovlps(x, addr);
        else
            movlps(x, addr);
    }
    void uni_vmovlps(const Xbyak::Ymm &x, const Xbyak::Address &addr) {
        vmovlps(x, addr);
    }

    void uni_vmovdqu(const Xbyak::Address &addr, const Xbyak::Xmm &x) {
        if (is_valid_isa(avx))
            vmovdqu(addr, x);
        else
            movdqu(addr, x);
    }
    void uni_vmovdqu(const Xbyak::Address &addr, const Xbyak::Ymm &x) {
        vmovdqu(addr, x);
    }
    void uni_vmovdqu(const Xbyak::Address &addr, const Xbyak::Zmm &x) {
        vmovdqu32(addr, x);
    }

    void uni_vmovdqu(const Xbyak::Xmm &x, const Xbyak::Address &addr) {
        if (is_valid_isa(avx))
            vmovdqu(x, addr);
        else
            movdqu(x, addr);
    }
    void uni_vmovdqu(const Xbyak::Ymm &x, const Xbyak::Address &addr) {
        vmovdqu(x, addr);
    }
    void uni_vmovdqu(const Xbyak::Zmm &x, const Xbyak::Address &addr) {
        vmovdqu32(x, addr);
    }

    void uni_vmovups(const Xbyak::Address &addr, const Xbyak::Xmm &x) {
        if (is_valid_isa(avx))
            vmovups(addr, x);
        else
            movups(addr, x);
    }
    void uni_vmovups(const Xbyak::Address &addr, const Xbyak::Ymm &x) {
        vmovups(addr, x);
    }

    void uni_vmovups(const Xbyak::Xmm &x, const Xbyak::Operand &op) {
        if (is_valid_isa(avx))
            vmovups(x, op);
        else
            movups(x, op);
    }
    void uni_vmovups(const Xbyak::Ymm &x, const Xbyak::Operand &op) {
        vmovups(x, op);
    }

    void uni_vmovups_tail(const Xbyak::Address &addr, const Xbyak::Ymm &mask,
            const Xbyak::Ymm &x) {
        vmaskmovps(addr, mask, x);
    }
    void uni_vmovups_tail(const Xbyak::Ymm &x, const Xbyak::Ymm &mask,
            const Xbyak::Address &addr) {
        vmaskmovps(x, mask, addr);
    }

    void uni_vmovups_tail(const Xbyak::Address &addr, const Xbyak::Opmask &mask,
            const Xbyak::Zmm &x) {
        vmovups(addr | mask, x);
    }
    void uni_vmovups_tail(const Xbyak::Zmm &x, const Xbyak::Opmask &mask,
            const Xbyak::Address &addr) {
        vmovups(x | mask | T_z, addr);
    }

    void uni_vmovntps(const Xbyak::Address &addr, const Xbyak::Xmm &x) {
        if (is_valid_isa(avx))
            vmovntps(addr, x);
        else
            movntps(addr, x);
    }

    void uni_vbroadcastss(const Xbyak::Xmm &x, const Xbyak::Operand &op) {
        if (is_valid_isa(avx2) || (is_valid_isa(avx) && op.isMEM()))
            vbroadcastss(x, op);
        else if (is_valid_isa(avx)) {
            vmovss(x, x, op);
            vshufps(x, x, x, 0x0);
        } else {
            movss(x, op);
            shufps(x, x, 0x0);
        }
    }
    void uni_vbroadcastss(const Xbyak::Ymm &x, const Xbyak::Operand &op) {
        if (op.isMEM() || is_valid_isa(avx2)) {
            vbroadcastss(x, op);
        } else {
            Xbyak::Xmm t(x.getIdx());
            if (!t.isEqualIfNotInherited(op)) movss(t, op);
            vinsertf128(x, x, t, 1);
            vshufps(x, x, x, 0);
        }
    }

    void uni_vpbroadcastd(const Xbyak::Xmm &x, const Xbyak::Operand &op) {
        if (is_valid_isa(avx2))
            vpbroadcastd(x, op);
        else if (is_valid_isa(avx)) {
            if (op.isMEM())
                vmovss(x, op.getAddress());
            else
                vmovss(x, x, op);
            vpshufd(x, x, 0x0);
        } else {
            movss(x, op);
            pshufd(x, x, 0x0);
        }
    }
    void uni_vpbroadcastd(const Xbyak::Ymm &x, const Xbyak::Operand &op) {
        if (is_valid_isa(avx2)) {
            vpbroadcastd(x, op);
        } else {
            const Xbyak::Xmm t(x.getIdx());
            if (!t.isEqualIfNotInherited(op)) {
                if (op.isMEM())
                    vmovss(t, op.getAddress());
                else
                    vmovss(t, t, op);
            }
            vinsertf128(x, x, t, 1);
            vshufps(x, x, x, 0);
        }
    }

    void uni_vshufps(const Xbyak::Xmm &x1, const Xbyak::Xmm &x2,
            const Xbyak::Operand &op, Xbyak::uint8 imm) {
        if (is_valid_isa(avx))
            vshufps(x1, x2, op, imm);
        else {
            movups(x1, x2);
            shufps(x1, op, imm);
        }
    }

    void uni_vpshufd(
            const Xbyak::Xmm &x1, const Xbyak::Operand &op, Xbyak::uint8 imm) {
        if (is_valid_isa(avx))
            vpshufd(x1, op, imm);
        else {
            pshufd(x1, op, imm);
        }
    }

    void uni_vrcpss(const Xbyak::Xmm &x, const Xbyak::Operand &op) {
        rcpss(x, op);
    }
    void uni_vrcpss(const Xbyak::Ymm &x1, const Xbyak::Xmm &x2) {
        Xbyak::Xmm x1_(x1.getIdx());
        Xbyak::Xmm x2_(x2.getIdx());
        vrcpss(x1_, x1_, x2_);
    }
    void uni_vrcpss(const Xbyak::Ymm &x, const Xbyak::Address &op) {
        Xbyak::Xmm x_(x.getIdx());
        vrcpss(x_, x_, op);
    }

    void uni_vrcpps(const Xbyak::Xmm &x, const Xbyak::Operand &op) {
        rcpps(x, op);
    }
    void uni_vrcpps(const Xbyak::Ymm &x, const Xbyak::Operand &op) {
        vrcpps(x, op);
    }
    void uni_vrcpps(const Xbyak::Zmm &x, const Xbyak::Operand &op) {
        vrcp14ps(x, op);
    }

    void uni_vdivps(const Xbyak::Xmm &x, const Xbyak::Operand &op1,
            const Xbyak::Operand &op2) {
        if (is_valid_isa(avx))
            vdivps(x, op1, op2);
        else {
            assert(x.isEqualIfNotInherited(op1));
            divps(x, op2);
        }
    }
    void uni_vdivps(const Xbyak::Ymm &x, const Xbyak::Operand &op1,
            const Xbyak::Operand &op2) {
        vdivps(x, op1, op2);
    }

    void uni_vdivss(const Xbyak::Xmm &x, const Xbyak::Operand &op1,
            const Xbyak::Operand &op2) {
        if (is_valid_isa(avx))
            vdivss(x, op1, op2);
        else {
            assert(x.isEqualIfNotInherited(op1));
            divss(x, op2);
        }
    }

    void uni_vdivps(const Xbyak::Xmm &x, const Xbyak::Operand &op1,
            const Xbyak::Operand &op2, const Xbyak::Xmm &buf) {
        movups(buf, op1);
        divps(buf, op2);
        if (x.getIdx() != buf.getIdx()) { movups(x, buf); }
    }

    void uni_vdivps(const Xbyak::Ymm &x, const Xbyak::Operand &op1,
            const Xbyak::Operand &op2, const Xbyak::Ymm &buf) {
        vdivps(x, op1, op2);
    }

    void uni_vaddps(const Xbyak::Xmm &x, const Xbyak::Operand &op1,
            const Xbyak::Operand &op2) {
        if (is_valid_isa(avx))
            vaddps(x, op1, op2);
        else {
            assert(x.getIdx() == op1.getIdx());
            addps(x, op2);
        }
    }
    void uni_vaddps(const Xbyak::Ymm &x, const Xbyak::Operand &op1,
            const Xbyak::Operand &op2) {
        vaddps(x, op1, op2);
    }
    void uni_vaddss(const Xbyak::Xmm &x, const Xbyak::Operand &op1,
            const Xbyak::Operand &op2) {
        if (is_valid_isa(avx))
            vaddss(x, op1, op2);
        else {
            assert(x.isEqualIfNotInherited(op1));
            addss(x, op2);
        }
    }
    void uni_vaddss(const Xbyak::Ymm &x, const Xbyak::Operand &op1,
            const Xbyak::Operand &op2) {
        vaddss(x, op1, op2);
    }

    void uni_vphaddd(const Xbyak::Xmm &x, const Xbyak::Xmm &x2,
            const Xbyak::Operand &op) {
        if (is_valid_isa(avx)) {
            vphaddd(x, x2, op);
        } else {
            assert(x.isEqualIfNotInherited(op));
            phaddd(x, op);
        }
    }

    void uni_vhaddps(const Xbyak::Xmm &x, const Xbyak::Xmm &x2,
            const Xbyak::Operand &op) {
        if (is_valid_isa(avx)) {
            vhaddps(x, x2, op);
        } else {
            assert(x.isEqualIfNotInherited(op));
            haddps(x, op);
        }
    }

    void uni_vpsignd(const Xbyak::Xmm &x1, const Xbyak::Xmm &x2,
            const Xbyak::Operand &op) {
        assert(x1.getIdx() == x2.getIdx());
        psignd(x1, op);
    }
    void uni_vpsignd(const Xbyak::Ymm &x1, const Xbyak::Ymm &x2,
            const Xbyak::Operand &op) {
        vpsignd(x1, x2, op);
    }

    void uni_vpsubd(const Xbyak::Xmm &x1, const Xbyak::Xmm &x2,
            const Xbyak::Operand &op) {
        assert(x1.getIdx() == x2.getIdx());
        psubd(x1, op);
    }
    void uni_vpsubd(const Xbyak::Ymm &x1, const Xbyak::Ymm &x2,
            const Xbyak::Operand &op) {
        vpsubd(x1, x2, op);
    }

    void uni_vpsubb(const Xbyak::Xmm &x1, const Xbyak::Xmm &x2,
            const Xbyak::Operand &op) {
        assert(x1.getIdx() == x2.getIdx());
        psubb(x1, op);
    }
    void uni_vpsubb(const Xbyak::Ymm &x1, const Xbyak::Ymm &x2,
            const Xbyak::Operand &op) {
        vpsubb(x1, x2, op);
    }

    void uni_vsubss(const Xbyak::Xmm &x, const Xbyak::Operand &op1,
            const Xbyak::Operand &op2) {
        assert(x.isEqualIfNotInherited(op1));
        subps(x, op2);
    }
    void uni_vsubss(const Xbyak::Ymm &x, const Xbyak::Operand &op1,
            const Xbyak::Operand &op2) {
        vsubss(x, Xbyak::Xmm(op1.getIdx()), Xbyak::Xmm(op2.getIdx()));
    }

    void uni_vsubps(const Xbyak::Xmm &x, const Xbyak::Operand &op1,
            const Xbyak::Operand &op2) {
        if (is_valid_isa(avx))
            vsubps(x, op1, op2);
        else {
            assert(x.isEqualIfNotInherited(op1));
            subps(x, op2);
        }
    }
    void uni_vsubps(const Xbyak::Ymm &x, const Xbyak::Operand &op1,
            const Xbyak::Operand &op2) {
        vsubps(x, op1, op2);
    }

    void uni_vsubps(const Xbyak::Xmm &x, const Xbyak::Operand &op1,
            const Xbyak::Operand &op2, const Xbyak::Xmm &buf) {
        movups(buf, op1);
        subps(buf, op2);
        if (x.getIdx() != buf.getIdx()) { movups(x, buf); }
    }

    void uni_vsubps(const Xbyak::Ymm &x, const Xbyak::Operand &op1,
            const Xbyak::Operand &op2, const Xbyak::Ymm &buf) {
        vsubps(x, op1, op2);
    }

    void uni_vpmulld(const Xbyak::Xmm &x1, const Xbyak::Xmm &x2,
            const Xbyak::Operand &op) {
        if (is_valid_isa(avx)) {
            vpmulld(x1, x2, op);
        } else {
            if (x1.getIdx() != x2.getIdx()) movdqa(x1, x2);
            pmulld(x1, op);
        }
    }
    void uni_vpmulld(const Xbyak::Ymm &x1, const Xbyak::Ymm &x2,
            const Xbyak::Operand &op) {
        vpmulld(x1, x2, op);
    }

    void uni_vmulps(const Xbyak::Xmm &x, const Xbyak::Operand &op1,
            const Xbyak::Operand &op2) {
        if (is_valid_isa(avx))
            vmulps(x, op1, op2);
        else {
            if (!x.isEqualIfNotInherited(op1)) movups(x, op1);
            mulps(x, op2);
        }
    }
    void uni_vmulps(const Xbyak::Ymm &x, const Xbyak::Operand &op1,
            const Xbyak::Operand &op2) {
        vmulps(x, op1, op2);
    }

    void uni_vmulss(const Xbyak::Xmm &x, const Xbyak::Operand &op1,
            const Xbyak::Operand &op2) {
        if (is_valid_isa(avx))
            vmulss(x, op1, op2);
        else {
            assert(x.isEqualIfNotInherited(op1));
            mulss(x, op2);
        }
    }
    void uni_vmulss(const Xbyak::Ymm &x, const Xbyak::Operand &op1,
            const Xbyak::Address &op2) {
        vmulss(x, Xbyak::Xmm(op1.getIdx()), op2);
    }
    void uni_vmulss(const Xbyak::Ymm &x, const Xbyak::Operand &op1,
            const Xbyak::Ymm &op2) {
        vmulss(x, Xbyak::Xmm(op1.getIdx()), Xbyak::Xmm(op2.getIdx()));
    }

    void uni_vfmadd132ps(const Xbyak::Xmm &x1, const Xbyak::Xmm &x2,
            const Xbyak::Operand &op) {
        // Note: x1 gets overriden by x1*op
        // This is incorrect if x1 == x2
        assert(x1.getIdx() != x2.getIdx());
        mulps(x1, op);
        addps(x1, x2);
    }
    void uni_vfmadd132ps(const Xbyak::Ymm &x1, const Xbyak::Ymm &x2,
            const Xbyak::Operand &op) {
        if (is_valid_isa(avx2))
            vfmadd132ps(x1, x2, op);
        else {
            // Note: x1 gets overriden by x1*op
            // This is incorrect if x1 == x2
            assert(x1.getIdx() != x2.getIdx());
            vmulps(x1, x1, op);
            vaddps(x1, x1, x2);
        }
    }

    void uni_vfmadd213ps(const Xbyak::Xmm &x1, const Xbyak::Xmm &x2,
            const Xbyak::Operand &op) {
        // Note: x1 gets overriden by x1*x2
        // This is incorrect if x1 == op
        assert(!x1.isEqualIfNotInherited(op));
        mulps(x1, x2);
        addps(x1, op);
    }
    void uni_vfmadd213ps(const Xbyak::Ymm &x1, const Xbyak::Ymm &x2,
            const Xbyak::Operand &op) {
        if (is_valid_isa(avx2))
            vfmadd213ps(x1, x2, op);
        else {
            // Note: x1 gets overriden by x1*x2
            // This is incorrect if x1 == op
            assert(!x1.isEqualIfNotInherited(op));
            vmulps(x1, x1, x2);
            vaddps(x1, x1, op);
        }
    }

    void uni_vfmadd213ss(const Xbyak::Xmm &x1, const Xbyak::Xmm &x2,
            const Xbyak::Operand &op) {
        // Note: x1 gets overriden by x1*x2
        // This is incorrect if x1 == op
        assert(!x1.isEqualIfNotInherited(op));
        mulss(x1, x2);
        addss(x1, op);
    }
    void uni_vfmadd213ss(const Xbyak::Ymm &x1, const Xbyak::Ymm &x2,
            const Xbyak::Operand &op) {
        if (is_valid_isa(avx2))
            vfmadd213ss(x1, x2, op);
        else {
            // Note: x1 gets overriden by x1*x2
            // This is incorrect if x1 == op
            assert(!x1.isEqualIfNotInherited(op));
            vmulss(x1, x1, x2);
            vaddss(x1, x1, op);
        }
    }

    void uni_vfmadd231ps(const Xbyak::Xmm &x1, const Xbyak::Xmm &x2,
            const Xbyak::Operand &op) {
        // Note: x2 gets overriden by x2*op
        // This is incorrect if x1 == x2
        assert(x1.getIdx() != x2.getIdx());
        mulps(x2, op);
        addps(x1, x2);
    }
    void uni_vfmadd231ps(const Xbyak::Ymm &x1, const Xbyak::Ymm &x2,
            const Xbyak::Operand &op) {
        if (is_valid_isa(avx2))
            vfmadd231ps(x1, x2, op);
        else {
            // Note: x2 gets overriden by x2*op
            // This is incorrect if x1 == x2
            assert(x1.getIdx() != x2.getIdx());
            vmulps(x2, x2, op);
            vaddps(x1, x1, x2);
        }
    }
    void uni_vfmadd231ss(const Xbyak::Xmm &x1, const Xbyak::Xmm &x2,
            const Xbyak::Operand &op) {
        // Note: x2 gets overriden by x2*op
        // This is incorrect if x1 == x2
        if (is_valid_isa(avx2))
            vfmadd231ss(x1, x2, op);
        else if (is_valid_isa(avx)) {
            vmulss(x2, x2, op);
            vaddss(x1, x1, x2);
        } else {
            assert(x1.getIdx() != x2.getIdx());
            mulss(x2, op);
            addss(x1, x2);
        }
    }
    void uni_vfmadd231ss(const Xbyak::Ymm &x1, const Xbyak::Ymm &x2,
            const Xbyak::Operand &op) {
        if (is_valid_isa(avx2))
            vfmadd231ss(Xbyak::Xmm(x1.getIdx()), Xbyak::Xmm(x2.getIdx()), op);
        else {
            // Note: x2 gets overriden by x2*op
            // This is incorrect if x1 == x2
            assert(x1.getIdx() != x2.getIdx());
            vmulss(x2, x2, op);
            vaddss(x1, x1, x2);
        }
    }

    void uni_vfnmadd231ps(const Xbyak::Xmm &x1, const Xbyak::Xmm &x2,
            const Xbyak::Operand &op) {
        // Note: x2 gets overriden by x2*op
        // This is incorrect if x1 == x2
        if (is_valid_isa(avx2))
            vfnmadd231ps(x1, x2, op);
        else if (is_valid_isa(avx)) {
            vmulps(x2, x2, op);
            vsubps(x1, x1, x2);
        } else {
            assert(x1.getIdx() != x2.getIdx());
            mulps(x2, op);
            subps(x1, x2);
        }
    }

    void uni_vfnmadd231ps(const Xbyak::Ymm &x1, const Xbyak::Ymm &x2,
            const Xbyak::Operand &op) {
        if (is_valid_isa(avx2))
            vfnmadd231ps(x1, x2, op);
        else {
            // Note: x2 gets overriden by x2*op
            // This is incorrect if x1 == x2
            assert(x1.getIdx() != x2.getIdx());
            vmulps(x2, x2, op);
            vsubps(x1, x1, x2);
        }
    }

    void uni_vfnmadd231ss(const Xbyak::Xmm &x1, const Xbyak::Xmm &x2,
            const Xbyak::Operand &op) {
        // Note: x2 gets overriden by x2*op
        // This is incorrect if x1 == x2
        if (is_valid_isa(avx2))
            vfnmadd231ss(x1, x2, op);
        else if (is_valid_isa(avx)) {
            vmulss(x2, x2, op);
            vsubss(x1, x1, x2);
        } else {
            assert(x1.getIdx() != x2.getIdx());
            mulss(x2, op);
            subss(x1, x2);
        }
    }

    void uni_vfnmadd231ss(const Xbyak::Ymm &x1, const Xbyak::Ymm &x2,
            const Xbyak::Operand &op) {
        if (is_valid_isa(avx2))
            vfnmadd231ss(x1, x2, op);
        else {
            // Note: x2 gets overriden by x2*op
            // This is incorrect if x1 == x2
            assert(x1.getIdx() != x2.getIdx());
            vmulss(x2, x2, op);
            vsubss(x1, x1, x2);
        }
    }

    void uni_vfmsub213ps(const Xbyak::Xmm &x1, const Xbyak::Xmm &x2,
            const Xbyak::Operand &op) {
        // Note: x1 gets overriden by x1*x2
        // This is incorrect if x1 == op
        assert(!x1.isEqualIfNotInherited(op));
        mulps(x1, x2);
        subps(x1, op);
    }
    void uni_vfmsub213ps(const Xbyak::Ymm &x1, const Xbyak::Ymm &x2,
            const Xbyak::Operand &op) {
        if (is_valid_isa(avx2))
            vfmsub213ps(x1, x2, op);
        else {
            // Note: x1 gets overriden by x1*x2
            // This is incorrect if x1 == op
            assert(!x1.isEqualIfNotInherited(op));
            vmulps(x1, x1, x2);
            vsubps(x1, x1, op);
        }
    }

    void uni_vsqrtps(const Xbyak::Xmm &x, const Xbyak::Operand &op) {
        sqrtps(x, op);
    }
    void uni_vsqrtps(const Xbyak::Ymm &x, const Xbyak::Operand &op) {
        vsqrtps(x, op);
    }

    void uni_vpaddd(const Xbyak::Xmm &x1, const Xbyak::Xmm &x2,
            const Xbyak::Operand &op) {
        if (is_valid_isa(avx))
            vpaddd(x1, x2, op);
        else {
            if (x1.getIdx() != x2.getIdx()) movdqa(x1, x2);
            paddd(x1, op);
        }
    }
    void uni_vpaddd(const Xbyak::Ymm &x1, const Xbyak::Ymm &x2,
            const Xbyak::Operand &op) {
        vpaddd(x1, x2, op);
    }

    void uni_vpaddb(const Xbyak::Xmm &x1, const Xbyak::Xmm &x2,
            const Xbyak::Operand &op) {
        if (is_valid_isa(avx))
            vpaddb(x1, x2, op);
        else {
            if (x1.getIdx() != x2.getIdx()) movdqa(x1, x2);
            paddb(x1, op);
        }
    }
    void uni_vpaddb(const Xbyak::Ymm &x1, const Xbyak::Ymm &x2,
            const Xbyak::Operand &op) {
        vpaddb(x1, x2, op);
    }

    void uni_vpmaddwd(const Xbyak::Xmm &x1, const Xbyak::Xmm &x2,
            const Xbyak::Operand &op) {
        if (is_valid_isa(avx))
            vpmaddwd(x1, x2, op);
        else {
            if (x1.getIdx() != x2.getIdx()) movdqa(x1, x2);
            pmaddwd(x1, op);
        }
    }
    void uni_vpmaddwd(const Xbyak::Ymm &x1, const Xbyak::Ymm &x2,
            const Xbyak::Operand &op) {
        vpmaddwd(x1, x2, op);
    }

    void uni_vpmaddubsw(const Xbyak::Xmm &x1, const Xbyak::Xmm &x2,
            const Xbyak::Operand &op) {
        if (is_valid_isa(avx))
            vpmaddubsw(x1, x2, op);
        else {
            if (x1.getIdx() != x2.getIdx()) movdqa(x1, x2);
            pmaddubsw(x1, op);
        }
    }
    void uni_vpmaddubsw(const Xbyak::Ymm &x1, const Xbyak::Ymm &x2,
            const Xbyak::Operand &op) {
        vpmaddubsw(x1, x2, op);
    }

    void uni_vandps(const Xbyak::Xmm &x1, const Xbyak::Xmm &x2,
            const Xbyak::Operand &op) {
        assert(x1.getIdx() == x2.getIdx());
        andps(x1, op);
    }
    void uni_vandps(const Xbyak::Ymm &x1, const Xbyak::Ymm &x2,
            const Xbyak::Operand &op) {
        if (!is_valid_isa(avx512_common) || x1.getBit() < 512)
            vandps(x1, x2, op);
        else
            vpandd(x1, x2, op);
    }

    void uni_vorps(const Xbyak::Xmm &x1, const Xbyak::Xmm &x2,
            const Xbyak::Operand &op) {
        assert(x1.getIdx() == x2.getIdx());
        orps(x1, op);
    }
    void uni_vorps(const Xbyak::Ymm &x1, const Xbyak::Ymm &x2,
            const Xbyak::Operand &op) {
        if (!is_valid_isa(avx512_common) || x1.getBit() < 512)
            vorps(x1, x2, op);
        else
            vpord(x1, x2, op);
    }

    void uni_vxorps(const Xbyak::Xmm &x1, const Xbyak::Xmm &x2,
            const Xbyak::Operand &op) {
        if (is_valid_isa(avx))
            vxorps(x1, x2, op);
        else {
            if (x1.getIdx() != x2.getIdx()) { uni_vmovups(x1, x2); }
            xorps(x1, op);
        }
    }
    void uni_vxorps(const Xbyak::Ymm &x1, const Xbyak::Ymm &x2,
            const Xbyak::Operand &op) {
        if (!is_valid_isa(avx512_common) || x1.getBit() < 512)
            vxorps(x1, x2, op);
        else
            vpxord(x1, x2, op);
    }

    void uni_vpslld(
            const Xbyak::Xmm &x, const Xbyak::Operand &op, const int imm) {
        assert(x.isEqualIfNotInherited(op));
        pslld(x, imm);
    }
    void uni_vpslld(
            const Xbyak::Ymm &x, const Xbyak::Operand &op, const int imm) {
        vpslld(x, op, imm);
    }

    void uni_vpsrld(
            const Xbyak::Xmm &x, const Xbyak::Operand &op, const int imm) {
        if (!x.isEqualIfNotInherited(op)) uni_vmovups(x, op);
        psrld(x, imm);
    }
    void uni_vpsrld(
            const Xbyak::Ymm &x, const Xbyak::Operand &op, const int imm) {
        vpsrld(x, op, imm);
    }

    void uni_vmaxps(const Xbyak::Xmm &x, const Xbyak::Operand &op1,
            const Xbyak::Operand &op2) {
        if (is_valid_isa(avx))
            vmaxps(x, op1, op2);
        else {
            if (!x.isEqualIfNotInherited(op1)) movups(x, op1);
            maxps(x, op2);
        }
    }
    void uni_vmaxps(const Xbyak::Ymm &x, const Xbyak::Operand &op1,
            const Xbyak::Operand &op2) {
        vmaxps(x, op1, op2);
    }

    void uni_vmaxss(const Xbyak::Xmm &x, const Xbyak::Operand &op1,
            const Xbyak::Operand &op2) {
        if (is_valid_isa(avx))
            vmaxss(x, op1, op2);
        else {
            if (!x.isEqualIfNotInherited(op1)) movss(x, op1);
            maxss(x, op2);
        }
    }

    void uni_vminps(const Xbyak::Xmm &x, const Xbyak::Operand &op1,
            const Xbyak::Operand &op2) {

        if (is_valid_isa(avx))
            vminps(x, op1, op2);
        else {
            if (!x.isEqualIfNotInherited(op1)) movups(x, op1);
            minps(x, op2);
        }
    }

    void uni_vminps(const Xbyak::Ymm &x, const Xbyak::Operand &op1,
            const Xbyak::Operand &op2) {
        vminps(x, op1, op2);
    }

    void uni_vminss(const Xbyak::Xmm &x, const Xbyak::Operand &op1,
            const Xbyak::Operand &op2) {

        if (is_valid_isa(avx))
            vminss(x, op1, op2);
        else {
            if (!x.isEqualIfNotInherited(op1)) movss(x, op1);
            minss(x, op2);
        }
    }

    void uni_vpmovsxbd(const Xbyak::Xmm &x, const Xbyak::Operand &op) {
        if (is_valid_isa(avx))
            vpmovsxbd(x, op);
        else
            pmovsxbd(x, op);
    }

    void uni_vpmovsxbd(const Xbyak::Ymm &y, const Xbyak::Operand &op) {
        vpmovsxbd(y, op);
    }

    void uni_vpmovzxbd(const Xbyak::Xmm &x, const Xbyak::Operand &op) {
        if (is_valid_isa(avx))
            vpmovzxbd(x, op);
        else
            pmovzxbd(x, op);
    }

    void uni_vpmovzxbd(const Xbyak::Ymm &y, const Xbyak::Operand &op) {
        vpmovzxbd(y, op);
    }

    void uni_vcmpps(const Xbyak::Xmm &x1, const Xbyak::Xmm &x2,
            const Xbyak::Operand &op, int cmp_predicate) {
        if (x1.getIdx() != x2.getIdx()) uni_vmovups(x1, x2);
        cmpps(x1, op, cmp_predicate);
    }
    void uni_vcmpps(const Xbyak::Ymm &x1, const Xbyak::Ymm &x2,
            const Xbyak::Operand &op, int cmp_predicate) {
        vcmpps(x1, x2, op, cmp_predicate);
    }

    void uni_vtestps(const Xbyak::Xmm &x1, const Xbyak::Operand &op) {
        ptest(x1, op);
    }

    void uni_vtestps(const Xbyak::Ymm &x1, const Xbyak::Operand &op) {
        assert(!(x1.isZMM() || op.isZMM()));
        vtestps(x1, op);
    }

    void uni_vblendvps(const Xbyak::Xmm &x1, const Xbyak::Xmm &x2,
            const Xbyak::Operand &op, const Xbyak::Xmm &msk) {
        assert(x1.getIdx() == x2.getIdx());
        assert(msk.getIdx() == 0);
        blendvps(x1, op);
    }
    void uni_vblendvps(const Xbyak::Ymm &x1, const Xbyak::Ymm &x2,
            const Xbyak::Operand &op, const Xbyak::Ymm &msk) {
        vblendvps(x1, x2, op, msk);
    }

    void uni_vblendps(const Xbyak::Xmm &x1, const Xbyak::Xmm &x2,
            const Xbyak::Operand &op, const int imm) {
        assert(!x1.isZMM() && !x2.isZMM());

        if (is_valid_isa(avx))
            vblendps(x1, x2, op, imm);
        else {
            assert(x1.getIdx() == x2.getIdx());
            blendps(x1, op, imm);
        }
    }

    void uni_vroundps(
            const Xbyak::Xmm &x, const Xbyak::Operand &op, const int imm) {
        roundps(x, op, imm);
    }
    void uni_vroundps(
            const Xbyak::Ymm &x, const Xbyak::Operand &op, const int imm) {
        vroundps(x, op, imm);
    }
    void uni_vroundps(
            const Xbyak::Zmm &x, const Xbyak::Operand &op, const int imm) {
        vrndscaleps(x, op, imm & 0x3);
    }

    void uni_vcvtps2dq(const Xbyak::Xmm &x, const Xbyak::Operand &op) {
        if (is_valid_isa(avx))
            vcvtps2dq(x, op);
        else
            cvtps2dq(x, op);
    }
    void uni_vcvtps2dq(const Xbyak::Ymm &x, const Xbyak::Operand &op) {
        vcvtps2dq(x, op);
    }

    void uni_vcvttps2dq(const Xbyak::Xmm &x, const Xbyak::Operand &op) {
        if (is_valid_isa(avx))
            vcvttps2dq(x, op);
        else
            cvttps2dq(x, op);
    }

    void uni_vcvtdq2ps(const Xbyak::Xmm &x, const Xbyak::Operand &op) {
        if (is_valid_isa(avx))
            vcvtdq2ps(x, op);
        else
            cvtdq2ps(x, op);
    }

    void uni_vcvtdq2ps(const Xbyak::Ymm &x, const Xbyak::Operand &op) {
        vcvtdq2ps(x, op);
    }

    void uni_vmovmskps(const Xbyak::Reg &x1, const Xbyak::Xmm &x2) {
        movmskps(x1.cvt64(), x2);
    }
    void uni_vmovmskps(const Xbyak::Reg &x1, const Xbyak::Ymm &x2) {
        vmovmskps(x1, x2);
    }

    void uni_vmovd(const Xbyak::Reg32 &r, const Xbyak::Xmm &x) {
        if (is_valid_isa(avx))
            vmovd(r, x);
        else
            movd(r, x);
    }
    void uni_vmovd(const Xbyak::Xmm &x, const Xbyak::Reg32 &r) {
        if (is_valid_isa(avx))
            vmovd(x, r);
        else
            movd(x, r);
    }
    void uni_vmovd(const Xbyak::Address &addr, const Xbyak::Xmm &x) {
        if (is_valid_isa(avx))
            vmovd(addr, x);
        else
            movd(addr, x);
    }

    void uni_vmovd(const Xbyak::Xmm &x, const Xbyak::Address &addr) {
        if (is_valid_isa(avx))
            vmovd(x, addr);
        else
            movd(x, addr);
    }

    void uni_vmovq(const Xbyak::Xmm &x, const Xbyak::Reg64 &r) {
        if (is_valid_isa(avx))
            vmovq(x, r);
        else
            movq(x, r);
    }
    void uni_vmovq(const Xbyak::Address &addr, const Xbyak::Xmm &x) {
        if (is_valid_isa(avx))
            vmovq(addr, x);
        else
            movq(addr, x);
    }

    void uni_vpackssdw(const Xbyak::Xmm &x1, const Xbyak::Xmm &x2,
            const Xbyak::Operand &op) {
        if (is_valid_isa(avx))
            vpackssdw(x1, x2, op);
        else {
            assert(x1.getIdx() == x2.getIdx());
            packssdw(x1, op);
        }
    }
    void uni_vpackssdw(const Xbyak::Ymm &x1, const Xbyak::Ymm &x2,
            const Xbyak::Operand &op) {
        vpackssdw(x1, x2, op);
    }

    void uni_vpackuswb(const Xbyak::Xmm &x1, const Xbyak::Xmm &x2,
            const Xbyak::Operand &op) {
        if (is_valid_isa(avx))
            vpackuswb(x1, x2, op);
        else {
            assert(x1.getIdx() == x2.getIdx());
            packuswb(x1, op);
        }
    }
    void uni_vpackuswb(const Xbyak::Ymm &x1, const Xbyak::Ymm &x2,
            const Xbyak::Operand &op) {
        vpackuswb(x1, x2, op);
    }

    void uni_vpacksswb(const Xbyak::Xmm &x1, const Xbyak::Xmm &x2,
            const Xbyak::Operand &op) {
        if (is_valid_isa(avx))
            vpacksswb(x1, x2, op);
        else {
            assert(x1.getIdx() == x2.getIdx());
            packsswb(x1, op);
        }
    }
    void uni_vpacksswb(const Xbyak::Ymm &x1, const Xbyak::Ymm &x2,
            const Xbyak::Operand &op) {
        vpacksswb(x1, x2, op);
    }

    void uni_vpinsrb(const Xbyak::Xmm &x1, const Xbyak::Xmm &x2,
            const Xbyak::Operand &op, const int imm) {
        assert(x1.getIdx() == x2.getIdx());
        if (is_valid_isa(avx))
            vpinsrb(x1, x2, op, imm);
        else
            pinsrb(x1, op, imm);
    }

    void uni_vpinsrb(const Xbyak::Ymm &x1, const Xbyak::Ymm &x2,
            const Xbyak::Operand &op, const int imm) {
        vpinsrb(x1, x2, op, imm);
    }

    void uni_vpinsrd(const Xbyak::Xmm &x1, const Xbyak::Xmm &x2,
            const Xbyak::Operand &op, const int imm) {
        assert(x1.getIdx() == x2.getIdx());
        if (is_valid_isa(avx))
            vpinsrd(x1, x2, op, imm);
        else
            pinsrd(x1, op, imm);
    }
    void uni_vpinsrd(const Xbyak::Ymm &x1, const Xbyak::Ymm &x2,
            const Xbyak::Operand &op, const int imm) {
        vpinsrd(x1, x2, op, imm);
    }

    void uni_vpinsrq(const Xbyak::Xmm &x1, const Xbyak::Xmm &x2,
            const Xbyak::Operand &op, const int imm) {
        assert(x1.getIdx() == x2.getIdx());
        if (is_valid_isa(avx))
            vpinsrq(x1, x2, op, imm);
        else
            pinsrq(x1, op, imm);
    }
    void uni_vpinsrq(const Xbyak::Ymm &x1, const Xbyak::Ymm &x2,
            const Xbyak::Operand &op, const int imm) {
        vpinsrq(x1, x2, op, imm);
    }

    void uni_vpinsrw(const Xbyak::Xmm &x1, const Xbyak::Xmm &x2,
            const Xbyak::Operand &op, const int imm) {
        assert(x1.getIdx() == x2.getIdx());
        if (is_valid_isa(avx))
            vpinsrw(x1, x2, op, imm);
        else
            pinsrw(x1, op, imm);
    }
    void uni_vpinsrw(const Xbyak::Ymm &x1, const Xbyak::Ymm &x2,
            const Xbyak::Operand &op, const int imm) {
        vpinsrw(x1, x2, op, imm);
    }

    void uni_vpextrb(
            const Xbyak::Operand &op, const Xbyak::Xmm &x, const int imm) {
        if (is_valid_isa(avx))
            vpextrb(op, x, imm);
        else
            pextrb(op, x, imm);
    }

    void uni_vpextrb(
            const Xbyak::Operand &op, const Xbyak::Ymm &x, const int imm) {
        vpextrb(op, x, imm);
    }

    void uni_vpextrw(
            const Xbyak::Operand &op, const Xbyak::Xmm &x, const int imm) {
        if (is_valid_isa(avx))
            vpextrw(op, x, imm);
        else
            pextrw(op, x, imm);
    }
    void uni_vpextrw(
            const Xbyak::Operand &op, const Xbyak::Ymm &x, const int imm) {
        vpextrw(op, x, imm);
    }

    void uni_vpextrd(
            const Xbyak::Operand &op, const Xbyak::Xmm &x, const int imm) {
        if (is_valid_isa(avx))
            vpextrd(op, x, imm);
        else
            pextrd(op, x, imm);
    }
    void uni_vpextrd(
            const Xbyak::Operand &op, const Xbyak::Ymm &x, const int imm) {
        vpextrd(op, x, imm);
    }

    void uni_vpextrq(
            const Xbyak::Operand &op, const Xbyak::Xmm &x, const int imm) {
        if (is_valid_isa(avx))
            vpextrq(op, x, imm);
        else
            pextrq(op, x, imm);
    }
    void uni_vpextrq(
            const Xbyak::Operand &op, const Xbyak::Ymm &x, const int imm) {
        vpextrq(op, x, imm);
    }

    void uni_vpmaxsd(const Xbyak::Xmm &x1, const Xbyak::Xmm &x2,
            const Xbyak::Operand &op) {
        if (is_valid_isa(avx))
            vpmaxsd(x1, x2, op);
        else {
            if (x1.getIdx() != x2.getIdx()) movdqa(x1, x2);
            pmaxsd(x1, op);
        }
    }

    void uni_vpmaxsd(const Xbyak::Ymm &x1, const Xbyak::Ymm &x2,
            const Xbyak::Operand &op) {
        vpmaxsd(x1, x2, op);
    }

    void uni_vpmaxsb(const Xbyak::Xmm &x1, const Xbyak::Xmm &x2,
            const Xbyak::Operand &op) {
        if (is_valid_isa(avx))
            vpmaxsb(x1, x2, op);
        else {
            if (x1.getIdx() != x2.getIdx()) movdqa(x1, x2);
            pmaxsb(x1, op);
        }
    }

    void uni_vpmaxsb(const Xbyak::Ymm &x1, const Xbyak::Ymm &x2,
            const Xbyak::Operand &op) {
        vpmaxsb(x1, x2, op);
    }

    void uni_vpminub(const Xbyak::Xmm &x1, const Xbyak::Xmm &x2,
            const Xbyak::Operand &op) {
        if (is_valid_isa(avx))
            vpminub(x1, x2, op);
        else {
            if (x1.getIdx() != x2.getIdx()) movdqa(x1, x2);
            pminub(x1, op);
        }
    }

    void mul_by_const(
            const Xbyak::Reg &out, const Xbyak::Reg64 &tmp, int value) {
        // Generates a shift + add sequence for multiplicating contents of the
        // out register by a known JIT-time value. Clobbers the tmp register.
        //
        // Pros compared to mul/imul:
        // - does not require using known registers
        // - not microcoded on Intel(R) Xeon Phi(TM) processors
        // Still, there are probably a lot of cases when mul/imul is faster on
        // Intel(R) Core(TM) processors. Not intended for critical path.

        // TODO: detect when overflow is emminent (Roma)
        // TODO: detect when using mul/imul is a better option (Roma)

        int p = 0; // the current power of 2
        int old_p = 0; // the last seen power of 2 such that value[old_p] != 0

        xor_(tmp, tmp);
        while (value) {
            if (value & 1) {
                int shift = p - old_p;
                if (shift) {
                    shl(out, shift);
                    old_p = p;
                }
                add(tmp, out);
            }
            value >>= 1;
            p++;
        }
        mov(out, tmp);
    }

    /*
      Saturation facility functions. enable to prepare the register
      holding the saturation upperbound and apply the saturation on
      the floating point register
     */
    template <typename Vmm>
    void init_saturate_f32(Vmm vmm_lbound, Vmm vmm_ubound, Xbyak::Reg64 reg_tmp,
            data_type_t idt, data_type_t odt, bool force_lbound = false) {
        using namespace data_type;
        if (!((idt == f32) && utils::one_of(odt, u8, s8, s32))) return;

        assert(IMPLICATION(idt == u8 || force_lbound,
                vmm_lbound.getIdx() != vmm_ubound.getIdx()));

        auto init_vmm = [&](Vmm vmm, float value) {
            Xbyak::Xmm xmm_tmp(vmm.getIdx());
            mov(reg_tmp, float2int(value));
            uni_vmovq(xmm_tmp, reg_tmp);
            if (vmm.isYMM() || vmm.isZMM())
                uni_vbroadcastss(vmm, xmm_tmp);
            else
                uni_vshufps(vmm, xmm_tmp, xmm_tmp, 0);
        };

        // No need to saturate on lower bound for signed integer types, as
        // the conversion to int would return INT_MIN, and then proper
        // saturation will happen in store_data. The param force_lbound, will
        // force saturate values unconditionally to lbound.
        if (odt == u8)
            uni_vpxor(vmm_lbound, vmm_lbound, vmm_lbound);
        else if (force_lbound) {
            const float saturation_lbound = odt == s8 ? INT8_MIN : INT32_MIN;
            init_vmm(vmm_lbound, saturation_lbound);
        }

        const float saturation_ubound = types::max_value<float>(odt);
        init_vmm(vmm_ubound, saturation_ubound);
    }

    template <typename Vmm>
    void saturate_f32(const Vmm &vmm, const Vmm &vmm_lbound,
            const Vmm &vmm_ubound, data_type_t odt, bool force_lbound = false) {
        // This function is used to saturate to odt in f32 before converting
        // to s32 in order to avoid bad saturation due to cvtps2dq
        // behavior (it returns INT_MIN if the f32 is out of the
        // s32 range)
        using namespace data_type;
        if (!utils::one_of(odt, u8, s8, s32)) return;

        // no need to apply lower saturation bound when odt is
        // signed, as cvtps2dq will return MIN_INT if the value
        // does not fit. The param force_lbound, will force saturate values
        // unconditionally to lbound.
        if (odt == u8 || force_lbound) {
            if (is_valid_isa(avx))
                vmaxps(vmm, vmm, vmm_lbound);
            else
                maxps(vmm, vmm_lbound);
        }
        if (is_valid_isa(avx))
            vminps(vmm, vmm, vmm_ubound);
        else
            minps(vmm, vmm_ubound);
    }

    /**
    * load_bytes is the utility function to facilitate loading of
    * load_size (0 <= load_size <= 32) many contiguous bytes into the Xmm/Ymm
    * register from the memory referenced by ptr[reg + offset] address.
    *
    * Functionally, invocation of load_bytes is equivalent to
    * the following loop:
    *
    * for (int idx = 0; idx < load_size; ++idx)
    *     vpinsrb(xmm, xmm, ptr[reg + offset + idx], idx);
    *
    * TODO: Add an option to zero-out unloaded bytes in the Xmm register.
    * TODO: Add an option for unsafe_load wherein one could read outside the
    * provided memory buffer so as to minimize the total number of read
    * memory instructions.
    */
    template <typename Vmm>
    void load_bytes(
            const Vmm &vmm, const Xbyak::Address &src_addr, int load_size) {
        const auto addr = [&](int bytes_offset) {
            return ptr[src_addr.getRegExp()
                    + Xbyak::RegExp(bytes_offset * sizeof(int8_t))];
        };

        load_bytes(vmm, load_size, addr);
    }

    template <typename Vmm>
    void load_bytes(const Vmm &vmm, const Xbyak::Reg64 &reg, int64_t offset,
            int load_size) {

        // Ensure offset is at most 4 bytes to be encoded in the instruction
        assert(offset >= INT_MIN && offset <= INT_MAX);

        const auto addr = [&](int bytes_offset) {
            return ptr[reg + offset + bytes_offset * sizeof(int8_t)];
        };

        load_bytes(vmm, load_size, addr);
    }

private:
    template <typename Vmm, typename AddrFunc>
    void load_bytes(const Vmm &vmm, int load_size, const AddrFunc &addr) {

        constexpr bool is_xmm = std::is_same<Vmm, Xbyak::Xmm>::value;
        constexpr bool is_ymm = std::is_same<Vmm, Xbyak::Ymm>::value;
        static_assert(
                is_xmm || is_ymm, "only Xmm or Ymm registers are allowed");

        MAYBE_UNUSED(is_xmm);
        MAYBE_UNUSED(is_ymm);

        // Ensure data fits completely inside the Xmm/Ymm register
        assert(load_size >= 0 && load_size <= 32);

        // At most 16 bytes can fit inside the Xmm register
        assert(IMPLICATION(load_size > 16, is_ymm));

        // Ensure that vector register is compatible with the ISA in hand
        assert(IMPLICATION(is_ymm, is_valid_isa(avx)));

        assert(is_valid_isa(sse41)
                && "routine is not supported for the current isa");

        auto xmm = Xbyak::Xmm(vmm.getIdx());
        auto ymm = Xbyak::Ymm(vmm.getIdx());

        if (load_size == 32) {
            vmovups(ymm, addr(0));
            return;
        }

        int start_bytes = 0;
        int bytes_to_load = load_size;

        if (load_size > 16) {
            // Prepare to insert to upper bits of ymm
            start_bytes = 16;
            bytes_to_load -= 16;
        }

        if (bytes_to_load >= 8 && bytes_to_load < 16)
            uni_vpinsrq(xmm, xmm, addr(start_bytes), 0);
        else if (bytes_to_load == 16)
            uni_vmovdqu(xmm, addr(start_bytes));

        switch (bytes_to_load) {
            case 0: break;
            case 1: uni_vpinsrb(xmm, xmm, addr(start_bytes), 0); break;
            case 2: uni_vpinsrw(xmm, xmm, addr(start_bytes), 0); break;
            case 3:
                uni_vpinsrw(xmm, xmm, addr(start_bytes), 0);
                uni_vpinsrb(xmm, xmm, addr(start_bytes + 2), 2);
                break;
            case 4: uni_vpinsrd(xmm, xmm, addr(start_bytes), 0); break;
            case 5:
                uni_vpinsrd(xmm, xmm, addr(start_bytes), 0);
                uni_vpinsrb(xmm, xmm, addr(start_bytes + 4), 4);
                break;
            case 6:
                uni_vpinsrd(xmm, xmm, addr(start_bytes), 0);
                uni_vpinsrw(xmm, xmm, addr(start_bytes + 4), 2);
                break;
            case 7:
                uni_vpinsrd(xmm, xmm, addr(start_bytes), 0);
                uni_vpinsrw(xmm, xmm, addr(start_bytes + 4), 2);
                uni_vpinsrb(xmm, xmm, addr(start_bytes + 6), 6);
                break;
            case 8: break;
            case 9: uni_vpinsrb(xmm, xmm, addr(start_bytes + 8), 8); break;
            case 10: uni_vpinsrw(xmm, xmm, addr(start_bytes + 8), 4); break;
            case 11:
                uni_vpinsrw(xmm, xmm, addr(start_bytes + 8), 4);
                uni_vpinsrb(xmm, xmm, addr(start_bytes + 10), 10);
                break;
            case 12: uni_vpinsrd(xmm, xmm, addr(start_bytes + 8), 2); break;
            case 13:
                uni_vpinsrd(xmm, xmm, addr(start_bytes + 8), 2);
                uni_vpinsrb(xmm, xmm, addr(start_bytes + 12), 12);
                break;
            case 14:
                uni_vpinsrd(xmm, xmm, addr(start_bytes + 8), 2);
                uni_vpinsrw(xmm, xmm, addr(start_bytes + 12), 6);
                break;
            case 15:
                uni_vpinsrd(xmm, xmm, addr(start_bytes + 8), 2);
                uni_vpinsrw(xmm, xmm, addr(start_bytes + 12), 6);
                uni_vpinsrb(xmm, xmm, addr(start_bytes + 14), 14);
                break;
            case 16: break;
            default: assert(!"improper load size");
        }

        if (load_size > 16) {
            vinsertf128(ymm, ymm, xmm, 1); // insert to upper bits of ymm
            vinsertf128(ymm, ymm, addr(0), 0); // insert to lower bits of ymm
        }
    }

    /**
    * store_bytes is the utility function to facilitate storing of
    * store_size (0 <= store_size <= 32) many contiguous bytes from the Xmm/Ymm
    * register into the memory referenced by ptr[reg + offset] address.
    *
    * Additionally, when store_size > 16, the input Ymm register will not be
    * preserved due to the usage of vextracti128 instruction.
    *
    * Functionally, invocation of store_bytes is equivalent
    * to the following loop:
    *
    * for (int idx = 0; idx < store_size; ++idx)
    *     vpextrb(ptr[reg + offset + idx], xmm, idx);
    *
    * TODO: Add an option for unsafe_store wherein one could store extra dwords
    * past the provided memory buffer so as to minimize the total number of
    * write memory instructions.
    */
public:
    template <typename Vmm>
    void store_bytes(
            const Vmm &vmm, const Xbyak::Address &dst_addr, int store_size) {
        const auto addr = [&](int bytes_offset) {
            return ptr[dst_addr.getRegExp()
                    + Xbyak::RegExp(bytes_offset * sizeof(int8_t))];
        };
        store_bytes(vmm, store_size, addr);
    }

    template <typename Vmm>
    void store_bytes(const Vmm &vmm, const Xbyak::Reg64 &reg, int64_t offset,
            int store_size) {

        // Ensure offset is at most 4 bytes to be encoded in the instruction
        assert(offset >= INT_MIN && offset <= INT_MAX);

        const auto addr = [&](int bytes_offset) {
            return ptr[reg + offset + bytes_offset * sizeof(int8_t)];
        };

        store_bytes(vmm, store_size, addr);
    }

private:
    template <typename Vmm, typename AddrFunc>
    void store_bytes(const Vmm &vmm, int store_size, const AddrFunc &addr) {

        constexpr bool is_xmm = std::is_same<Vmm, Xbyak::Xmm>::value;
        constexpr bool is_ymm = std::is_same<Vmm, Xbyak::Ymm>::value;
        static_assert(
                is_xmm || is_ymm, "only Xmm or Ymm registers are allowed");

        MAYBE_UNUSED(is_xmm);
        MAYBE_UNUSED(is_ymm);

        // Ensure data fits completely inside the Xmm/Ymm register
        assert(store_size >= 0 && store_size <= 32);

        // At most 16 bytes can fit inside the Xmm register
        assert(IMPLICATION(store_size > 16, is_ymm));

        // Ensure that vector register is compatible with the ISA in hand
        assert(IMPLICATION(is_ymm, is_valid_isa(avx)));

        assert(is_valid_isa(sse41)
                && "routine is not supported for the current isa");

        auto xmm = Xbyak::Xmm(vmm.getIdx());
        auto ymm = Xbyak::Ymm(vmm.getIdx());

        if (store_size == 32) {
            vmovups(addr(0), ymm);
            return;
        }

        int start_bytes = 0;
        int bytes_to_store = store_size;

        if (store_size > 16) {
            vmovdqu(addr(0), xmm); // load lower bits from ymm
            start_bytes = 16;
            bytes_to_store -= 16;
            vextractf128(xmm, ymm, 1); // load upper bits from ymm into xmm
        }

        if (bytes_to_store >= 8 && bytes_to_store < 16)
            uni_vpextrq(addr(start_bytes), xmm, 0);
        else if (bytes_to_store == 16)
            uni_vmovdqu(addr(start_bytes), xmm);

        switch (bytes_to_store) {
            case 0: break;
            case 1: uni_vpextrb(addr(start_bytes), xmm, 0); break;
            case 2: uni_vpextrw(addr(start_bytes), xmm, 0); break;
            case 3:
                uni_vpextrw(addr(start_bytes), xmm, 0);
                uni_vpextrb(addr(start_bytes + 2), xmm, 2);
                break;
            case 4: uni_vpextrd(addr(start_bytes), xmm, 0); break;
            case 5:
                uni_vpextrd(addr(start_bytes), xmm, 0);
                uni_vpextrb(addr(start_bytes + 4), xmm, 4);
                break;
            case 6:
                uni_vpextrd(addr(start_bytes), xmm, 0);
                uni_vpextrw(addr(start_bytes + 4), xmm, 2);
                break;
            case 7:
                uni_vpextrd(addr(start_bytes), xmm, 0);
                uni_vpextrw(addr(start_bytes + 4), xmm, 2);
                uni_vpextrb(addr(start_bytes + 6), xmm, 6);
                break;
            case 8: break;
            case 9: uni_vpextrb(addr(start_bytes + 8), xmm, 8); break;
            case 10: uni_vpextrw(addr(start_bytes + 8), xmm, 4); break;
            case 11:
                uni_vpextrw(addr(start_bytes + 8), xmm, 4);
                uni_vpextrb(addr(start_bytes + 10), xmm, 10);
                break;
            case 12: uni_vpextrd(addr(start_bytes + 8), xmm, 2); break;
            case 13:
                uni_vpextrd(addr(start_bytes + 8), xmm, 2);
                uni_vpextrb(addr(start_bytes + 12), xmm, 12);
                break;
            case 14:
                uni_vpextrd(addr(start_bytes + 8), xmm, 2);
                uni_vpextrw(addr(start_bytes + 12), xmm, 6);
                break;
            case 15:
                uni_vpextrd(addr(start_bytes + 8), xmm, 2);
                uni_vpextrw(addr(start_bytes + 12), xmm, 6);
                uni_vpextrb(addr(start_bytes + 14), xmm, 14);
                break;
            case 16: break;
            default: assert(!"improper store size");
        }
    }

public:
    /**
    * load_bytes_to_dword_extension is the utility function to facilitate
    * loading of load_size (0 <= load_size <= 16) many contiguous bytes in
    * the Xmm register from the memory referenced by ptr[reg + offset]
    * address and then do signed/zero extension of those to double words.
    *
    * Functionally, invocation of load_bytes_to_dword_extension is equivalent
    * to the following:
    *
    * for (int idx = 0; idx < load_size; ++idx)
    *     vpinsrb(xmm, xmm, ptr[reg + offset + idx], idx);
    * if (is_signed) vpmovsxbd(vmm, vmm); else vpmovzxbd(vmm, vmm);
    *
    * Valid values for the load_size variable are:
    * [0..4] for XMM version of the function
    * [0..8] for YMM version of the function.
    * TODO: Implement this routine for every ISA.
    */
    template <typename Vmm>
    void load_bytes_to_dword_extension(const Vmm &vmm, const Xbyak::Reg64 &reg,
            int64_t offset, bool is_signed, int load_size) {
        // Ensure offset is at most 4 bytes to be encoded in the instruction
        assert(offset >= INT_MIN && offset <= INT_MAX);
        load_bytes_to_dword_extension(
                vmm, ptr[reg + offset], is_signed, load_size);
    }

    template <typename Vmm>
    void load_bytes_to_dword_extension(const Vmm &vmm,
            const Xbyak::Address &src_addr, bool is_signed, int load_size) {

        constexpr bool is_xmm = std::is_same<Vmm, Xbyak::Xmm>::value;
        constexpr bool is_ymm = std::is_same<Vmm, Xbyak::Ymm>::value;
        static_assert(
                is_xmm || is_ymm, "only Xmm or Ymm registers are allowed");
        MAYBE_UNUSED(is_xmm);
        MAYBE_UNUSED(is_ymm);

        // Ensure extended double words fit inside Ymm (32 * load_size <= 256)
        assert(load_size >= 0 && load_size <= 8);
        // For Xmm register, load capacity is halved (32 * load_size <= 128)
        assert(IMPLICATION(is_xmm, load_size <= 4));

        // Ensure that vector register is compatible with the ISA in hand
        assert(IMPLICATION(is_ymm, is_valid_isa(avx)));

        assert(is_valid_isa(sse41)
                && "routine is not supported for the current isa");

        // For load_size == 8/4, do load/extension in one go
        if (load_size == 8) {
            const auto ymm = Xbyak::Ymm(vmm.getIdx());
            if (is_signed)
                vpmovsxbd(ymm, src_addr);
            else
                vpmovzxbd(ymm, src_addr);
        } else if (load_size == 4) {
            const auto xmm = Xbyak::Xmm(vmm.getIdx());
            if (is_signed)
                uni_vpmovsxbd(xmm, src_addr);
            else
                uni_vpmovzxbd(xmm, src_addr);
        } else {
            load_bytes(vmm, src_addr, load_size);
            if (is_signed)
                uni_vpmovsxbd(vmm, vmm);
            else
                uni_vpmovzxbd(vmm, vmm);
        }
    }

    /* A utility function to store data of type type_out from vmm register
     * into the memory. Moreover store_size many chunks are written to the
     * memory beginning with ptr[reg + offset] address.
     *
     * Note: Content of Vmm register is not guaranteed to be preserved after the
     * invocation of this routine.
     *
     * TODO: Support for every possible data type.
     */
    template <typename Vmm>
    void store_data(data_type_t type_out, const Vmm &vmm,
            const Xbyak::Reg64 &reg, int64_t offset, int store_size) {

        assert(is_valid_isa(sse41)
                && "routine is not supported for the current isa");
        constexpr bool is_ymm = std::is_same<Vmm, Xbyak::Ymm>::value;

        // Owing to lack of cross lane operations in non avx2 compatible isa
        // this functionality remains unimplemented for int8 data type
        const bool is_int8_dt
                = utils::one_of(type_out, data_type::s8, data_type::u8);
        assert(IMPLICATION(is_ymm && is_int8_dt, is_valid_isa(avx2)));

        // Ensure that vector register is compatible with the ISA in hand
        assert(IMPLICATION(is_ymm, is_valid_isa(avx)));

        MAYBE_UNUSED(is_ymm);
        MAYBE_UNUSED(is_int8_dt);

        auto ymm = Xbyak::Ymm(vmm.getIdx());

        switch (type_out) {
            case data_type::f32:
            case data_type::s32:
                store_bytes(vmm, reg, offset, sizeof(int32_t) * store_size);
                break;
            case data_type::u8:
            case data_type::s8:
                uni_vpackssdw(vmm, vmm, vmm);
                // For each y_i of size 64 bits, following cross lane
                // operation on ymm yields
                // [y_3 y_2 y_1 y_0] |--> [0 0 y_2 y_0]
                if (is_ymm) vpermq(ymm, ymm, 0x08);
                if (type_out == data_type::s8)
                    uni_vpacksswb(vmm, vmm, vmm);
                else
                    uni_vpackuswb(vmm, vmm, vmm);
                store_bytes(vmm, reg, offset, store_size);
                break;
            default: assert(!"unsupported destination data type");
        }
    }

    /* A utility function to load data of type type_in to vmm register
     * from the memory. Moreover load_size many chunks are read from the memory
     * beginning with ptr[reg + offset] address.
     *
     * TODO: Support for every possible data type.
     */
    template <typename Vmm>
    void load_data(data_type_t type_in, const Vmm &vmm, const Xbyak::Reg64 &reg,
            int64_t offset, int load_size) {
        // Ensure offset is at most 4 bytes to be encoded in the instruction
        assert(offset >= INT_MIN && offset <= INT_MAX);
        load_data(type_in, vmm, ptr[reg + offset], load_size);
    }

    template <typename Vmm>
    void load_data(data_type_t type_in, const Vmm &vmm,
            const Xbyak::Address &src_addr, int load_size) {

        assert(is_valid_isa(sse41)
                && "routine is not supported for the current isa");

        switch (type_in) {
            case data_type::f32:
            case data_type::s32:
                load_bytes(vmm, src_addr, sizeof(int32_t) * load_size);
                break;
            case data_type::s8:
            case data_type::u8:
                load_bytes_to_dword_extension(
                        vmm, src_addr, type_in == data_type::s8, load_size);
                break;
            default: assert(!"unsupported source data type");
        }
    }

    /* A utility function to process f32 tail (load, store or other) depending
     * on tail size, stored in Reg64. Tail size must be value from 0 to 3/7
     * (Xmm/Ymm). Tail process functions require integer as argument to specify
     * behavior for each tail size.
     *
     * Only supported for Xmm and Ymm.
     */
    template <typename Vmm>
    void runtime_tail_process(const Xbyak::Reg64 &reg_tail,
            const Xbyak::Reg64 &reg_tmp,
            const std::function<void(int)> &tail_process) {
        constexpr int simd_w_ymm = 8;
        constexpr int f32_bits = sizeof(float) * 8;
        const auto simd_w = Vmm().getBit() / f32_bits;
        assert(simd_w != Xbyak::Zmm().getBit() / f32_bits);

        Xbyak::Label label_tbl, label_tbl_end;
        Xbyak::Label l_case[simd_w_ymm];

        mov(reg_tmp, label_tbl);
        const Xbyak::Address label_address
                = ptr[reg_tmp + reg_tail * sizeof(void *)];
        jmp(label_address);

        // create jump table
        L(label_tbl);
        for (size_t i = 0; i < simd_w; i++)
            putL(l_case[i]);

        // cases for each tail size - from 0 to 3/7
        L(l_case[0]);
        jmp(label_tbl_end, T_NEAR);
        for (size_t i = 1; i < simd_w; i++) {
            L(l_case[i]);
            tail_process(i);
            jmp(label_tbl_end, T_NEAR);
        }
        L(label_tbl_end);
    }

    DNNL_DISALLOW_COPY_AND_ASSIGN(jit_generator);

public:
    /* All uni_ instructions -- apart from uni_vzeroupper() -- will comply with
     * the max_cpu_isa argument */
    jit_generator(void *code_ptr = nullptr, size_t code_size = MAX_CODE_SIZE,
            bool use_autogrow = true, cpu_isa_t max_cpu_isa = isa_all)
        : Xbyak::CodeGenerator(code_size,
                (code_ptr == nullptr && use_autogrow) ? Xbyak::AutoGrow
                                                      : code_ptr)
        , max_cpu_isa_(max_cpu_isa) {}

    virtual ~jit_generator() {}

    virtual const char *name() const = 0;
    virtual const char *source_file() const = 0;

    void register_jit_code(const Xbyak::uint8 *code, size_t code_size) const {
        jit_utils::register_jit_code(code, code_size, name(), source_file());
    }

    const Xbyak::uint8 *jit_ker() const { return jit_ker_; }

    template <typename... kernel_args_t>
    void operator()(kernel_args_t... args) const {
        using jit_kernel_func_t = void (*)(const kernel_args_t... args);
        auto *fptr = (jit_kernel_func_t)jit_ker_;
        (*fptr)(std::forward<kernel_args_t>(args)...);
    }

    virtual status_t create_kernel() {
        generate();
        jit_ker_ = getCode();
        return (jit_ker_) ? status::success : status::runtime_error;
    }

private:
    const cpu_isa_t max_cpu_isa_;
    const Xbyak::uint8 *getCode() {
        this->ready();
        if (!is_initialized()) return nullptr;
        const Xbyak::uint8 *code = CodeGenerator::getCode();
        register_jit_code(code, getSize());
        return code;
    }

    inline bool is_valid_isa(cpu_isa_t isa) {
        return is_subset(isa, max_cpu_isa_) && mayiuse(isa);
    }

    static inline bool is_initialized() {
        return Xbyak::GetError() == Xbyak::ERR_NONE;
    }

protected:
    virtual void generate() = 0;
    const Xbyak::uint8 *jit_ker_ = nullptr;
};

} // namespace x64
} // namespace cpu
} // namespace impl
} // namespace dnnl

#endif
