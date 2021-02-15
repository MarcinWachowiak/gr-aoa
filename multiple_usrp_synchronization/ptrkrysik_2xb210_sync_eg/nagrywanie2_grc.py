#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Nagrywanie2 Grc
# GNU Radio version: 3.7.14.0
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import time


class nagrywanie2_grc(gr.top_block):

    def __init__(self, decim=10, fc=690e6, file_name='output_file', gain1=20, gain2=20, gain3=20, gain4=20, if_freq=0e6, path='/home/ws', rec_len=1, samp_rate=1e6, start_time=""):
        gr.top_block.__init__(self, "Nagrywanie2 Grc")

        ##################################################
        # Parameters
        ##################################################
        self.decim = decim
        self.fc = fc
        self.file_name = file_name
        self.gain1 = gain1
        self.gain2 = gain2
        self.gain3 = gain3
        self.gain4 = gain4
        self.if_freq = if_freq
        self.path = path
        self.rec_len = rec_len
        self.samp_rate = samp_rate
        self.start_time = start_time

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0_0 = uhd.usrp_source(
        	",".join(("serial=3094E18", "master_clock_rate=10e6")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(2),
        	),
        )
        self.uhd_usrp_source_0_0.set_clock_source('external', 0)
        self.uhd_usrp_source_0_0.set_time_source('external', 0)
        self.uhd_usrp_source_0_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0_0.set_center_freq(fc, 0)
        self.uhd_usrp_source_0_0.set_gain(gain3, 0)
        self.uhd_usrp_source_0_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_source_0_0.set_bandwidth(1e6, 0)
        self.uhd_usrp_source_0_0.set_auto_dc_offset("", 0)
        self.uhd_usrp_source_0_0.set_auto_iq_balance("", 0)
        self.uhd_usrp_source_0_0.set_center_freq(fc, 1)
        self.uhd_usrp_source_0_0.set_gain(gain4, 1)
        self.uhd_usrp_source_0_0.set_antenna('RX2', 1)
        self.uhd_usrp_source_0_0.set_bandwidth(1e6, 1)
        self.uhd_usrp_source_0_0.set_auto_dc_offset("", 1)
        self.uhd_usrp_source_0_0.set_auto_iq_balance("", 1)
        (self.uhd_usrp_source_0_0).set_min_output_buffer(10000000)
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("serial=30AD33C", "master_clock_rate=10e6")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(2),
        	),
        )
        self.uhd_usrp_source_0.set_clock_source('external', 0)
        self.uhd_usrp_source_0.set_time_source('external', 0)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(fc, 0)
        self.uhd_usrp_source_0.set_gain(gain1, 0)
        self.uhd_usrp_source_0.set_antenna('RX2', 0)
        self.uhd_usrp_source_0.set_bandwidth(1e6, 0)
        self.uhd_usrp_source_0.set_auto_dc_offset("", 0)
        self.uhd_usrp_source_0.set_auto_iq_balance("", 0)
        self.uhd_usrp_source_0.set_center_freq(fc, 1)
        self.uhd_usrp_source_0.set_gain(gain2, 1)
        self.uhd_usrp_source_0.set_antenna('RX2', 1)
        self.uhd_usrp_source_0.set_bandwidth(1e6, 1)
        self.uhd_usrp_source_0.set_auto_dc_offset("", 1)
        self.uhd_usrp_source_0.set_auto_iq_balance("", 1)
        (self.uhd_usrp_source_0).set_min_output_buffer(10000000)
        self.blocks_head_0_0_1 = blocks.head(gr.sizeof_gr_complex*1, int(samp_rate*rec_len*15))
        self.blocks_head_0_0_0 = blocks.head(gr.sizeof_gr_complex*1, int(samp_rate*rec_len*15))
        self.blocks_head_0_0 = blocks.head(gr.sizeof_gr_complex*1, int(samp_rate*rec_len*15))
        self.blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, int(samp_rate*rec_len*15))
        self.blocks_file_sink_0_1 = blocks.file_sink(gr.sizeof_gr_complex*1, path+"/"+file_name+"_fc_"+str(int(fc/1e6))+"M_fs_"+str(int(samp_rate/1e6))+"M_gain_"+str(gain1)+"_start_time_"+start_time.replace(":","_").replace(" ","_")+"_ch2.sfile", False)
        self.blocks_file_sink_0_1.set_unbuffered(True)
        self.blocks_file_sink_0_0_0 = blocks.file_sink(gr.sizeof_gr_complex*1, path+"/"+file_name+"_fc_"+str(int(fc/1e6))+"M_fs_"+str(int(samp_rate/1e6))+"M_gain_"+str(gain1)+"_start_time_"+start_time.replace(":","_").replace(" ","_")+"_ch4.sfile", False)
        self.blocks_file_sink_0_0_0.set_unbuffered(True)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_gr_complex*1, path+"/"+file_name+"_fc_"+str(int(fc/1e6))+"M_fs_"+str(int(samp_rate/1e6))+"M_gain_"+str(gain1)+"_start_time_"+start_time.replace(":","_").replace(" ","_")+"_ch3.sfile", False)
        self.blocks_file_sink_0_0.set_unbuffered(True)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, path+"/"+file_name+"_fc_"+str(int(fc/1e6))+"M_fs_"+str(int(samp_rate/1e6))+"M_gain_"+str(gain1)+"_start_time_"+start_time.replace(":","_").replace(" ","_")+"_ch1.sfile", False)
        self.blocks_file_sink_0.set_unbuffered(True)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_head_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_head_0_0, 0), (self.blocks_file_sink_0_0, 0))
        self.connect((self.blocks_head_0_0_0, 0), (self.blocks_file_sink_0_1, 0))
        self.connect((self.blocks_head_0_0_1, 0), (self.blocks_file_sink_0_0_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_head_0, 0))
        self.connect((self.uhd_usrp_source_0, 1), (self.blocks_head_0_0_0, 0))
        self.connect((self.uhd_usrp_source_0_0, 0), (self.blocks_head_0_0, 0))
        self.connect((self.uhd_usrp_source_0_0, 1), (self.blocks_head_0_0_1, 0))

    def get_decim(self):
        return self.decim

    def set_decim(self, decim):
        self.decim = decim

    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc
        self.uhd_usrp_source_0_0.set_center_freq(self.fc, 0)
        self.uhd_usrp_source_0_0.set_center_freq(self.fc, 1)
        self.uhd_usrp_source_0.set_center_freq(self.fc, 0)
        self.uhd_usrp_source_0.set_center_freq(self.fc, 1)
        self.blocks_file_sink_0_1.open(self.path+"/"+self.file_name+"_fc_"+str(int(self.fc/1e6))+"M_fs_"+str(int(self.samp_rate/1e6))+"M_gain_"+str(self.gain1)+"_start_time_"+start_time.replace(":","_").replace(" ","_")+"_ch2.sfile")
        self.blocks_file_sink_0_0_0.open(self.path+"/"+self.file_name+"_fc_"+str(int(self.fc/1e6))+"M_fs_"+str(int(self.samp_rate/1e6))+"M_gain_"+str(self.gain1)+"_start_time_"+start_time.replace(":","_").replace(" ","_")+"_ch4.sfile")
        self.blocks_file_sink_0_0.open(self.path+"/"+self.file_name+"_fc_"+str(int(self.fc/1e6))+"M_fs_"+str(int(self.samp_rate/1e6))+"M_gain_"+str(self.gain1)+"_start_time_"+start_time.replace(":","_").replace(" ","_")+"_ch3.sfile")
        self.blocks_file_sink_0.open(self.path+"/"+self.file_name+"_fc_"+str(int(self.fc/1e6))+"M_fs_"+str(int(self.samp_rate/1e6))+"M_gain_"+str(self.gain1)+"_start_time_"+start_time.replace(":","_").replace(" ","_")+"_ch1.sfile")

    def get_file_name(self):
        return self.file_name

    def set_file_name(self, file_name):
        self.file_name = file_name
        self.blocks_file_sink_0_1.open(self.path+"/"+self.file_name+"_fc_"+str(int(self.fc/1e6))+"M_fs_"+str(int(self.samp_rate/1e6))+"M_gain_"+str(self.gain1)+"_start_time_"+start_time.replace(":","_").replace(" ","_")+"_ch2.sfile")
        self.blocks_file_sink_0_0_0.open(self.path+"/"+self.file_name+"_fc_"+str(int(self.fc/1e6))+"M_fs_"+str(int(self.samp_rate/1e6))+"M_gain_"+str(self.gain1)+"_start_time_"+start_time.replace(":","_").replace(" ","_")+"_ch4.sfile")
        self.blocks_file_sink_0_0.open(self.path+"/"+self.file_name+"_fc_"+str(int(self.fc/1e6))+"M_fs_"+str(int(self.samp_rate/1e6))+"M_gain_"+str(self.gain1)+"_start_time_"+start_time.replace(":","_").replace(" ","_")+"_ch3.sfile")
        self.blocks_file_sink_0.open(self.path+"/"+self.file_name+"_fc_"+str(int(self.fc/1e6))+"M_fs_"+str(int(self.samp_rate/1e6))+"M_gain_"+str(self.gain1)+"_start_time_"+start_time.replace(":","_").replace(" ","_")+"_ch1.sfile")

    def get_gain1(self):
        return self.gain1

    def set_gain1(self, gain1):
        self.gain1 = gain1
        self.uhd_usrp_source_0.set_gain(self.gain1, 0)

        self.blocks_file_sink_0_1.open(self.path+"/"+self.file_name+"_fc_"+str(int(self.fc/1e6))+"M_fs_"+str(int(self.samp_rate/1e6))+"M_gain_"+str(self.gain1)+"_start_time_"+start_time.replace(":","_").replace(" ","_")+"_ch2.sfile")
        self.blocks_file_sink_0_0_0.open(self.path+"/"+self.file_name+"_fc_"+str(int(self.fc/1e6))+"M_fs_"+str(int(self.samp_rate/1e6))+"M_gain_"+str(self.gain1)+"_start_time_"+start_time.replace(":","_").replace(" ","_")+"_ch4.sfile")
        self.blocks_file_sink_0_0.open(self.path+"/"+self.file_name+"_fc_"+str(int(self.fc/1e6))+"M_fs_"+str(int(self.samp_rate/1e6))+"M_gain_"+str(self.gain1)+"_start_time_"+start_time.replace(":","_").replace(" ","_")+"_ch3.sfile")
        self.blocks_file_sink_0.open(self.path+"/"+self.file_name+"_fc_"+str(int(self.fc/1e6))+"M_fs_"+str(int(self.samp_rate/1e6))+"M_gain_"+str(self.gain1)+"_start_time_"+start_time.replace(":","_").replace(" ","_")+"_ch1.sfile")

    def get_gain2(self):
        return self.gain2

    def set_gain2(self, gain2):
        self.gain2 = gain2
        self.uhd_usrp_source_0.set_gain(self.gain2, 1)


    def get_gain3(self):
        return self.gain3

    def set_gain3(self, gain3):
        self.gain3 = gain3
        self.uhd_usrp_source_0_0.set_gain(self.gain3, 0)


    def get_gain4(self):
        return self.gain4

    def set_gain4(self, gain4):
        self.gain4 = gain4
        self.uhd_usrp_source_0_0.set_gain(self.gain4, 1)


    def get_if_freq(self):
        return self.if_freq

    def set_if_freq(self, if_freq):
        self.if_freq = if_freq

    def get_path(self):
        return self.path

    def set_path(self, path):
        self.path = path
        self.blocks_file_sink_0_1.open(self.path+"/"+self.file_name+"_fc_"+str(int(self.fc/1e6))+"M_fs_"+str(int(self.samp_rate/1e6))+"M_gain_"+str(self.gain1)+"_start_time_"+start_time.replace(":","_").replace(" ","_")+"_ch2.sfile")
        self.blocks_file_sink_0_0_0.open(self.path+"/"+self.file_name+"_fc_"+str(int(self.fc/1e6))+"M_fs_"+str(int(self.samp_rate/1e6))+"M_gain_"+str(self.gain1)+"_start_time_"+start_time.replace(":","_").replace(" ","_")+"_ch4.sfile")
        self.blocks_file_sink_0_0.open(self.path+"/"+self.file_name+"_fc_"+str(int(self.fc/1e6))+"M_fs_"+str(int(self.samp_rate/1e6))+"M_gain_"+str(self.gain1)+"_start_time_"+start_time.replace(":","_").replace(" ","_")+"_ch3.sfile")
        self.blocks_file_sink_0.open(self.path+"/"+self.file_name+"_fc_"+str(int(self.fc/1e6))+"M_fs_"+str(int(self.samp_rate/1e6))+"M_gain_"+str(self.gain1)+"_start_time_"+start_time.replace(":","_").replace(" ","_")+"_ch1.sfile")

    def get_rec_len(self):
        return self.rec_len

    def set_rec_len(self, rec_len):
        self.rec_len = rec_len
        self.blocks_head_0_0_1.set_length(int(self.samp_rate*self.rec_len*15))
        self.blocks_head_0_0_0.set_length(int(self.samp_rate*self.rec_len*15))
        self.blocks_head_0_0.set_length(int(self.samp_rate*self.rec_len*15))
        self.blocks_head_0.set_length(int(self.samp_rate*self.rec_len*15))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source_0_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.blocks_head_0_0_1.set_length(int(self.samp_rate*self.rec_len*15))
        self.blocks_head_0_0_0.set_length(int(self.samp_rate*self.rec_len*15))
        self.blocks_head_0_0.set_length(int(self.samp_rate*self.rec_len*15))
        self.blocks_head_0.set_length(int(self.samp_rate*self.rec_len*15))
        self.blocks_file_sink_0_1.open(self.path+"/"+self.file_name+"_fc_"+str(int(self.fc/1e6))+"M_fs_"+str(int(self.samp_rate/1e6))+"M_gain_"+str(self.gain1)+"_start_time_"+start_time.replace(":","_").replace(" ","_")+"_ch2.sfile")
        self.blocks_file_sink_0_0_0.open(self.path+"/"+self.file_name+"_fc_"+str(int(self.fc/1e6))+"M_fs_"+str(int(self.samp_rate/1e6))+"M_gain_"+str(self.gain1)+"_start_time_"+start_time.replace(":","_").replace(" ","_")+"_ch4.sfile")
        self.blocks_file_sink_0_0.open(self.path+"/"+self.file_name+"_fc_"+str(int(self.fc/1e6))+"M_fs_"+str(int(self.samp_rate/1e6))+"M_gain_"+str(self.gain1)+"_start_time_"+start_time.replace(":","_").replace(" ","_")+"_ch3.sfile")
        self.blocks_file_sink_0.open(self.path+"/"+self.file_name+"_fc_"+str(int(self.fc/1e6))+"M_fs_"+str(int(self.samp_rate/1e6))+"M_gain_"+str(self.gain1)+"_start_time_"+start_time.replace(":","_").replace(" ","_")+"_ch1.sfile")

    def get_start_time(self):
        return self.start_time

    def set_start_time(self, start_time):
        self.start_time = start_time


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "-d", "--decim", dest="decim", type="intx", default=10,
        help="Set decim [default=%default]")
    parser.add_option(
        "-f", "--fc", dest="fc", type="eng_float", default=eng_notation.num_to_str(690e6),
        help="Set fc [default=%default]")
    parser.add_option(
        "-o", "--file-name", dest="file_name", type="string", default='output_file',
        help="Set output_file [default=%default]")
    parser.add_option(
        "", "--gain1", dest="gain1", type="eng_float", default=eng_notation.num_to_str(20),
        help="Set gain1 [default=%default]")
    parser.add_option(
        "", "--gain2", dest="gain2", type="eng_float", default=eng_notation.num_to_str(20),
        help="Set gain2 [default=%default]")
    parser.add_option(
        "", "--gain3", dest="gain3", type="eng_float", default=eng_notation.num_to_str(20),
        help="Set gain3 [default=%default]")
    parser.add_option(
        "", "--gain4", dest="gain4", type="eng_float", default=eng_notation.num_to_str(20),
        help="Set gain4 [default=%default]")
    parser.add_option(
        "-l", "--if-freq", dest="if_freq", type="eng_float", default=eng_notation.num_to_str(0e6),
        help="Set if_freq [default=%default]")
    parser.add_option(
        "-p", "--path", dest="path", type="string", default='/home/ws',
        help="Set /home/ws [default=%default]")
    parser.add_option(
        "-T", "--rec-len", dest="rec_len", type="eng_float", default=eng_notation.num_to_str(1),
        help="Set rec_len [default=%default]")
    parser.add_option(
        "", "--samp-rate", dest="samp_rate", type="eng_float", default=eng_notation.num_to_str(1e6),
        help="Set samp_rate [default=%default]")
    parser.add_option(
        "-s", "--start-time", dest="start_time", type="string", default="",
        help="Set start_time [default=%default]")
    return parser


def main(top_block_cls=nagrywanie2_grc, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(decim=options.decim, fc=options.fc, file_name=options.file_name, gain1=options.gain1, gain2=options.gain2, gain3=options.gain3, gain4=options.gain4, if_freq=options.if_freq, path=options.path, rec_len=options.rec_len, samp_rate=options.samp_rate, start_time=options.start_time)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
