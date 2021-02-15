/* -*- c++ -*- */
/*
 * Copyright 2016
 * Srikanth Pagadarai <srikanth.pagadarai@gmail.com>
 * Travis F. Collins <travisfcollins@gmail.com>
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

#ifndef INCLUDED_BEAMFORMING_CORRELATE_IMPL_H
#define INCLUDED_BEAMFORMING_CORRELATE_IMPL_H

#include <aoa/correlate.h>
#include <eigen3/Eigen/Dense>

namespace gr {
  namespace aoa {

    class correlate_impl : public correlate
    {
     private:
      const int d_num_inputs;
      const int d_snapshot_size;
      const int d_overlap_size;
      const int d_avg_method; 
      const int d_nonoverlap_size;
      // value assigned using the initialization list of the constructor
      Eigen::MatrixXcf d_J;
      Eigen::MatrixXcf d_input_matrix;

     public:
      correlate_impl(int inputs, int snapshot_size, int overlap_size, int avg_method);
      ~correlate_impl();

      int work(
              int noutput_items,
              gr_vector_const_void_star &input_items,
              gr_vector_void_star &output_items
      );
    };

  } // namespace aoa
} // namespace gr

#endif /* INCLUDED_BEAMFORMING_CORRELATE_IMPL_H */

