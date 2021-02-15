import os 
from os import path

def get_meas_path(file_type, distance, rx_gain, src_att, physical_aoa):
    glob_path = os.getcwd()
    meas_dir = "%s/meas_dist_%dm_rx_%ddB_src_att_%ddB" %(glob_path, distance, rx_gain, src_att)

    try:
        os.mkdir(meas_dir)
    except OSError:
        if(path.exists(meas_dir)):
            print ("Directory: %s already exists, skipping" % meas_dir)
        else:
            print ("Creation of the directory: %s failed" % meas_dir)
    else:
        print ("Successfully created the directory: %s " % meas_dir)

    meas_path = ""
    if(file_type == "aoa"):
        meas_path = "%s/angle_%d_err.bin" %(meas_dir,physical_aoa)
    elif(file_type == "ch1"):
        meas_path = "%s/raw_ch_1_%d.bin" %(meas_dir,physical_aoa)
    elif(file_type == "ch2"):
        meas_path = "%s/raw_ch_2_%d.bin" %(meas_dir,physical_aoa)
    else:
        print("Unknown file type %s!" %file_type)

    print(meas_path)
    return meas_path





