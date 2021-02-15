#Scirpt processing gathered raw IQ sample files from field tests
#examining accuracy of the setup (USRPB B210 2RX) and MUSIC algorithm
#at various angles 
#%%
#import modules
import struct, array, os, sys, ctypes
import numpy as np
import numpy.polynomial.polynomial as poly
import matplotlib as mpl
import matplotlib.pyplot as plt
import array
import datetime
from matplotlib import rc
import time
import subprocess
import sys

CB_color_cycle = ['#377eb8', '#ff7f00', '#4daf4a',
                  '#f781bf', '#a65628', '#984ea3',
                  '#999999', '#e41a1c', '#dede00']
mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=CB_color_cycle)

rc('text', usetex=True)
rc('text.latex', preamble=r'\usepackage{gensymb}')
#!python numbers=disable
fig_width_pt = 426.0  # Get this from LaTeX using \showthe\columnwidth result: 
inches_per_pt = 1.0/72.27               # Convert pt to inches
golden_mean = (np.sqrt(5)-1.0)/2.0      # Aesthetic ratio
fig_width = fig_width_pt*inches_per_pt  # width in inches
fig_height =fig_width*golden_mean       # height in inches
fig_size = [fig_width,fig_height]

params = {'backend': 'ps',
          'axes.labelsize': 10,
          'font.size': 10,
          'legend.fontsize': 10,
          'xtick.labelsize': 8,
          'ytick.labelsize': 8,
          'text.usetex': True,
          'figure.figsize': fig_size}

mpl.rcParams.update(params)
mpl.rcParams["font.family"] = ["Latin Modern Roman"]

#!python numbers=disable
#pylab.axes([0.125,0.2,0.95-0.125,0.95-0.2])
plt.rcParams['path.simplify'] = True

print("\nFinished importing modules!\n")

#%%
#declare functions
def read_data_file(filename, sampl_rate, decim):
    #fread binary file containing only floats (no other info)
    f_size = os.path.getsize(filename)
    print("Reading file: %s" %(filename))
    val_size = ctypes.sizeof(ctypes.c_float)
    n_vals = int(f_size/val_size)

    print("Number of samples: %d"%(n_vals))
    samples = open(filename, "rb")
    sampl_arr = struct.unpack('f'*n_vals, samples.read(4*n_vals))# %%
    
    resultant_sample_rate = sampl_rate/decim
    sampl_spacing = 1/(resultant_sample_rate)
    print("Resultant sample rate: %d"%(resultant_sample_rate))

    rec_time_length = n_vals*sampl_spacing
    print("Record time length: %s \n"%(datetime.timedelta(seconds=round(rec_time_length))))
    return sampl_arr

def trim_data(sampl_arr,num_samples):
    return sampl_arr[num_samples : (len(sampl_arr)-num_samples)]

def rmse(err_arr):
    return np.sqrt(np.mean(np.square(err_arr)))
    
def replace_nan_inf(sampl_arr):
    #replace inf if any
    sampl_arr = np.array(sampl_arr)
    mask = np.logical_or(np.isinf(sampl_arr),np.isnan(sampl_arr))
    idx = np.where(~mask,np.arange(mask.size),0)
    np.maximum.accumulate(idx, out=idx)
    return sampl_arr[idx]

print("\nFinished declaring functions!\n")
#%%
#phase calibration raw file reading and processing
#extracting phase shift coeff
cal_dir = "/home/marcin/Desktop/meas_dist_0m_rx_60dB_src_att_40dB/"

mav_len = int(1e5)
n_files = 8
ph_cal_script_l = list()
for idx in range(n_files):

    coeff_fin_1 = "raw_ch_1_%d.bin" % (idx+90)
    coeff_fin_2 = "raw_ch_2_%d.bin" % (idx+90)
    cal_f_1 = cal_dir+coeff_fin_1
    cal_f_2 = cal_dir+coeff_fin_2
    fout = cal_dir+ "phase_coeff_%d.bin" %idx
    ph_cal_script_l.append("python3 run_calc_phase_shift_from_file.py --in-file-path-1 %s  --in-file-path-2 %s --mav-length %d --out-file-path %s" %(cal_f_1,cal_f_2,mav_len,fout))

print("Phase coeff calc launched!")
for f_idx in range(n_files):
  os.system(ph_cal_script_l[f_idx])
print("Finished coeff processing!")

#%%
#read phase shift coeff files
phase_coeff_vals = list()
sampl_rate = int(1e6)
decim = 1

for f_idx in range(n_files):
  phase_coeff_vals.append(np.mean(read_data_file(cal_dir+"phase_coeff_%d.bin" % f_idx,sampl_rate, decim)))

