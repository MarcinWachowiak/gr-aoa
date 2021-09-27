/* -*- c++ -*- */
/*
 * Copyright 2020
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

#ifndef INCLUDED_BEAMFORMING_PRECISE_MOVING_AVERAGE_H
#define INCLUDED_BEAMFORMING_PRECISE_MOVING_AVERAGE_H

#include <aoa/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace aoa {

    /*!
     * \brief output is the moving sum of the last N samples, scaled by the scale factor
     * \ingroup aoa
     *
     */
    class BEAMFORMING_API precise_moving_average : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<precise_moving_average> sptr;

      /*!
     * Create a moving average block.
     *
     * \param length Number of samples to use in the average.
     * \param max_iter limits how long we go without flushing the accumulator
     * This is necessary to avoid numerical instability for float and complex.
     */
      static sptr make(int length, int max_iter = 4096);
    };

  } // namespace aoa
} // namespace gr

#endif /* INCLUDED_BEAMFORMING_PRECISE_MOVING_AVERAGE_H */

