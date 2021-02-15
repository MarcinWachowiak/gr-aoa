import os 

def get_meas_path(distance, rx_gain, src_att, physical_aoa):
        glob_path = os.getcwd()
        meas_dir = "%s/meas_dist_%dm_rx_%ddB_src_att_%ddB" %(glob_path, distance, rx_gain, src_att)

        try:
            os.mkdir(meas_dir)
        except OSError:
            print ("Creation of the directory %s failed" % meas_dir)
        else:
            print ("Successfully created the directory %s " % meas_dir)

        meas_path = "%s/angle_%d_err.bin" %(meas_dir,physical_aoa)
        print(meas_path)
        return meas_path
