/*
How to synchronize USRPs
Based on: https://kb.ettus.com/Synchronizing_USRP_Events_Using_Timed_Commands_in_UHD
and
https://files.ettus.com/manual/page_sync.html
Targetted for devices availbile at uni Nxxx Bxxx

When additional DSP/FPGA optimized function blocks are required
Check RFNoC feature and blocks
*/

#include "gr_uhd_common.h"
#include "usrp_source_impl.h"
#include <boost/format.hpp>
#include <boost/make_shared.hpp>
#include <boost/thread/thread.hpp>
#include <iostream>
#include <stdexcept>

namespace gr {
namespace uhd {

//shared pointer for all usrp devices in network
::uhd::usrp::multi_usrp::sptr multi_usrp_sptr = uhd::usrp::multi_usrp::make( 
"addr0=192.168.10.2, addr1=192.168.10.3, addr3=192.168.10.4");

//set peripheral clk and time sources
multi_usrp->set_clock_source("external"); 
multi_usrp->set_time_source("external");

//latch regular local time reset by reference PPS 
multi_usrp->set_time_next_pps(uhd::time_spec_t(0.0));
std::this_thread::sleep_for(std::chrono::milliseconds(1000));


//synchronized retune 
multi_usrp->clear_command_time();

multi_usrp->set_command_time(multi_usrp->get_time_now() + uhd::time_spec_t(0.1)); //set cmd time for .1s in the future

uhd::tune_request_t tune_request(freq);
multi_usrp->set_rx_freq(tune_request);
std::this_thread::sleep_for(std::chrono::milliseconds(110)); //sleep 110ms (~10ms after retune occurs) to allow LO to lock

multi_usrp->clear_command_time();

//phase offset ambiguity still present
//needs to be corrected after input stream observation

//synchronous RX
// create a receive streamer
uhd::stream_args_t stream_args("fc32", wire); // complex floats
//define input channels
stream_args.channels = "0,1,2,3,4,5";
uhd::rx_streamer::sptr rx_stream = multi_usrp->get_rx_stream(stream_args);

// setup streaming
uhd::stream_cmd_t stream_cmd(uhd::stream_cmd_t::STREAM_MODE_START_CONTINUOUS);
stream_cmd.stream_now = false;
//set stream start timestamp
stream_cmd.time_spec  = uhd::time_spec_t(multi_usrp->get_time_now() + uhd::time_spec_t(1.0));
rx_stream->issue_stream_cmd(stream_cmd);







































//synchronous TX - similar to RX
// create a transmit streamer
uhd::stream_args_t stream_args("fc32", wire); // complex floats
//define input channels
stream_args.channels = "0,1,2,3,4,5";
uhd::tx_streamer::sptr tx_stream = multi_usrp->get_tx_stream(stream_args);

// setup streaming
uhd::stream_cmd_t stream_cmd(uhd::stream_cmd_t::STREAM_MODE_START_CONTINUOUS);
stream_cmd.stream_now = false;
//set stream start timestamp
stream_cmd.time_spec  = uhd::time_spec_t(multi_usrp->get_time_now() + uhd::time_spec_t(1.0));
tx_stream->issue_stream_cmd(stream_cmd);
    }
}