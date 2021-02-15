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

#ifndef INCLUDED_BEAMFORMING_HEAD_W_RST_H
#define INCLUDED_BEAMFORMING_HEAD_W_RST_H

#include <aoa/api.h>
#include <gnuradio/block.h>
#include <stddef.h> // size_t

namespace gr {
  namespace aoa {

    /*!
     * \brief copies the first N items to the output, then waits for reset
     * \ingroup aoa
     *
     */
    class BEAMFORMING_API head_w_rst : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<head_w_rst> sptr;

      static sptr make(size_t sizeof_stream_item, uint64_t nitems);

      virtual void reset(bool dump_buff) = 0;
      virtual void set_length(uint64_t nitems) = 0;
    };

  } // namespace aoa
} // namespace gr

#endif /* INCLUDED_BEAMFORMING_HEAD_W_RST_H */

