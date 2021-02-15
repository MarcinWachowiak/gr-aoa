#import threading 
from gui_and_save_usrp_source_synchronized_2xB210_grc import *
import time
import datetime
import thread

class sync_gui_and_save_usrp_source_synchronized_2xB210_grc(gui_and_save_usrp_source_synchronized_2xB210_grc):
    def __init__(self, decim=10, fc=690e6, file_name="output_file", gain1=30, gain2=30, if_freq=0e6, path="/home/ws", samp_rate=1e6, start_time="", rec_len=1, gain3=30, gain4=30):
        super(nagrywanie2, self).__init__(decim=decim, fc=fc, file_name=file_name, gain1=gain1, gain2=gain2, if_freq=if_freq, path=path, samp_rate=samp_rate, start_time=start_time, rec_len=rec_len, gain3=gain3, gain4=gain4)
        
        self.set_time_unknown_pps_costam(uhd.time_spec(0.0))

        self.uhd_usrp_source_0.set_start_time(uhd.time_spec(3.0))
        self.uhd_usrp_source_0_0.set_start_time(uhd.time_spec(3.0))

    def set_time_unknown_pps_costam(self, time_spec):
        time_last_pps = self.uhd_usrp_source_0.get_time_last_pps()
        while(self.uhd_usrp_source_0.get_time_last_pps() == time_last_pps):
            time.sleep(0.01)
        self.uhd_usrp_source_0.set_time_next_pps(time_spec)
        self.uhd_usrp_source_0_0.set_time_next_pps(time_spec)

        time_last_pps = self.uhd_usrp_source_0.get_time_last_pps()
        while(self.uhd_usrp_source_0.get_time_last_pps() == time_last_pps):
            time.sleep(0.01)

        print self.uhd_usrp_source_0.get_time_now().get_real_secs()
        print self.uhd_usrp_source_0_0.get_time_now().get_real_secs()

if __name__ == '__main__':
    main(top_block_cls=nagrywanie2)
