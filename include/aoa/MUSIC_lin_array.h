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

#ifndef INCLUDED_BEAMFORMING_MUSIC_LIN_ARRAY_H
#define INCLUDED_BEAMFORMING_MUSIC_LIN_ARRAY_H

#include <aoa/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace aoa {

    /*!
     * \brief Performs DoA estimation using MUSIC algorithm for a linear antenna array. 
     * \ingroup doa
     * 
     * \details
     * This block takes a correlation matrix of size (number of antenna elements x number of antenna elements) 
     * as input and generates a complex vector of size (pseudo-spectrum length x 1) 
     * whose arg-max values represent the estimated DoAs. 
     *
     */
    class BEAMFORMING_API MUSIC_lin_array : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<MUSIC_lin_array> sptr;

      /*!
       * \brief Make a block to estimate DoAs using MUSIC algorithm for linear arrays.
       *
       * \param norm_spacing    Normalized spacing between antenna elements
       * \param num_targets     Known number of targets 
       * \param num_ant_ele     Number of antenna elements
       * \param pspectrum_len   Length of the Pseudo-Spectrum length
       */
      static sptr make(float norm_spacing, int num_targets, int num_ant_ele, int pspectrum_len);
    };

  } // namespace aoa
} // namespace gr

#endif /* INCLUDED_BEAMFORMING_MUSIC_LIN_ARRAY_H */

