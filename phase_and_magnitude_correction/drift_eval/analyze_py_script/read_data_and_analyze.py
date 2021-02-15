#Script reading, analysing and plotting correcitng coefficients
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
    
    resultant_sample_rate = sampl_rate/decimation
    sampl_spacing = 1/(resultant_sample_rate)
    print("Resultant sample rate: %d"%(resultant_sample_rate))

    rec_time_length = n_vals*sampl_spacing
    print("Record time length: %s \n"%(datetime.timedelta(seconds=round(rec_time_length))))
    return sampl_arr, sampl_spacing

def plot_data_with_stats(sampl_arr,sampl_spacing,is_phase):
    #calculate stats
    coeff_mean = np.mean(sampl_arr,dtype=np.float64)
    coeff_std_dev = np.std(sampl_arr,dtype=np.float64)
    rel_std_var = np.abs(100*coeff_std_dev/coeff_mean)
    
    stats_str = r"$\sigma$ = %1.3f" % coeff_std_dev
    title_str = "Power correction coefficient"
    y_label_str ="Power correction coefficent value [-]"
    leg_loc = 4
    txt_x = 0.855
    txt_y = 0.15

    if (is_phase):
        angle_std_variation = np.rad2deg(coeff_std_dev)
        stats_str = r"$\sigma$ = %1.4f $\approx$ %1.2f$\degree$" % (coeff_std_dev,angle_std_variation)
        title_str = "Phase correction coefficient"
        y_label_str ="Coefficient value [rad]"
        leg_loc = 1
        txt_x = 0.74
        txt_y = 0.8
        
    props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
    fig, ax = plt.subplots()
    # place a text box in upper left in axes coords
    ax.text(txt_x, txt_y, stats_str, transform=ax.transAxes, fontsize=10,
        verticalalignment='bottom', bbox=props)
    #simple data plot
    plt.title(title_str)
    plt.xlabel("Time [h]")
    plt.ylabel(y_label_str)

    timebase = np.linspace(0,sampl_spacing*len(sampl_arr),len(sampl_arr))
    ax.plot(timebase, sampl_arr, linewidth=0.1)

    decimation_rate = 1000
    timebase_decim = timebase[0:len(timebase):decimation_rate]
    sampl_arr_decim = sampl_arr[0:len(sampl_arr):decimation_rate]

    poly_deg = 7
    poly_coeff = poly.polyfit(timebase_decim, sampl_arr_decim,poly_deg)
    ffit = poly.polyval(timebase_decim, poly_coeff)
    ax.plot(timebase_decim,ffit)
    
    ax.legend(['_nolegend_', "Polynomial fit"],loc=leg_loc)

    x_ticks_loc = (np.arange(min(timebase),max(timebase),3600))
    x_ticks_val = arr_get_hh(x_ticks_loc)
    #y_ticks_loc = ((np.round(np.linspace(min(sampl_arr),3),np.round(max(sampl_arr),3),8)))
    plt.xticks(x_ticks_loc,x_ticks_val)
    plt.locator_params(axis='y',nbins=11)
    plt.xlim([min(x_ticks_loc),max(x_ticks_loc)])
    plt.grid()

def plot_data_with_stats_composite(fig, ax,sampl_arr_list,ss_l):
    
    #simple data plot
    plt.xlabel("Time [min]")
    plt.ylabel("Coefficient value [rad]")

    for arr_idx in range (len(sampl_arr_list)):
        timebase = np.linspace(0,ss_l[arr_idx]*len(sampl_arr_list[arr_idx]),len(sampl_arr_list[arr_idx]))
        ax.plot(timebase, sampl_arr_list[arr_idx], linewidth=1)

