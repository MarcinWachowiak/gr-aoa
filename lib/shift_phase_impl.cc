/* -*- c++ -*- */
/*
 *
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
#include "shift_phase_impl.h"

namespace gr {
  namespace aoa {

    shift_phase::sptr
    shift_phase::make()
    {
      return gnuradio::get_initial_sptr
        (new shift_phase_impl());
    }

    shift_phase_impl::shift_phase_impl()
      : gr::sync_block("shift_phase",
              gr::io_signature::make2(2, 2, sizeof(gr_complex), sizeof(float)),
              gr::io_signature::make(1, 1, sizeof(gr_complex)))
    {
      const int alignment_multiple = volk_get_alignment() / sizeof(gr_complex);
      set_alignment(std::max(1, alignment_multiple));
    }

    shift_phase_impl::~shift_phase_impl()
    {
    }

    int
    shift_phase_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      const gr_complex *in = (const gr_complex *) input_items[0];
      const float *coeff = (const float*) input_items[1];

      gr_complex *out = (gr_complex *) output_items[0];

      //normalize angles to complex coefficients (e^j*coeff)
      for (size_t j = 0; j < noutput_items; j++) {
        out[j] = gr_complex(cos(coeff[j]),sin(coeff[j]));
      }

      //multiply input by shift coeffs calculated from input angles
      volk_32fc_x2_multiply_32fc(out,in,out,noutput_items);

      return noutput_items;
    }

  } /* namespace aoa */
} /* namespace gr */

