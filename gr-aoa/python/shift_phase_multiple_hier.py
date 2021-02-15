#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021
# Marcin Wachowiak <marcin.r.wachowiak@gmail.com>
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#


from gnuradio import gr
import aoa

def gen_sig_io_two_types_symmetrical(num_elements,sig_type_st,sig_type_nd):
    # Dynamically create types for signature, two data types 
    #symmetrically filled list 
    io = []
    for i in range(int(num_elements/2)):
        io.append(sig_type_st*1)
    for j in range(int(num_elements/2)):
        io.append(sig_type_nd*1)
    return io

class shift_phase_multiple_hier(gr.hier_block2):
    """
    docstring for block shift_phase_multiple_hier
    """
    def __init__(self, num_signals=1):
        gr.hier_block2.__init__(self,
            "shift_phase_multiple_hier",
            gr.io_signaturev(2*num_signals, 2*num_signals, gen_sig_io_two_types_symmetrical(2*num_signals,gr.sizeof_gr_complex,gr.sizeof_float)),
            gr.io_signature(num_signals, num_signals, gr.sizeof_gr_complex),
        )
        ##################################################
        # Parameters
        ##################################################
        self.num_signals = num_signals
        ##################################################
        # Blocks
        ##################################################

        ##################################################
        # Connections
        ##################################################
        for p in range(num_signals):
            ## Add blocks
            # Place calc phase shift block
            object_name_m = 'shift_phase_'+str(p)
            setattr(self, object_name_m, aoa.shift_phase())

            self.connect((getattr(self,object_name_m), 0), (self, p))
            self.connect((self, p), (getattr(self,object_name_m), 0))
            self.connect((self, p+num_signals), (getattr(self,object_name_m), 1))

    def get_num_signals(self):
        return self.num_signals

    def set_num_signals(self, num_signals):
        self.num_signals = num_signals