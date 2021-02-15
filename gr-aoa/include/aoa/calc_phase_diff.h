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

#ifndef INCLUDED_BEAMFORMING_CALC_PHASE_DIFF_H
#define INCLUDED_BEAMFORMING_CALC_PHASE_DIFF_H

#include <aoa/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace aoa {

    /*!
     * \brief <+description of block+>
     * \ingroup aoa
     *
     */
    class BEAMFORMING_API calc_phase_diff : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<calc_phase_diff> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of aoa::calc_phase_diff.
       *
       * To avoid accidental use of raw pointers, aoa::calc_phase_diff's
       * constructor is in a private implementation
       * class. aoa::calc_phase_diff::make is the public interface for
       * creating new instances.
       */
      static sptr make(int node_idx, float norm_spacing);
    };

  } // namespace aoa
} // namespace gr

#endif /* INCLUDED_BEAMFORMING_CALC_PHASE_DIFF_H */

