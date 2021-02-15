#import threading 
from run_usrp_b201_2xRX_save_sampl_to_file import *
import time
import _thread
import uhd

class sync_topper(run_usrp_b201_2xRX_save_sampl_to_file):
    def __init__(self, center_frequency=2.4e9, chan_bandwidth=1e6, gain_rx_1=20, gain_rx_2=20, samp_rate=1e6):
        super(sync_topper, self).__init__(center_frequency=center_frequency, chan_bandwidth=chan_bandwidth, gain_rx_1=gain_rx_1, gain_rx_2=gain_rx_2, samp_rate=samp_rate)
        
        #recent approach
        #print("setting time on pps!")
        #self.set_time_on_pps()
        #print("done!")

        print("synced retune!")
        self.sync_retune(center_frequency)
        #probably obsolete
        print("done!")

        print("Start streaming!")
        #self.start_sync_streaming_old()
        self.start_sync_streaming()
        print("done!")
        #old approach
        #self.set_time_on_pps_old(uhd.time_spec(0.0))

    def start_rx_stream(self,streamer, start_time):
        """
        Kick off the RX streamer
        """
        stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.start_cont)
        stream_cmd.stream_now = False
        stream_cmd.time_spec = start_time
        streamer.issue_stream_cmd(stream_cmd)
        
    def get_rx_streamers(self,usrp):
        """
        Return a streamer
        """
        st_args = uhd.usrp.StreamArgs("fc32", "sc16")
        st_args.channels = [0,1]
        return usrp.get_rx_stream(st_args)

    def set_time_on_pps(self):

        self.uhd_usrp_source_0.set_time_next_pps.time_spec(0.0)
        time.sleep(1.0)
        #additional/optional printing
        print (self.uhd_usrp_source_0.get_time_now().get_real_secs())

    def set_time_on_pps_old(self, time_spec):
        time_last_pps = self.uhd_usrp_source_0.get_time_last_pps()
        while(self.uhd_usrp_source_0.get_time_last_pps() == time_last_pps):
            time.sleep(0.01)
        self.uhd_usrp_source_0.set_time_next_pps(time_spec)

        time_last_pps = self.uhd_usrp_source_0.get_time_last_pps()
        
        while(self.uhd_usrp_source_0.get_time_last_pps() == time_last_pps):
            time.sleep(0.01)

        print (self.uhd_usrp_source_0.get_time_now())

        print (self.uhd_usrp_source_0.get_time_now().get_real_secs())
        #add more time printing? 
    
    def sync_retune(self, center_freq):

        cmd_delay = uhd.types.TimeSpec(0.5)
        self.uhd_usrp_source_0.clear_command_time()
        shared_curr_time = self.uhd_usrp_source_0.get_time_now()
        self.uhd_usrp_source_0.set_command_time(cmd_delay+shared_curr_time)

        tune_req = uhd.types.TuneRequest(center_freq)
        self.uhd_usrp_source_0.set_rx_freq(tune_req, 0)
        self.uhd_usrp_source_0.set_rx_freq(tune_req, 1)

        self.uhd_usrp_source_0.clear_command_time()

    def start_sync_streaming (self):
        rx_streamer = get_rx_streamer(self.uhd_usrp_source_0, args.channel)
        start_rx_stream(rx_streamer,uhd.time_spec(0.1))


if __name__ == '__main__':
    main(top_block_cls=sync_topper)

#add issue stream request?
#add synchronous retune - set center frequency?
