#%%
from gnuradio import uhd

uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("", "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,2)),
            ),
        )

#streamer restart/align
stop_cmd = uhd.stream_cmd_t(uhd.stream_cmd_t.STREAM_MODE_STOP_CONTINUOUS)
stop_cmd.stream_now = True

self.uhd_usrp_source_0.issue_stream_cmd(stop_cmd)

stream_cmd = uhd.stream_cmd_t(uhd.stream_cmd_t.STREAM_MODE_START_CONTINUOUS)
stream_cmd.stream_now = False
#delay by 5s
stream_cmd.time_spec = self.uhd_usrp_source_0.get_time_now() + uhd.time_spec_t(5.0)
self.uhd_usrp_source_0.issue_stream_cmd(stream_cmd)

#freq align - potential phase sync
retune_time = self.uhd_usrp_source_0.get_time_now()+uhd.time_spec_t(5.0)
self.uhd_usrp_source_0.set_command_time(retune_time)

center_freq_tmp = 2.4501e9
tune_req = uhd.tune_request_t(center_freq_tmp)
self.uhd_usrp_source_0.set_center_freq(tune_req,0)
self.uhd_usrp_source_0.set_center_freq(tune_req,1)

self.uhd_usrp_source_0.clear_command_time()

print("Finished!")
# %%
