/* -*- c++ -*- */
/*
 * Copyright 2021
 * Marcin Wachowiak <marcin.r.wachowiak@gmail.com>
 *
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "calc_phase_diff_impl.h"

namespace gr {
  namespace aoa {

    calc_phase_diff::sptr
    calc_phase_diff::make(int node_idx, float norm_spacing)
    {
      return gnuradio::get_initial_sptr
        (new calc_phase_diff_impl(node_idx, norm_spacing));
    }

    calc_phase_diff_impl::calc_phase_diff_impl(int node_idx,float norm_spacing)
      : gr::sync_block("calc_phase_diff",
              gr::io_signature::make(2, 2, sizeof(gr_complex)),
              gr::io_signature::make(1, 1, sizeof(float))),
              d_node_idx(node_idx),
              d_norm_spacing(norm_spacing)
    {
      const int alignment_multiple = volk_get_alignment() / sizeof(gr_complex);
      set_alignment(std::max(1, alignment_multiple));

      //calc constant position diff coeff
      d_loc_shift_coeff = exp(gr_complex(0.0,1.0)*(float)(2*M_PI*d_norm_spacing*d_node_idx));
    }

    calc_phase_diff_impl::~calc_phase_diff_impl()
    {
    }

    int
    calc_phase_diff_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      const gr_complex *ref = (const gr_complex *) input_items[0];
      const gr_complex *in = (const gr_complex *) input_items[1];
      float *out = (float *) output_items[0];
      
      //buffer pointer
      gr_complex *buffer = (gr_complex*) volk_malloc(noutput_items*sizeof(gr_complex),volk_get_alignment());
      //location based phase diff coefficient
      //multiply conjungate of second signal with ref signal
      volk_32fc_x2_multiply_conjugate_32fc(buffer, ref, in, noutput_items);
      
      //correct by constant location phase diff coefficient
      volk_32fc_s32fc_multiply_32fc(buffer, buffer, d_loc_shift_coeff, noutput_items);
      
      for (size_t j = 0; j < noutput_items; j++) {
        //calc arg
        out[j] = fast_atan2f(buffer[j]);
      }

      volk_free(buffer);
      return noutput_items;
    }


  } /* namespace aoa */
} /* namespace gr */