def trim_data_and_plot(sampl_arr,num_samples,sampl_spacing):
    data_begin = sampl_arr[ : num_samples]
    data_mid = sampl_arr[num_samples : (len(sampl_arr)-num_samples)]
    data_end = sampl_arr[(len(sampl_arr)-num_samples) : ]
    
    t_base_begin = np.linspace(0,num_samples*sampl_spacing,num_samples)
    t_base_mid = np.linspace(sampl_spacing*num_samples,sampl_spacing*(len(sampl_arr)-num_samples),len(sampl_arr)-2*num_samples)
    #t_base_end = np.linspace(sampl_spacing*(len(sampl_arr)-num_samples),sampl_spacing*len(sampl_arr),num_samples)

    ax1 = plt.subplot(212)
    ax1.plot(t_base_mid,data_mid)
    ax1.set_title('Middle')
    x_ticks_loc = (np.linspace(min(t_base_mid),max(t_base_mid),8).round())
    x_ticks_val = arr_get_h_m_format(x_ticks_loc)
    ax1.set_xticks(x_ticks_loc)
    ax1.set_xticklabels(x_ticks_val)
    ax1.set_xlabel("Time [hh:mm]")
    ax1.grid()

    ax2 = plt.subplot(221)
    ax2.plot(t_base_begin,data_begin)
    ax2.set_title('Beginning')
    ax2.set_xlabel("Time [s]")
    ax2.grid()

    ax3 = plt.subplot(222)
    ax3.plot(t_base_begin,data_end)
    ax3.set_title('Tail')
    ax3.set_xlabel("Time [s]")
    ax3.grid()

    plt.tight_layout()
    plt.show()

    return data_mid 

def trim_data(sampl_arr,num_samples):
    return sampl_arr[num_samples : (len(sampl_arr)-num_samples)]

def trim_data_spc(sampl_arr,num_s_begin, num_s_end):
    return sampl_arr[num_s_begin : (len(sampl_arr)-num_s_end)]

def arr_get_h_m_format(seconds_arr):
    ret_str_arr = list()
    for idx in range(len(seconds_arr)):
        ret_str_arr.append(str(datetime.timedelta(seconds=seconds_arr[idx]))[:-3])
    return ret_str_arr

def arr_get_hh(seconds_arr):
    ret_str_arr = list()
    for idx in range(len(seconds_arr)):
        ret_str_arr.append(str(datetime.timedelta(seconds=seconds_arr[idx]))[:-6])
    return ret_str_arr

def fw_replace_nan(sampl_arr):
    #replace inf if any
    mask = np.logical_or(np.isinf(sampl_arr),np.isnan(sampl_arr))
    idx = np.where(~mask,np.arange(mask.size),0)
    np.maximum.accumulate(idx, out=idx)
    return sampl_arr[idx]

print("\nFinished declaring functions!\n")


#%%
#REFERENCE PLOT - wired setup
sampl_rate = int(1e6)
decimation = int(1e4)
n_skip_samples = int(100)

#read data
dir = "/home/marcin/Desktop/ref_drift/"

mag_drift_arr, mag_sampl_spacing = read_data_file(dir+'mag_corr_coeff_mav_1k_filter_log.bin',sampl_rate, decimation)
mag_arr_mid = trim_data_and_plot(mag_drift_arr, n_skip_samples,mag_sampl_spacing)
plot_data_with_stats(mag_arr_mid,mag_sampl_spacing,False)
plt.ylim([1.269,1.278])
plt.tight_layout()
plt.savefig("ref_mag_drift.pdf",dpi=600,bbox_inches = 'tight')
plt.show()

phase_drift_arr, ph_sampl_spacing = read_data_file(dir+'phase_shift_coeff_mav_1k_filter_log.bin',sampl_rate, decimation)
phase_arr_mid = trim_data_and_plot(phase_drift_arr, n_skip_samples,ph_sampl_spacing)
plot_data_with_stats(phase_arr_mid,ph_sampl_spacing,True)
plt.ylim([-1.966,-1.957])
plt.tight_layout()
plt.savefig("ref_phase_drift.pdf",dpi=600,bbox_inches = 'tight')
plt.show()
print("\nFinished plotting!\n\n")


#%%
#2,45GHz MAV with band-pass filter eval, MAV length sweep
sampl_rate = int(1e6)
decimation = int(1e4)
n_skip_samples = int(60*100)

#no movement in room during measurment 
#dir_name_1= "/home/marcin/GNU-Radio-USRP-Beamforming/phase_and_magnitude_correction/drift_eval/recorded/drift_meas_2_45G_1MSPS_10e4_decim_filtered_full_mav_eval/"

#with movement in room during measurment 
dir_name_1 = "/home/marcin/Desktop/phase_drift_eval_5/"

