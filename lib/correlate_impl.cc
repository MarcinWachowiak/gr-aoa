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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "correlate_impl.h"

namespace gr {
  namespace aoa {

    correlate::sptr
    correlate::make(int inputs, int snapshot_size, int overlap_size, int avg_method)
    {
      return gnuradio::get_initial_sptr
        (new correlate_impl(inputs, snapshot_size, overlap_size, avg_method));
    }

    correlate_impl::correlate_impl(int inputs, int snapshot_size, int overlap_size, int avg_method)
      : gr::sync_decimator("correlate",
              gr::io_signature::make(inputs, inputs, sizeof(gr_complex)),
              gr::io_signature::make(1, 1, sizeof(gr_complex)*inputs*inputs), (snapshot_size-overlap_size)),
        d_num_inputs(inputs),
        d_snapshot_size(snapshot_size),
        d_overlap_size(overlap_size),
        d_avg_method(avg_method),
        d_nonoverlap_size(snapshot_size-overlap_size)

    {
      set_history(d_overlap_size+1);

      // Create container for temporary matrix
      d_input_matrix = Eigen::MatrixXcf(d_snapshot_size,d_num_inputs);

      // initialize the reflection matrix
      d_J = Eigen::MatrixXf::Identity(d_num_inputs, d_num_inputs);
      d_J = d_J.reverse();
    }

    correlate_impl::~correlate_impl()
    {
    }

    int
    correlate_impl::work(int output_matrices,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
     // Cast pointer
      gr_complex *out = (gr_complex *) output_items[0];

      // Create each output matrix
      for (int i=0; i<output_matrices; i++)
      {
        // Form input matrix
        for(int k=0; k<d_num_inputs; k++) 
        {
            memcpy((void*)d_input_matrix.col(k).data(),
            ((gr_complex*)input_items[k]+i*d_nonoverlap_size),
            sizeof(gr_complex)*d_snapshot_size);
        }
        // Make output pointer into matrix pointer
        Eigen::Map<Eigen::MatrixXcf> out_matrix(out+d_num_inputs*d_num_inputs*i,d_num_inputs,d_num_inputs);
        
        // Do autocorrelation
        out_matrix = (1.0/d_snapshot_size)*d_input_matrix.transpose()*d_input_matrix.conjugate();

        if (d_avg_method == 1){
          out_matrix = 0.5*out_matrix+(0.5/d_snapshot_size)*d_J*out_matrix.conjugate()*d_J;
        }
      }

      // Tell runtime system how many output items we produced.
      return (output_matrices);
    }
  } /* namespace aoa */
} /* namespace gr */

