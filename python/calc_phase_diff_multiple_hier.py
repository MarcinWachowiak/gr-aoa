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

class calc_phase_diff_multiple_hier(gr.hier_block2):
    """
    docstring for block calc_phase_diff_multiple_hier
    """
    def __init__(self, num_signals=1, norm_spacing=0.5):
        gr.hier_block2.__init__(
            self, "calc_phase_diff_multiple_hier",
                gr.io_signature(num_signals+1, num_signals+1, gr.sizeof_gr_complex),
                gr.io_signature(num_signals, num_signals, gr.sizeof_float),
        )
        ##################################################
        # Parameters
        ##################################################
        self.num_signals = num_signals
        self.norm_spacing = norm_spacing
        ##################################################
        # Blocks
        ##################################################

        ##################################################
        # Connections
        ##################################################
        for p in range(num_signals):
            ## Add blocks
            # Place calc phase shift block
            object_name_m = 'calc_phase_diff_'+str(p)
            setattr(self, object_name_m, aoa.calc_phase_diff(p+1,self.norm_spacing))

            self.connect((getattr(self,object_name_m), 0), (self, p))
            self.connect((self, 0), (getattr(self,object_name_m), 0))
            self.connect((self, p+1), (getattr(self,object_name_m), 1))
           
           
    def get_num_signals(self):
        return self.num_signals

    def set_num_signals(self, num_signals):
        self.num_signals = num_signals

    def get_norm_spacing(self):
        return self.norm_spacing

    def set_norm_spacing(self, norm_spacing):
        self.norm_spacing = norm_spacing
