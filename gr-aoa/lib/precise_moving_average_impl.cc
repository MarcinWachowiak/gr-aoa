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
#include "precise_moving_average_impl.h"

namespace gr {
  namespace aoa {

    precise_moving_average::sptr
    precise_moving_average::make(int length, int max_iter)
    {
      return gnuradio::get_initial_sptr
        (new precise_moving_average_impl(length, max_iter));
    }

    precise_moving_average_impl::precise_moving_average_impl(int length,
                                                     int max_iter)
      : gr::sync_block("precise_moving_average",
              gr::io_signature::make(1, 1, sizeof(float)),
              gr::io_signature::make(1, 1, sizeof(float))),
      d_length(length),
      d_max_iter(max_iter)
    {
      d_scale = static_cast<double>(1.0/length);
      this->set_history(length);
    }

    precise_moving_average_impl::~precise_moving_average_impl()
    {
    }

    int
    precise_moving_average_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      const float *in = (const float *) input_items[0];
      float *out = (float *) output_items[0];

      unsigned int num_iter = (unsigned int)((noutput_items > d_max_iter) ? d_max_iter : noutput_items);
        double sum = in[0];
        for (int i = 1; i < d_length - 1; i++) {
            sum += in[i];
        }

        for (unsigned int i = 0; i < num_iter; i++) {
            sum += in[i + d_length - 1];
            out[i] = sum * d_scale;
            sum -= in[i];
        }

      return noutput_items;
    }
  } /* namespace aoa */
} /* namespace gr */

