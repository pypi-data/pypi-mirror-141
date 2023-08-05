/*******************************************************************************
* Copyright 2019-2021 Intel Corporation
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

#ifndef CPU_SIMPLE_RESAMPLING_HPP
#define CPU_SIMPLE_RESAMPLING_HPP

#include <cassert>
#include <functional>

#include "common/c_types_map.hpp"
#include "common/primitive.hpp"
#include "common/type_helpers.hpp"
#include "common/utils.hpp"

#include "cpu/platform.hpp"
#include "cpu/primitive_attr_postops.hpp"

#include "cpu/cpu_resampling_pd.hpp"
#include "cpu/resampling_utils.hpp"

namespace dnnl {
namespace impl {
namespace cpu {

struct simple_resampling_base_t {
    simple_resampling_base_t(const resampling_pd_t *pd) : pd_(pd) {}
    virtual ~simple_resampling_base_t() = default;

    virtual status_t init() = 0;
    virtual status_t execute(const exec_ctx_t &ctx) const = 0;

protected:
    const resampling_pd_t *pd_;

    dim_t nsp_outer_ = 0;
    dim_t stride_d_ = 0;
    dim_t stride_h_ = 0;
    dim_t stride_w_ = 0;
    dim_t inner_stride_ = 0;
};

struct simple_resampling_fwd_t : public primitive_t {
    struct pd_t : public cpu_resampling_fwd_pd_t {
        using cpu_resampling_fwd_pd_t::cpu_resampling_fwd_pd_t;

        DECLARE_COMMON_PD_T("simple:any", simple_resampling_fwd_t);

        status_t init(engine_t *engine) {
            using namespace format_tag;
            using namespace data_type;
            using sm = primitive_attr_t::skip_mask_t;

            const bool ok = is_fwd() && !has_zero_dim_memory()
                    && platform::has_data_type_support(src_md()->data_type)
                    && platform::has_data_type_support(dst_md()->data_type)
                    && set_default_params() == status::success
                    && attr()->has_default_values(
                            sm::post_ops, dst_md()->data_type)
                    && attr_.set_default_formats(dst_md(0)) == status::success;
            if (!ok) return status::unimplemented;

            format_tag_t dat_tag = memory_desc_matches_one_of_tag(*src_md(),
                    nCw8c, nChw8c, nCdhw8c, nCw16c, nChw16c, nCdhw16c, ncw,
                    nchw, ncdhw, nwc, nhwc, ndhwc);
            if (!memory_desc_matches_tag(*dst_md(), dat_tag))
                return status::unimplemented;

            return status::success;
        }
    };

    simple_resampling_fwd_t(const pd_t *apd);
    status_t init(engine_t *engine) override;
    ~simple_resampling_fwd_t() = default;

    status_t execute(const exec_ctx_t &ctx) const override;

private:
    const pd_t *pd() const { return (const pd_t *)primitive_t::pd().get(); }

    std::unique_ptr<simple_resampling_base_t> kernel_;
};

struct simple_resampling_bwd_t : public primitive_t {
    struct pd_t : public cpu_resampling_bwd_pd_t {
        using cpu_resampling_bwd_pd_t::cpu_resampling_bwd_pd_t;

        DECLARE_COMMON_PD_T("simple:any", simple_resampling_bwd_t);

        status_t init(engine_t *engine) {
            using namespace format_tag;
            using namespace data_type;
            const bool ok = !is_fwd() && !has_zero_dim_memory()
                    && platform::has_data_type_support(diff_dst_md()->data_type)
                    && platform::has_data_type_support(diff_src_md()->data_type)
                    && set_default_params() == status::success
                    && attr()->has_default_values();
            if (!ok) return status::unimplemented;

            format_tag_t dat_tag = memory_desc_matches_one_of_tag(
                    *diff_src_md(), nCw8c, nChw8c, nCdhw8c, nCw16c, nChw16c,
                    nCdhw16c, ncw, nchw, ncdhw, nwc, nhwc, ndhwc);
            if (!memory_desc_matches_tag(*diff_dst_md(), dat_tag))
                return status::unimplemented;

            return status::success;
        }
    };

    simple_resampling_bwd_t(const pd_t *apd);
    status_t init(engine_t *engine) override;
    ~simple_resampling_bwd_t() = default;

    status_t execute(const exec_ctx_t &ctx) const override;

private:
    const pd_t *pd() const { return (const pd_t *)primitive_t::pd().get(); }

    std::unique_ptr<simple_resampling_base_t> kernel_;
};

} // namespace cpu
} // namespace impl
} // namespace dnnl

#endif
