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

#ifndef INCLUDED_BEAMFORMING_HEAD_W_RST_IMPL_H
#define INCLUDED_BEAMFORMING_HEAD_W_RST_IMPL_H

#include <aoa/head_w_rst.h>

namespace gr {
  namespace aoa {

    class head_w_rst_impl : public head_w_rst
    {
     private:
      uint64_t d_nitems;
      uint64_t d_ncopied_items;
      bool d_dump_buff;
      pmt::pmt_t status_port;
      int8_t status_num;
     public:
      head_w_rst_impl(size_t sizeof_stream_item, uint64_t nitems);
      ~head_w_rst_impl();
      
      void reset(bool dump_buff);
      void set_length(uint64_t nitems) { d_nitems = nitems; }

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);

    };

  } // namespace aoa
} // namespace gr

#endif /* INCLUDED_BEAMFORMING_HEAD_W_RST_IMPL_H */

