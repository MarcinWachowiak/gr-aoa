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
#include "rootMUSIC_linear_array_impl.h"

namespace Eigen {
namespace Vector {
template <class T>
inline void push_back(Eigen::Matrix<T,Eigen::Dynamic,1>& v, const T d) {
  Eigen::Matrix<T,Eigen::Dynamic,1> tmp = v;
  v.conservativeResize(tmp.size() + 1);
  v.head(tmp.size()) = tmp;
  v[v.size()-1] = d;
}
} // namespace Vector
} // namespace Eigen

namespace gr {
  namespace aoa {

    rootMUSIC_linear_array::sptr
    rootMUSIC_linear_array::make(float norm_spacing, int num_targets, int num_ant_ele)
    {
      return gnuradio::get_initial_sptr
        (new rootMUSIC_linear_array_impl(norm_spacing, num_targets, num_ant_ele));
    }

    rootMUSIC_linear_array_impl::rootMUSIC_linear_array_impl(float norm_spacing, int num_targets, int num_ant_ele)
      : gr::sync_block("rootMUSIC_linear_array",
              gr::io_signature::make(1, 1, sizeof(gr_complex)*num_ant_ele*num_ant_ele),
              gr::io_signature::make(1, num_targets, num_targets*sizeof(float))),
	      d_norm_spacing(norm_spacing),
	      d_num_targets(num_targets),
	      d_num_ant_ele(num_ant_ele)
    {
      // initialization of the Frobenius companion matrix
      d_comp_mat = Eigen::MatrixXcf(2*d_num_ant_ele-2, 2*d_num_ant_ele-2).setZero();
      // set the first sub-diagonal to all-ones
      d_comp_mat.diagonal(-1).setOnes();

    }

    rootMUSIC_linear_array_impl::~rootMUSIC_linear_array_impl()
    {
    }

    void 
    rootMUSIC_linear_array_impl::get_roots_polynomial(Eigen::MatrixXcf& A, Eigen::VectorXcf& roots) 
    {
      Eigen::VectorXcf u(2*d_num_ant_ele-1);

      // determine the polynomial vector and normalize it
      for (int ii = -d_num_ant_ele+1; ii < 0; ii++) 
      {
	u(ii+d_num_ant_ele-1) =A.diagonal(ii).sum();
	u(d_num_ant_ele-1-ii) = conj(u(ii+d_num_ant_ele-1)); 
      }
      u(d_num_ant_ele-1) = A.diagonal().sum();
      u = (gr_complex(-1.0, 0.0)/u(2*d_num_ant_ele-2))*u;

      // assign u to the last-column of the Frobenius companion matrix
      d_comp_mat.col(2*d_num_ant_ele-3) = u.topRows(2*d_num_ant_ele-3);

      // determine its EVD to get roots of the polynomial vector

      Eigen::ComplexEigenSolver<Eigen::MatrixXcf> complex_eigensolver(d_comp_mat);
      roots = complex_eigensolver.eigenvalues();   
      }

    int
    rootMUSIC_linear_array_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      const gr_complex *in = (const gr_complex *) input_items[0];
      float *out = (float *) output_items[0];
      // process each input vector (Rxx matrix)
      Eigen::MatrixXcf eig_vec;
      Eigen::VectorXcf eigval_roots;
      Eigen::VectorXf dist;

      Eigen::VectorXcf eigval_roots_inside;
      Eigen::VectorXf  dist_inside;

      for (int item = 0; item < noutput_items; item++)
      {
          // make input pointer into matrix pointer;
          Eigen::Map<Eigen::MatrixXcf> in_matrix((gr_complex*)in+item*d_num_ant_ele*d_num_ant_ele, d_num_ant_ele, d_num_ant_ele);
          
          Eigen::Map<Eigen::VectorXf> out_vec(out+item*d_num_targets, d_num_targets);

          // determine EVD of the auto-correlation matrix
          Eigen::SelfAdjointEigenSolver<Eigen::MatrixXcf> hermitian_eigensolver(in_matrix);
          eig_vec = hermitian_eigensolver.eigenvectors();

          // noise subspace and its square matrix
          Eigen::MatrixXcf U_N = eig_vec.leftCols(d_num_ant_ele-d_num_targets);
          Eigen::MatrixXcf U_N_sq = U_N*U_N.adjoint();

        // determine the roots of the polynomial generated using U_N_sq
        get_roots_polynomial(U_N_sq, eigval_roots);

        // distance of the roots w.r.t from unit circle
        dist = 1.0-eigval_roots.array().abs();
      
        dist_inside.resize(0);
        eigval_roots_inside.resize(0);
      
        for(Eigen::Index i=0; i<dist.size(); ++i) {
          if(dist(i) > 0.0){
              Eigen::Vector::push_back<float>(dist_inside,dist(i));
              Eigen::Vector::push_back<gr_complex>(eigval_roots_inside,eigval_roots(i));
          } else {
            //do nothing - skip
          }
        }
    
        //corner case when solutions are outside of unit circle (when sources have the same angle or there are less visible sources than required)
        //some of the results are correct and it prevents runtime crashes
        if(dist_inside.size() == 0 || dist_inside.size()<d_num_targets) {
          dist = dist.array().abs();
          Eigen::Index min_dist_fill_idx;
          while((d_num_targets-dist_inside.size()) != 0) {
              //pick root closes to unity circle, even outside to prevent crashes
              dist.minCoeff(&min_dist_fill_idx);
              Eigen::Vector::push_back<float>(dist_inside,dist(min_dist_fill_idx));
              Eigen::Vector::push_back<gr_complex>(eigval_roots_inside,eigval_roots(min_dist_fill_idx));
          }
        }

        Eigen::VectorXf aoa_vec(d_num_targets);
        Eigen::Index min_dist_idx;
        for (int ii = 0; ii < d_num_targets; ii++) 
        {
          //find the roots that are closest to the unit circle
          dist_inside.minCoeff(&min_dist_idx);
          // locate the root and convert it to correct form
          aoa_vec(ii) = 180.0*acos(arg(eigval_roots_inside(min_dist_idx))/(2*EIGEN_PI*d_norm_spacing))/EIGEN_PI;
          // discard this minimum to find the next minimum
          dist_inside(min_dist_idx) = float(INFINITY);
          eigval_roots_inside(min_dist_idx) = gr_complex(float(INFINITY), 0.0);
        }
        // sort the AoA vector
        // useful for display purposes
        std::sort(aoa_vec.data(),aoa_vec.data()+aoa_vec.size());
    
        memcpy((char *)&(out[item*d_num_targets]), (const char *)aoa_vec.col(0).data(), d_num_targets*sizeof(float));
      }
      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace aoa */
} /* namespace gr */