mag_file_names_1 = ["mag_corr_coeff_mav_1k_nofilter_log.bin","mag_corr_coeff_mav_10k_nofilter_log.bin","mag_corr_coeff_mav_100k_nofilter_log.bin","mag_corr_coeff_mav_1M_nofilter_log.bin","mag_corr_coeff_mav_10M_nofilter_log.bin"]

#pha_file_names_1 = ["phase_shift_coeff_mav_1k_nofilter_log.bin","phase_shift_coeff_mav_10k_nofilter_log.bin","phase_shift_coeff_mav_100k_nofilter_log.bin","phase_shift_coeff_mav_1M_nofilter_log.bin"]

pha_file_names_1 = ["phase_shift_coeff_mav_1k_filter_log.bin","phase_shift_coeff_mav_10k_filter_log.bin","phase_shift_coeff_mav_100k_filter_log.bin","phase_shift_coeff_mav_1M_filter_log.bin","phase_shift_coeff_mav_10M_filter_log.bin"]


mag_sampl_arr_list_1 = list()
mag_ss_vec_l_1 = list()
pha_sampl_arr_list_1 = list()
pha_ss_vec_l_1 = list()

n_files_each_1 = 5

#read
for f_idx in range(n_files_each_1):
    mag_sampl_arr, mag_ss_vec = read_data_file(dir_name_1 + mag_file_names_1[f_idx],sampl_rate,decimation)
    mag_sampl_arr_list_1.append(fw_replace_nan(np.array(mag_sampl_arr)))
    mag_ss_vec_l_1.append(mag_ss_vec)

for f_idx in range(n_files_each_1):
    pha_sampl_arr, pha_ss_arr = read_data_file(dir_name_1 + pha_file_names_1[f_idx],sampl_rate,decimation)
    pha_sampl_arr_list_1.append(fw_replace_nan(np.array(pha_sampl_arr)))
    pha_ss_vec_l_1.append(pha_ss_arr)
    
#trim
n_last_samples = 3600*100
for f_idx in range(n_files_each_1):
    arr_mid = trim_data(mag_sampl_arr_list_1[f_idx], n_skip_samples)
    mag_sampl_arr_list_1[f_idx] = arr_mid

    arr_mid = trim_data(-pha_sampl_arr_list_1[f_idx], n_skip_samples)
    pha_sampl_arr_list_1[f_idx] = arr_mid[-n_last_samples:]
print("\nFinished reading!\n")

#plot
fig, ax = plt.subplots()
plt.title("Phase correction coefficient with band-pass filter at 2.45 GHz")
props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
plot_data_with_stats_composite(fig, ax,pha_sampl_arr_list_1,pha_ss_vec_l_1)

stats_str = "1k$\,\,\,\,\,\,\,\,\sigma$ = %1.2f\n10k $\,\,\,\sigma$ = %1.2f\n100k $\sigma$ = %1.2f\n1M $\,\,\,\,\sigma$ = %1.2f\n10M $\,\sigma$ = %1.2f" %(np.std(pha_sampl_arr_list_1[0],dtype=np.float64),np.std(pha_sampl_arr_list_1[1],dtype=np.float64),np.std(pha_sampl_arr_list_1[2],dtype=np.float64),np.std(pha_sampl_arr_list_1[3],dtype=np.float64),np.std(pha_sampl_arr_list_1[4],dtype=np.float64))

ax.text(0.62, 0.039, stats_str, transform=ax.transAxes, fontsize=10,
    verticalalignment='bottom', bbox=props)

plt.legend(title = "MAV length",labels = ["1k", "10k", "100k","1M","10M"],loc ='lower right')
x_ticks_loc =np.linspace(0,3600,7)
x_ticks_val = (np.linspace(0,60,7))

x_strings = ["%2.2f" % number for number in x_ticks_val]
x_strings = [s.rstrip("0") for s in x_strings]
x_strings = [s.rstrip(".") for s in x_strings]

plt.xticks(x_ticks_loc,x_strings)
plt.xlim([0,3600])
plt.ylim([-1.2,3.2])

plt.grid()
plt.tight_layout()
plt.savefig("phase_distort_wfilter_2_45GHz.pdf",dpi=600,bbox_inches = 'tight')
plt.show()
print("\nFinished plotting!\n")


#%%
#2,44GHz MAV without band-pass filter eval, MAV sweep
sampl_rate = int(1e6)
decimation = int(1e4)
n_skip_samples = int(60*100)

