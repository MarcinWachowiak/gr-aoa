#Scripts evaluating gathered AoA data for various scenarios
#including: high acitivity in the wireless channel, effects
#of bandpass filtration and movement during measurment
#%%
#import modules
import struct, array, os, sys, ctypes
import numpy as np
import numpy.polynomial.polynomial as poly
import matplotlib as mpl
import matplotlib.pyplot as plt
import array
import datetime
import scipy.signal as scp
from matplotlib import rc
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import FormatStrFormatter

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
          'axes.labelsize': 8,
          'font.size': 8,
          'legend.fontsize': 8,
          'xtick.labelsize': 8,
          'ytick.labelsize': 8,
          'text.usetex': True,
          'figure.figsize': fig_size}

mpl.rcParams.update(params)
mpl.rcParams["font.family"] = ["Latin Modern Roman"]

#!python numbers=disable
#pylab.axes([0.125,0.2,0.95-0.125,0.95-0.2])
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

def fw_replace_nan(sampl_arr):
    #replace inf if any
    mask = np.logical_or(np.isinf(sampl_arr),np.isnan(sampl_arr))
    idx = np.where(~mask,np.arange(mask.size),0)
    np.maximum.accumulate(idx, out=idx)
    return sampl_arr[idx]

print("\nFinished declaring functions!\n")

# %%
#Read AoA values from files
sampl_rate = int(1e6)
decim = int(1024)
dir = "/home/marcin/Desktop/"
ref_err = read_data_file(dir+"ref_90_deg.bin",sampl_rate,decim)
movement_err = read_data_file(dir+"movement_90_deg.bin",sampl_rate,decim)
act_filter_err = read_data_file(dir+"filter_90_deg.bin",sampl_rate,decim)
act_no_filter_err = read_data_file(dir+"no_filter_90_deg.bin",sampl_rate,decim)

#remove DC offset to expose variabiity (remove constant error)
ref_err = ref_err - np.mean(ref_err)
movement_err = movement_err - np.mean(movement_err)
act_filter_err = act_filter_err - np.mean(act_filter_err)
act_no_filter_err = act_no_filter_err - np.mean(act_no_filter_err)
time_vals = np.linspace(0,60,len(ref_err))
#%%
#HIGH / LOW ACTIVITY IN THE WIRELESS CHANNEL EVAL
props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
fig, axs = plt.subplots(2)
fig.suptitle('Estimation error in regard to activity in wireless channel at 2.45 GHz', fontsize=12)
axs[0].plot(time_vals,ref_err,'o',ms=0.5,rasterized=True,fillstyle='full')
axs[0].set_title("Low activity",fontsize=9)
axs[0].text(0.825, 0.06,("$RMSE = %1.3f\degree$" % np.std(ref_err)), transform=axs[0].transAxes, fontsize=8, verticalalignment='bottom', bbox=props)

axs[1].plot(time_vals,act_filter_err,'o',ms=0.5,rasterized=True,fillstyle='full')
axs[1].set_title("High activity",fontsize=9)
axs[1].text(0.825, 0.06, ("$RMSE = %1.3f\degree$" % np.std(act_filter_err)), transform=axs[1].transAxes, fontsize=8, verticalalignment='bottom', bbox=props)

axs[1].set_xlabel('Time [s]')
axs[0].set_ylabel('AoA error [$\degree$]')
axs[1].set_ylabel('AoA error [$\degree$]')

plt.tight_layout()
plt.savefig("aoa_low_high_activity.pdf",dpi=600,bbox_inches = 'tight')
plt.show()

#%%
#FILTER / NO FILTER HIGH ACTIVITY IN WIRELESS CHANNEL EVAL
props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)

fig, axs = plt.subplots(2)
fig.suptitle('Effect of band-pass filtering on estimation error at 2.45 GHz', fontsize=12)
axs[0].plot(time_vals,act_no_filter_err,'o',ms=0.5,rasterized=True,fillstyle='full')
axs[0].set_title("Without band-pass filter",fontsize=9)
axs[0].text(0.823, 0.06,("$RMSE = %1.3f\degree$" % np.std(act_no_filter_err)), transform=axs[0].transAxes, fontsize=8, verticalalignment='bottom', bbox=props)

axs[1].plot(time_vals,act_filter_err,'o',ms=0.5,rasterized=True,fillstyle='full')
axs[1].set_title("With band-pass filter",fontsize=9)
axs[1].text(0.823, 0.06, ("$RMSE = %1.3f\degree$" % np.std(act_filter_err)), transform=axs[1].transAxes, fontsize=8, verticalalignment='bottom', bbox=props)

axs[1].set_xlabel('Time [s]')
axs[0].set_ylabel('AoA error [$\degree$]')
axs[1].set_ylabel('AoA error [$\degree$]')

plt.tight_layout()
plt.savefig("aoa_filtering_effect.pdf",dpi=600,bbox_inches = 'tight')
plt.show()

#%%
#MOVEMENT / NO MOVEMENT LOW ACTIVITY EVAL
props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)

fig, axs = plt.subplots(2)
fig.suptitle('Effect of movement on estimation error at 2.45 GHz', fontsize=12)
axs[0].plot(time_vals,ref_err,'o',ms=0.5,rasterized=True,fillstyle='full')
axs[0].set_title("Static environment",fontsize=9)
axs[0].text(0.823, 0.06,("$RMSE = %1.3f\degree$" % np.std(ref_err)), transform=axs[0].transAxes, fontsize=8, verticalalignment='bottom', bbox=props)

axs[1].plot(time_vals,movement_err,'o',ms=0.3,color ='#377eb8',linewidth=0 ,rasterized=True,fillstyle='full')
axs[1].set_title("Movement in room -- walking person",fontsize=9)
axs[1].text(0.823, 0.06, ("$RMSE = %1.3f\degree$" % np.std(movement_err)), transform=axs[1].transAxes, fontsize=8, verticalalignment='bottom', bbox=props)

axs[1].set_xlabel('Time [s]')
axs[0].set_ylabel('AoA error [$\degree$]')
axs[1].set_ylabel('AoA error [$\degree$]')

plt.tight_layout()
plt.savefig("aoa_movement_eff.pdf",dpi=600,bbox_inches = 'tight')
plt.show()

# %%
#MOVEMENT CHARACTERISTIC SHAPE ZOOM
divider = 18
print(len(movement_err))
samp_count = int(len(movement_err)/divider) #10s interval
movement_err_zoom = movement_err[6*samp_count:7*samp_count:]
time_vals_zoom = np.linspace(0,60/divider,len(movement_err_zoom))

fig, axs = plt.subplots()
axs.set_title("Estimation error in environment with movement",fontsize = 12)

axs.plot(time_vals_zoom,movement_err_zoom,'o',ms=0.6,rasterized=True,fillstyle='full')
axs.set_xlabel('Time [s]')
axs.set_ylabel('AoA error [$\degree$]')
plt.xlim([0,3])
plt.tight_layout()
plt.savefig("aoa_mov_zoomed.pdf",dpi=600,bbox_inches = 'tight')
plt.show()
