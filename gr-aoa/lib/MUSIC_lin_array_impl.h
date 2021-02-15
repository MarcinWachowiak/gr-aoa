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

#ifndef INCLUDED_BEAMFORMING_MUSIC_LIN_ARRAY_IMPL_H
#define INCLUDED_BEAMFORMING_MUSIC_LIN_ARRAY_IMPL_H

#include <aoa/MUSIC_lin_array.h>
#include <eigen3/Eigen/Dense>

namespace gr {
  namespace aoa {

    class MUSIC_lin_array_impl : public MUSIC_lin_array
    {
     private:
      float d_norm_spacing;
      int d_num_targets;
      int d_num_ant_ele;
      int d_pspectrum_len;
      float *d_theta;
      Eigen::VectorXf d_array_loc;
      Eigen::MatrixXcf d_vii_matrix;
      Eigen::MatrixXcf d_vii_matrix_trans;

     public:
      MUSIC_lin_array_impl(float norm_spacing, int num_targets, int inputs, int pspectrum_len);
      ~MUSIC_lin_array_impl();

      void amv(Eigen::VectorXcf& v_ii, Eigen::VectorXf& array_loc, float theta);

      int work(int noutput_items,
         gr_vector_const_void_star &input_items,
         gr_vector_void_star &output_items);
    };

  } // namespace aoa
} // namespace gr

#endif /* INCLUDED_BEAMFORMING_MUSIC_LIN_ARRAY_IMPL_H */