#no movement in room during measurment 
#dir_name_1= "/home/marcin/GNU-Radio-USRP-Beamforming/phase_and_magnitude_correction/drift_eval/recorded/drift_meas_2_45G_1MSPS_10e4_decim_filtered_full_mav_eval/"

#with movement in room during measurment 
dir_name_1 = "/home/marcin/Desktop/phase_drift_eval_prime/"

mag_file_names_1 = ["mag_corr_coeff_mav_1k_nofilter_log.bin","mag_corr_coeff_mav_10k_nofilter_log.bin","mag_corr_coeff_mav_100k_nofilter_log.bin","mag_corr_coeff_mav_1M_nofilter_log.bin","mag_corr_coeff_mav_10M_nofilter_log.bin"]

#pha_file_names_1 = ["phase_shift_coeff_mav_1k_nofilter_log.bin","phase_shift_coeff_mav_10k_nofilter_log.bin","phase_shift_coeff_mav_100k_nofilter_log.bin","phase_shift_coeff_mav_1M_nofilter_log.bin"]

pha_file_names_1 = ["phase_shift_coeff_mav_1k_nofilter_log.bin","phase_shift_coeff_mav_10k_nofilter_log.bin","phase_shift_coeff_mav_100k_nofilter_log.bin","phase_shift_coeff_mav_1M_nofilter_log.bin","phase_shift_coeff_mav_10M_nofilter_log.bin"]


mag_sampl_arr_list_1 = list()
mag_ss_vec_l_1 = list()
pha_sampl_arr_list_1 = list()
pha_ss_vec_l_1 = list()

n_files_each_1 = 4

#read
for f_idx in range(n_files_each_1):
    mag_sampl_arr, mag_ss_vec = read_data_file(dir_name_1 + mag_file_names_1[f_idx],sampl_rate,decimation)
    mag_sampl_arr_list_1.append(fw_replace_nan(np.array(mag_sampl_arr)))
    mag_ss_vec_l_1.append(mag_ss_vec)

for f_idx in range(n_files_each_1):
    pha_sampl_arr, pha_ss_arr = read_data_file(dir_name_1 + pha_file_names_1[f_idx],sampl_rate,decimation)
    pha_sampl_arr_list_1.append(fw_replace_nan(np.array(pha_sampl_arr)))
    pha_ss_vec_l_1.append(pha_ss_arr)
    
#trim
n_last_samples = 3600*100
for f_idx in range(n_files_each_1):
    arr_mid = trim_data(mag_sampl_arr_list_1[f_idx], n_skip_samples)
    mag_sampl_arr_list_1[f_idx] = arr_mid

    arr_mid = trim_data(pha_sampl_arr_list_1[f_idx], n_skip_samples)
    pha_sampl_arr_list_1[f_idx] = arr_mid[-n_last_samples:]
print("\nFinished reading!\n")

fig, ax = plt.subplots()
plt.title("Phase correction coefficient without band-pass filter at 2.44 GHz")
props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
plot_data_with_stats_composite(fig, ax,pha_sampl_arr_list_1,pha_ss_vec_l_1)

stats_str = "1k$\,\,\,\,\,\,\,\,\sigma$ = %1.2f$\cdot10^{-3}$\n10k $\,\,\,\sigma$ = %1.2f$\cdot10^{-3}$\n100k $\sigma$ = %1.2f$\cdot10^{-3}$\n1M $\,\,\,\,\sigma$ = %1.2f$\cdot10^{-3}$" %(1000*np.std(pha_sampl_arr_list_1[0],dtype=np.float64),1000*np.std(pha_sampl_arr_list_1[1],dtype=np.float64),1000*np.std(pha_sampl_arr_list_1[2],dtype=np.float64),1000*np.std(pha_sampl_arr_list_1[3],dtype=np.float64))

ax.text(0.735, 0.035, stats_str, transform=ax.transAxes, fontsize=10,
    verticalalignment='bottom', bbox=props)

plt.legend(title = "MAV length",labels = ["1k", "10k", "100k","1M","10M"],loc = 1)
x_ticks_loc =np.linspace(0,3600,7)
x_ticks_val = (np.linspace(0,60,7))

x_strings = ["%2.2f" % number for number in x_ticks_val]
x_strings = [s.rstrip("0") for s in x_strings]
x_strings = [s.rstrip(".") for s in x_strings]

