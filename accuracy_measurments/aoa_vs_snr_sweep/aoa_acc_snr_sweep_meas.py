#Script launching generated GNU-Radio measurment routines, that
#measure noise power level, AoA error and signal power level to
#analyze how AoA error depends on SNR

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
    return sampl_arr, sampl_spacing
print("\nFinished declaring functions!\n")

def rmse(err_arr):
    return np.sqrt(np.mean(np.square(err_arr)))

#%%
# file paths
file_dir = "/home/marcin/GNU-Radio-USRP-AoA/accuracy_measurments/aoa_snr_sweep/results/"

#measure noise power level
for snr_meas in range(5):
    snr_file_name = file_dir + "snr_ref_lvl_%d.bin" % snr_meas
    print("Launched measurment of SNR : %d" % snr_meas)
    os.system("python3 run_noise_pow_meas.py --snr-filename %s" %(snr_file_name))

#GR measurment routines params (source located at 90 deg.)
phase_coeff = 1.428
n_steps = 90
src_att_vec = np.round(np.linspace(0,89,n_steps))
#src_att_vec =  np.unique(np.round(np.logspace(2,6.4,n_steps, base=2)))

#measure AoA and signal power level
print("Src attenuation vector: ",src_att_vec)
for att_val in src_att_vec:

    print("Launched measurment for SRC ATT: %d" % att_val)
    aoa_file_name = file_dir + "aoa_src_att_%d.bin" % (att_val)
    snr_file_name = file_dir + "sig_pwr_src_att_%d.bin" % (att_val)
    os.system("python3 run_aoa_acc_sig_pow_meas.py --aoa-filename %s  --phase-coeff %f --snr-filename %s --src-att %d" %(aoa_file_name, phase_coeff, snr_file_name, att_val))

print("Measurment finished!")


# %%
#Read the gathered data, noise, sig power levels and AoA error
sampl_rate = int(1e6)
decim = 1024
file_dir = "/home/marcin/GNU-Radio-USRP-AoA/accuracy_measurments/aoa_snr_sweep/results/"

aoa_val_l = list()
aoa_std =list()
noise_pwr_l = list()
sig_pwr_l = list()
snr_l = list()

#read noise files
for snr_idx in range (5):

    noise_pwr, ss = read_data_file(file_dir+"snr_ref_lvl_%d.bin"%snr_idx,sampl_rate,decim)
    noise_pwr_l.append(np.mean(noise_pwr))

print("Noise levels: ", noise_pwr_l)
avg_noise_lvl = np.mean(noise_pwr_l)
print("Average noise lvl: ", avg_noise_lvl)

#read AoA and signal files
for src_att in range (90):
    aoa_arr, ss = read_data_file(file_dir+"aoa_src_att_%d.bin"%src_att,sampl_rate,decim)
    sig_pwr, ss = read_data_file(file_dir+"sig_pwr_src_att_%d.bin"%src_att,sampl_rate,decim)

    aoa_val_l.append(rmse(aoa_arr))
    aoa_std.append(np.std(aoa_arr))

    avg_sig_pwr = np.mean(sig_pwr)
    sig_pwr_l.append(avg_sig_pwr)

    snr_val = 10*np.log10(avg_sig_pwr/avg_noise_lvl)
    snr_l.append(snr_val)


#%%
#Select data range for plotting
print(snr_l)
n_first_vals = 50
snr_l=snr_l[-n_first_vals:],
aoa_val_l = aoa_val_l[-n_first_vals:]
aoa_std = aoa_std[-n_first_vals:]

snr_l = (np.round(np.array(snr_l),decimals=0))
snr_l_arr, idx_list = np.unique(snr_l,return_index=True)

print(snr_l_arr)

aoa_val_l = np.abs(np.take(aoa_val_l,idx_list,axis=0))
aoa_std = np.take(aoa_std,idx_list,axis=0)

#%%
#plot and save figure
fig, ax = plt.subplots()
plt.errorbar(snr_l_arr,aoa_val_l,yerr=aoa_std,xerr=None, fmt='.', elinewidth=1.2, capsize=3)

plt.title("Error of angle estimation in regard to SNR")
plt.ylabel("RMSE of angle estimation $[\degree]$")
plt.xlabel("Signal to noise ratio [dB]")
plt.xlim([-4,38])
plt.ylim([0,19])

plt.tight_layout()
plt.grid()
plt.savefig("meas_aoa_vs_snr.pdf", dpi=600,bbox_inches = 'tight')

plt.show()