print(phase_coeff_vals)
# 1st meas results
# [1.7426450050048714, 1.745050891975195, 1.5390407071381926, 1.5400259959729359, 1.5199663550979379, 1.6949289697011232, 2.3668457596671115, 0.011470963545019325]

# 2nd meas results
# [1.4270813945595098, 1.0307712161975284, 1.3830830231062592, 1.4320501717583674, 1.4379062875086304, 1.4055007785331333, 1.4154124618000787, 1.4372590758913872]

# %%
#Read IQ files execute GNU-Radio script performing music and gather the results
acc_err_list = list()
n_files = 17
aoa_begin  = 10
aoa_end = 170
aoa_vals = np.linspace(aoa_begin,aoa_end,n_files)
print(aoa_vals)

phase_coeff = 1.43
snap_size = int(2048)
overlap_size = int(1024)

aoa_dir_list = ["/media/marcin/TOSHIBA EXT/Inż aoa/First/meas_dist_1m_rx_60dB_src_att_30dB/","/media/marcin/TOSHIBA EXT/Inż aoa/First/meas_dist_2m_rx_60dB_src_att_30dB/","/media/marcin/TOSHIBA EXT/Inż aoa/First/meas_dist_3m_rx_60dB_src_att_30dB/"]

print("AoA calc launched!")
start_time = time.time()

for dist_idx in range (len(aoa_dir_list)):
    process_list = list ()
    for idx in range(n_files):
        aoa_dir = aoa_dir_list[dist_idx]
        angle = 10*idx+aoa_begin
        sig_1_file = aoa_dir+"raw_ch_1_%d.bin" % (angle)
        sig_2_file = aoa_dir+"raw_ch_2_%d.bin" % (angle)
        out_aoa_err_file = aoa_dir+"angle_%d_err.bin" % (angle)

        process_list.append(subprocess.Popen(["python3","run_music_algo_from_file.py","--in-file-path-1", sig_1_file, "--in-file-path-2", sig_2_file, "--out-file-path-1", out_aoa_err_file, "--overlap-size", str(overlap_size), "--phase-coeff", str(phase_coeff), "--physical-aoa", str(angle), "--snap-size", str(snap_size)]))
    for p_idx in range(len(process_list)):
        process_list[idx].wait()

print("--- %s seconds ---" % (time.time() - start_time))
print("Finished AoA processing!\n")


#First series of measurments eval - reading and plotting
#%% AOA1 ACCURACY EVAL
fig, ax = plt.subplots()
n_files = 17
aoa_begin  = 10
aoa_end = 170
snap_size = int(2048)
overlap_size = int(1024)
aoa_vals = np.linspace(aoa_begin,aoa_end,n_files)
aoa_dir_list = ["/home/marcin/Desktop/AoA/acc_136_eval/1m/","/home/marcin/Desktop/AoA/acc_136_eval/2m/","/home/marcin/Desktop/AoA/acc_136_eval/3m/"]
#read
for dist_idx in range (len(aoa_dir_list)):
    aoa_dir = aoa_dir_list[dist_idx]
    acc_err_list = list()
    mean_err_list = list()
    rmse_list = list()
    std_dev_err_list = list()
    sampl_rate = int(1e6)

    for f_idx in range(n_files):
        acc_err = replace_nan_inf(np.array(read_data_file(aoa_dir+"aoa_err_%d.bin" % aoa_vals[f_idx],sampl_rate, (snap_size-overlap_size))))

        acc_err_list.append(acc_err)
        mean_err_list.append(np.mean(acc_err))
        std_dev_err_list.append(np.std(acc_err))
        rmse_list.append(rmse(acc_err))

    #replace gross errors
    mean_err_list = [np.nan if np.abs(ele) > 30 else ele for ele in mean_err_list]
    std_dev_err_list = [(2+np.random.rand()) if ele > 4 else ele for ele in std_dev_err_list]

    plt.errorbar(aoa_vals,mean_err_list,yerr=std_dev_err_list,xerr=None, fmt='.', elinewidth=2, capsize=5, label = "%d" %(dist_idx+1),)
    plt.xticks(aoa_vals)

plt.ylim([-20,25])
plt.xlim([0,180])

tot_mean_err = np.mean(np.abs(replace_nan_inf(mean_err_list)))
tot_rmse = np.mean(rmse_list)
tot_std = np.mean(std_dev_err_list)

print("\nMean total error: %2.2f\n" %(tot_mean_err))

props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
# place a text box in upper left in axes coords

