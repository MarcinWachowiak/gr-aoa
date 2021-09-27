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

#ifndef INCLUDED_BEAMFORMING_PRECISE_MOVING_AVERAGE_IMPL_H
#define INCLUDED_BEAMFORMING_PRECISE_MOVING_AVERAGE_IMPL_H

#include <aoa/precise_moving_average.h>
#include <algorithm>
#include <vector>

namespace gr {
  namespace aoa {

    class precise_moving_average_impl : public precise_moving_average
    {
      private:
        int d_length;
        double d_scale;
        int d_max_iter;

     public:
      precise_moving_average_impl(int length, int max_iter = 4096);
      ~precise_moving_average_impl();

      int work(
              int noutput_items,
              gr_vector_const_void_star &input_items,
              gr_vector_void_star &output_items
      );
    };

  } // namespace aoa
} // namespace gr

#endif /* INCLUDED_BEAMFORMING_PRECISE_MOVING_AVERAGE_IMPL_H */

