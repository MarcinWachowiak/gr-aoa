#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.8.1.0

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import pdu_utils
import pmt


class message_usrp_sync_timed_commands_test(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet")

        ##################################################
        # Variables
        ##################################################
        self.trigger_cmd = trigger_cmd = gr.tag_utils.python_to_tag((0, pmt.intern("TRIGGER"), pmt.PMT_T, pmt.intern("src")))
        self.samp_rate = samp_rate = 10000
        self.cmd_msg = cmd_msg = pmt.to_pmt({'lo_offset': 100})

        ##################################################
        # Blocks
        ##################################################
        self.pdu_utils_tag_message_trigger_0 = pdu_utils.tag_message_trigger_b(pmt.intern("TRIGGER"), pmt.PMT_NIL, cmd_msg, 0, samp_rate, 0.0, 5, False)
        self.blocks_vector_source_x_0_0 = blocks.vector_source_b((0,0), False, 1, [trigger_cmd])
        self.blocks_throttle_0_0 = blocks.throttle(gr.sizeof_char*1, samp_rate,True)
        self.blocks_message_debug_0 = blocks.message_debug()
        self.blocks_delay_0 = blocks.delay(gr.sizeof_char*1, 5*samp_rate)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.pdu_utils_tag_message_trigger_0, 'msg'), (self.blocks_message_debug_0, 'print'))
        self.connect((self.blocks_delay_0, 0), (self.blocks_throttle_0_0, 0))
        self.connect((self.blocks_throttle_0_0, 0), (self.pdu_utils_tag_message_trigger_0, 0))
        self.connect((self.blocks_vector_source_x_0_0, 0), (self.blocks_delay_0, 0))


    def get_trigger_cmd(self):
        return self.trigger_cmd

    def set_trigger_cmd(self, trigger_cmd):
        self.trigger_cmd = trigger_cmd
        self.blocks_vector_source_x_0_0.set_data((0,0), [self.trigger_cmd])

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_delay_0.set_dly(5*self.samp_rate)
        self.blocks_throttle_0_0.set_sample_rate(self.samp_rate)
        self.pdu_utils_tag_message_trigger_0.set_sample_rate(self.samp_rate)

    def get_cmd_msg(self):
        return self.cmd_msg

    def set_cmd_msg(self, cmd_msg):
        self.cmd_msg = cmd_msg
        self.pdu_utils_tag_message_trigger_0.set_message(self.cmd_msg)





def main(top_block_cls=message_usrp_sync_timed_commands_test, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
