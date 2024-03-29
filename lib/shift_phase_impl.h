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

#ifndef INCLUDED_BEAMFORMING_SHIFT_PHASE_IMPL_H
#define INCLUDED_BEAMFORMING_SHIFT_PHASE_IMPL_H

#include <gnuradio/aoa/shift_phase.h>
#include <volk/volk.h>
#include <gnuradio/math.h>

namespace gr {
  namespace aoa {

    class shift_phase_impl : public shift_phase
    {
     private:

     public:
      shift_phase_impl();
      ~shift_phase_impl();

      int work(
              int noutput_items,
              gr_vector_const_void_star &input_items,
              gr_vector_void_star &output_items
      );
    };

  } // namespace aoa
} // namespace gr

#endif /* INCLUDED_BEAMFORMING_SHIFT_PHASE_IMPL_H */

