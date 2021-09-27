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

#ifndef INCLUDED_BEAMFORMING_CORRELATE_H
#define INCLUDED_BEAMFORMING_CORRELATE_H

#include <aoa/api.h>
#include <gnuradio/sync_decimator.h>

namespace gr {
  namespace aoa {

    /*!
     * \brief Calculate autocorrelation matrix of input data snapshot
     * \ingroup AoA
     *
     */
    class BEAMFORMING_API correlate : virtual public gr::sync_decimator
    {
     public:
      typedef boost::shared_ptr<correlate> sptr;

      /*!
       * \brief Make an correlate block.
       * 
       * \param inputs          Number of input streams
       * \param snapshot_size   Size of each snapshot
       * \param overlap_size    Size of the overlap between successive snapshots
       * \param avg_method      Use Forward Averaging or Forward-Backward Averaging
       */
      static sptr make(int inputs, int snapshot_size, int overlap_size, int avg_method);
    };

  } // namespace aoa
} // namespace gr

#endif /* INCLUDED_BEAMFORMING_CORRELATE_H */