plt.xticks(x_ticks_loc,x_strings)
plt.xlim([0,3600])
plt.ylim([1.35,1.37])

#
plt.grid()
plt.tight_layout()
plt.savefig("phase_distort_nofilter_2_44GHz.pdf",dpi=600,bbox_inches = 'tight')
plt.show()


#%%
#MOVEMENT EVAL
sampl_rate = int(1e6)
decimation = int(1e4)
n_skip_samples = 0

#no movement in room during measurment 
#dir_name_1= "/home/marcin/GNU-Radio-USRP-Beamforming/phase_and_magnitude_correction/drift_eval/recorded/drift_meas_2_45G_1MSPS_10e4_decim_filtered_full_mav_eval/"

#with movement in room during measurment 
dir_name_1 = "/home/marcin/Desktop/phase_drift_eval/"

mag_file_names_1 = ["mag_corr_coeff_mav_1k_nofilter_log.bin","mag_corr_coeff_mav_10k_nofilter_log.bin","mag_corr_coeff_mav_100k_nofilter_log.bin","mag_corr_coeff_mav_1M_nofilter_log.bin","mag_corr_coeff_mav_10M_nofilter_log.bin"]

#pha_file_names_1 = ["phase_shift_coeff_mav_1k_nofilter_log.bin","phase_shift_coeff_mav_10k_nofilter_log.bin","phase_shift_coeff_mav_100k_nofilter_log.bin","phase_shift_coeff_mav_1M_nofilter_log.bin"]

pha_file_names_1 = ["phase_shift_coeff_mav_1k_nofilter_log.bin","phase_shift_coeff_mav_10k_nofilter_log.bin","phase_shift_coeff_mav_100k_nofilter_log.bin","phase_shift_coeff_mav_1M_nofilter_log.bin","phase_shift_coeff_mav_10M_nofilter_log.bin"]


mag_sampl_arr_list_1 = list()
mag_ss_vec_l_1 = list()
pha_sampl_arr_list_1 = list()
pha_ss_vec_l_1 = list()

n_files_each_1 = 4

#read
for f_idx in range(n_files_each_1):
    mag_sampl_arr, mag_ss_vec = read_data_file(dir_name_1 + mag_file_names_1[f_idx],sampl_rate,decimation)
    mag_sampl_arr_list_1.append(fw_replace_nan(np.array(mag_sampl_arr)))
    mag_ss_vec_l_1.append(mag_ss_vec)

for f_idx in range(n_files_each_1):
    pha_sampl_arr, pha_ss_arr = read_data_file(dir_name_1 + pha_file_names_1[f_idx],sampl_rate,decimation)
    pha_sampl_arr_list_1.append(fw_replace_nan(np.array(pha_sampl_arr)))
    pha_ss_vec_l_1.append(pha_ss_arr)
    
#trim
n_last_samples = 120*100
for f_idx in range(n_files_each_1):
    arr_mid = trim_data(mag_sampl_arr_list_1[f_idx], n_skip_samples)
    mag_sampl_arr_list_1[f_idx] = arr_mid

    arr_mid = trim_data(pha_sampl_arr_list_1[f_idx], n_skip_samples)
    pha_sampl_arr_list_1[f_idx] = arr_mid[-n_last_samples:]
print("\nFinished reading!\n")

#plot
fig, ax = plt.subplots()
plt.title("Phase correction coefficient in presence of movement")
props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
plot_data_with_stats_composite(fig, ax,pha_sampl_arr_list_1,pha_ss_vec_l_1)

plt.xlabel("Time [s]")

plt.legend(title = "MAV length",labels = ["1k", "10k", "100k","1M","10M"],loc ='lower right',ncol=6)

# x_ticks_loc =np.linspace(0,3600,7)
# x_ticks_val = (np.linspace(0,60,7))

# x_strings = ["%2.2f" % number for number in x_ticks_val]
# x_strings = [s.rstrip("0") for s in x_strings]
# x_strings = [s.rstrip(".") for s in x_strings]

#plt.xticks(x_ticks_loc,x_strings)
plt.xlim([0,120])
plt.ylim([1.25,1.45])

plt.grid()
plt.tight_layout()
plt.savefig("movement_ph_coeff.pdf",dpi=600,bbox_inches = 'tight')
plt.show()