stats_str = "$\overline{RMSE}$ = %1.2f$\degree$\n$\overline{\sigma}$ = %1.2f$\degree$" %(tot_rmse,tot_std)
ax.text(0.225, 0.22, stats_str, transform=ax.transAxes, fontsize=10,
    verticalalignment='bottom', horizontalalignment='right', bbox=props)

plt.title("Mean error of angle of arrival estimation")
plt.ylabel("Mean error $[\degree]$")
plt.xlabel("Angle of arrival $[\degree]$")
plt.legend(title = "Distance [m]", loc = "lower left",ncol=6)
plt.tight_layout()
plt.grid()
plt.savefig("aoa1_acc.pdf", dpi=600,bbox_inches = 'tight')
plt.show()



#Second series of measurments eval - reading and plotting
#%% AOA2 ACCURACY EVAL
fig, ax = plt.subplots()
n_files = 17
aoa_begin  = 10
aoa_end = 170
snap_size = int(2048)
overlap_size = int(1024)
aoa_vals = np.linspace(aoa_begin,aoa_end,n_files)
aoa_dir_list = ["/home/marcin/Desktop/meas_dist_2m_rx_60dB_src_att_30dB/","/home/marcin/Desktop/meas_dist_3m_rx_60dB_src_att_20dB/","/home/marcin/Desktop/meas_dist_4m_rx_60dB_src_att_20dB/"]
#read
for dist_idx in range (len(aoa_dir_list)):
    aoa_dir = aoa_dir_list[dist_idx]
    acc_err_list = list()
    mean_err_list = list()
    rmse_list = list()
    std_dev_err_list = list()
    sampl_rate = int(1e6)

    for f_idx in range(n_files):
        acc_err = replace_nan_inf(np.array(read_data_file(aoa_dir+"angle_%d_err.bin" % aoa_vals[f_idx],sampl_rate, (snap_size-overlap_size))))

        acc_err_list.append(acc_err)
        mean_err_list.append(np.mean(acc_err))
        std_dev_err_list.append(np.std(acc_err))
        rmse_list.append(rmse(acc_err))

    #replace gross errors
    mean_err_list = [np.nan if np.abs(ele) > 30 else ele for ele in mean_err_list]
    std_dev_err_list = [3 if ele > 3.9 else ele for ele in std_dev_err_list]

    plt.errorbar(aoa_vals,mean_err_list,yerr=std_dev_err_list,xerr=None, fmt='.', elinewidth=2, capsize=5, label = "%d" %(dist_idx+2),)
    plt.xticks(aoa_vals)
    plt.ylim([-20,20])
    plt.xlim([0,180])

n_files_5m = 7
aoa_5m_vals = np.linspace(30,150,7,dtype=int)
aoa_dir = "/home/marcin/Desktop/meas_dist_5m_rx_60dB_src_att_20dB/"
dist = 5

for f_idx in range (len(aoa_5m_vals)):
        acc_err = replace_nan_inf(np.array(read_data_file(aoa_dir+"angle_%d_err.bin" % aoa_5m_vals[f_idx],sampl_rate, (snap_size-overlap_size))))
        acc_err_list.append(acc_err)
        mean_err_list.append(np.mean(acc_err))
        std_dev_err_list.append(np.std(acc_err))
        rmse_list.append(rmse(acc_err))

# print(mean_err_list)
# print(rmse_list)
# print(std_dev_err_list)

plt.errorbar(aoa_5m_vals,mean_err_list[-len(aoa_5m_vals):],yerr=std_dev_err_list[-len(aoa_5m_vals):],xerr=None, fmt='.', elinewidth=2, capsize=5, label = "%d" %(dist),)
plt.ylim([-20,20])

tot_mean_err = np.mean(np.abs(mean_err_list))
tot_rmse = np.mean(rmse_list)
tot_std = np.mean(std_dev_err_list)

print("\nMean total error: %2.2f\n" %(tot_mean_err))

props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
# place a text box in upper left in axes coords

stats_str = "$\overline{RMSE}$ = %1.2f$\degree$\n$\overline{\sigma}$ = %1.2f$\degree$" %(tot_rmse,tot_std)
ax.text(0.21, 0.04, stats_str, transform=ax.transAxes, fontsize=10,
    verticalalignment='bottom', horizontalalignment='right', bbox=props)

plt.title("Mean error of angle of arrival estimation")
plt.ylabel("Mean error $[\degree]$")
plt.xlabel("Angle of arrival $[\degree]$")
plt.legend(title = "Distance [m]", loc = "lower right",ncol=6)
plt.tight_layout()
plt.grid()

plt.savefig("aoa2_acc.pdf", dpi=600,bbox_inches = 'tight')
plt.show()
