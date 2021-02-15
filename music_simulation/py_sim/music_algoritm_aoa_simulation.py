#Scipts performing MUSIC algorithm, plotting pseudospectrum,
#running parametric and statistical (Monte-Carlo) analyses
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
#Functions:
#generate signal autocorrelation matrix - forward averaging
def autocorrelate(signals_mat,snap_size):
    return 1.0/snap_size*np.transpose(signals_mat)@np.conjugate(signals_mat)

#generate signal autocorrelation matrix - forward-backward averaging
def autocorrelate_fb(signals_mat,snap_size):
    d_J = np.eye(signals_mat.shape[1],signals_mat.shape[1])
    d_J = np.fliplr(d_J)
    out_matrix = 1.0/snap_size*np.transpose(signals_mat)@np.conjugate(signals_mat)
    return 0.5*out_matrix+(0.5/snap_size)*d_J@np.conjugate(out_matrix)@d_J

#antenna array creation, equally placed around zero
def gen_antenna_vec(lambda_separation,n_rx):
    return np.linspace(-(n_rx-1)*lambda_separation/2,(n_rx-1)*lambda_separation/2,n_rx)
    
    #CPP: ant_loc = np.zeros(n_rx)
    #CPP: for j in range (n_rx):
    #CPP:    ant_loc[j] = ant_separation*0.5*(n_rx-1-2*j)

#generate theta angles for evaluation in range of 0-180deg
def gen_theta_vector (pspec_length):
    return np.linspace(0,np.pi,pspec_length)

    #generate theta vector
    #CPP: d_theta = np.zeros(pspec_length,dtype=float)
    #CPP: d_theta[0] = 0.0
    #CPP: theta_prev = 0.0
    #CPP: for k in range(1,pspec_length):
    #CPP:     theta = theta_prev+180.0/pspec_length
    #CPP:     theta_prev = theta
    #CPP:     d_theta[k] = np.pi*theta/180.0

#array response matrix formation
def gen_array_response_mat(pspec_length,n_rx,theta_vec,antenna_vec):
    vii_temp = np.zeros(n_rx)
    arr_resp_mat = np.ndarray([pspec_length,n_rx],dtype=complex)
    arr_resp_mat_trans = np.ndarray([n_rx, pspec_length],dtype=complex)
    for ii in range (pspec_length):
        vii_temp = np.exp(-1j*2*np.pi*np.cos(theta_vec[ii])*antenna_vec)
        arr_resp_mat[ii,:]=vii_temp

    arr_resp_mat_trans = arr_resp_mat.conj().T

    return arr_resp_mat, arr_resp_mat_trans

#core MUSIC algorithm
def calc_aoa_music(n_sources,n_rx,autocorr_mat,arr_resp_mat,arr_resp_mat_trans):
    #determine EVD of the auto-correlation matrix
    eig_val,eig_vect =np.linalg.eig(autocorr_mat)
    # noise subspace
    U_N = eig_vect[:,n_sources:n_rx] 
    #CPP: eig_vec.cols(0, d_num_ant_ele-d_num_targets-1);
    U_N_sq =U_N@(U_N.conj().T)
    #determine pseudo-spectrum for each value of theta in [0.0, 180.0)
    pspec_out_vec = np.zeros(pspec_length,dtype=float)
    
    for ii in range(pspec_length):
        Q_temp = arr_resp_mat_trans[:,ii]@U_N_sq@arr_resp_mat[ii,:]
        pspec_out_vec[ii] = 1.0/(Q_temp.real)

        #null-spectrum
        #pspec_out_vec[ii] = Q_temp.real

    pspec_out_vec = 10.0*np.log10(pspec_out_vec/np.max(pspec_out_vec))

    return pspec_out_vec

#calculate array response vector coefficients for specified theta
def array_response_vector(antena_vec,theta):
    return np.exp(-1j*2*np.pi*antena_vec*np.cos(theta))

#create real case sinusoidal signal with ADC params (redundant)
def gen_real_case_signal():
    #Generate signals based on provided params:
    #TO DO:
    #+add automatic phase offset calculation for specified AOA
    #+add mulitple signals (more harmonics at different angles)
    #+(optional)add phase noise 
    #+IQ imbalance?
    #signal (single harmonic wave)
    sig_freq = 1e3  
    #print("Signal frequency after downconversion: %d [Hz]"%(sig_freq))
    #sample rate
    sampl_rate = 1e5
    #print("RX sample rate: %d"%(sampl_rate))
    snap_size = 1024
    #print("Snapshot size: %d"%(snap_size))
    obs_time_len = snap_size/sampl_rate
    #print("Resultant observation time: %.3f ms"%(1000*obs_time_len))

    #angle vector values
    angle_vec = 2*np.pi*sig_freq*np.linspace(0,obs_time_len,snap_size)
    #timestep vector values
    time_vec = np.linspace(0,snap_size/sampl_rate, snap_size)
    n_rx = 2
    snap_size = 1024
    ampl_diff_vec = np.array([1,1])
    #print("Amplitude coefficients vector:", ampl_diff_vec)
    phase_diff_vec = np.array([0,0.7*np.pi])
    #print("Phase coefficients vector:", phase_diff_vec)

    add_noise_flag = True
    sig_mat = np.ndarray([snap_size,n_rx],dtype=complex)

    for idx in range(n_rx):
        cx_signal_vec = np.array((ampl_diff_vec[idx]*np.cos(angle_vec+phase_diff_vec[idx])+(1j*ampl_diff_vec[idx]*np.sin(angle_vec+phase_diff_vec[idx]))))
        
        if add_noise_flag: 
            awgn = np.random.normal(0, 0.05, snap_size)+(1j*np.random.normal(0, 0.05, snap_size))
            cx_signal_vec = cx_signal_vec+awgn

        sig_mat[:,idx] = cx_signal_vec
    """
    plt.figure(1)
    plt.xlabel("Time [s]")
    plt.subplot(211)
    plt.title("Signals in time")
    plt.plot(time_vec,np.real(sig_mat[:,0]),label = "Real")
    plt.plot(time_vec,np.imag(sig_mat[:,0]),label = "Imag")
    plt.legend()
    plt.subplot(212)
    plt.plot(time_vec,np.real(sig_mat[:,1]),label = "Real")
    plt.plot(time_vec,np.imag(sig_mat[:,1]),label = "Imag")
    plt.xlabel("Time [s]")
    plt.legend()
    plt.show()
    """
    return sig_mat

    # N = array.shape()
    # v = np.exp(-1j*2*np.pi*array*np.cos(theta))
    # return v/np.sqrt(N)

#create artificial testing signal 
def gen_signals_mat(n_rx,antenna_vec, n_sources, n_samples, source_theta_vec = None,source_power_vec = None,power_diff_vec = None, snr_db = float('inf'),print_params = False):
    
    if (source_theta_vec is None):
         # random source directions
        source_theta_vec = np.pi*(np.random.rand(n_sources))
    
    if (source_power_vec is None):
        # random source powers
        source_power_vec = np.sqrt(1/2)*(np.random.randn(n_sources) + np.random.randn(n_sources)*1j) 
    
    if (power_diff_vec is None):
        power_diff_vec = np.ones(n_rx)

    if(print_params == True):
        print("Sources theta: ",source_theta_vec)
        print("Sources power: ", abs(source_power_vec))
        print("RX node power diff coefficient: ", power_diff_vec )
    
    #generate signal samples
    signals_mat = np.zeros((n_samples,n_rx),dtype=complex)
    for sample_idx in range(n_samples):
        array_sync_sample_vec = np.zeros(n_rx)
        for source_idx in range(n_sources):
            phase = np.exp(1j*2*np.pi*np.random.randn(1))
            array_sync_sample_vec = array_sync_sample_vec + phase*source_power_vec[source_idx]*array_response_vector(antenna_vec,source_theta_vec[source_idx])
        signals_mat[sample_idx,:] = array_sync_sample_vec 
    #add white gaussian noise
    for sample_vec_idx in range(signals_mat.shape[1]):
         signals_mat[:,sample_vec_idx] = add_awgn_vec( signals_mat[:,sample_vec_idx],snr_db)

    power_diff_vec = np.array(power_diff_vec)
    signals_mat = signals_mat*power_diff_vec.T
    return signals_mat, source_theta_vec

def rmse(predictions, target):
    return np.sqrt(((predictions - target) ** 2).mean())

def add_awgn_vec(in_vec,snr_db):
    sig_pow = np.sum(np.square(np.abs(in_vec))) / len(in_vec)
    noise_pow = sig_pow / 10**(snr_db/10)
    imp = 1 #assuming impedance is 1 Ohm
    noise_vec = (np.sqrt(imp*noise_pow/2))*(np.random.randn(len(in_vec))+1j*np.random.randn(len(in_vec)))

    #print("In vec var:", np.var(in_vec))
    #print("Noise vec var:", np.var(noise_vec))
    #print("SNR [dB]:", 10*np.log10(np.var(in_vec)/np.var(noise_vec)))
    return in_vec + noise_vec

print("\nFinished declaring functions!\n")

#%%
#Music algorithm simulation - reference run

#rng seed
np.random.seed(5)
n_sources = 2               # number of sources
n_rx = 4                    # number of ULA elements 
snr = 10                    # signal to noise ratio
antenna_separation = 0.5    #
pspec_length = 1800         #
n_samples = 1024            #

#antenna vector creation
antenna_vec = gen_antenna_vec(antenna_separation,n_rx)
#print("Antenna vector: ", antenna_vec)
theta_vec = gen_theta_vector(pspec_length)
#print("Theta vector: ", theta_vec)

arr_response_mat, arr_response_mat_trans = gen_array_response_mat(pspec_length,n_rx,theta_vec,antenna_vec)

#custom source powers, thetas and power reception diffs
source_theta_vec = np.radians(np.array([50, 120]))
source_power_vec = np.array([1, 1])
power_diff_vec = np.array([1, 1, 1, 1])

#generate signal 
sig_mat, source_theta_vec = gen_signals_mat(n_rx,antenna_vec,n_sources,n_samples,source_theta_vec,source_power_vec,power_diff_vec,snr)

#generate autocorrelation matrix (n_inputs x n_inputs)
#print("Autocorrelation matrix shape: ",acorr_sig_mat.shape)
autocorr_mat = np.ndarray([n_rx,n_rx],dtype=complex)
autocorr_mat = autocorrelate(sig_mat,n_samples)
pspec_vec = calc_aoa_music(n_sources,n_rx,autocorr_mat,arr_response_mat,arr_response_mat_trans)

plt.plot(np.degrees(theta_vec),pspec_vec,label ='_nolegend_')
#plot reference - real theta values vertical lines 
for source_theta_val in source_theta_vec:
    plt.axvline(np.degrees(source_theta_val),linewidth = 0.5, color='k')
plt.xlim(0.0,180.0)
plt.title("MUSIC algorithm pseudospectrum")
plt.xlabel("Angle of arrival [°]")
plt.ylabel("Power [dB]")
plt.legend(["Real AoA"])
plt.tight_layout()
plt.savefig("aoa_sim.pdf",dpi=600,bbox_inches = 'tight')
plt.show()


#%%
#SNR SWEEP 

#rng seed
np.random.seed(5)
n_sources = 2               # number of sources
n_rx = 4                    # number of ULA elements 
snr = 10                    # signal to noise ratio
antenna_separation = 0.5    #
pspec_length = 1800         #
n_samples = 1024            #

#antenna vector creation
antenna_vec = gen_antenna_vec(antenna_separation,n_rx)
#print("Antenna vector: ", antenna_vec)
theta_vec = gen_theta_vector(pspec_length)
#print("Theta vector: ", theta_vec)

arr_response_mat, arr_response_mat_trans = gen_array_response_mat(pspec_length,n_rx,theta_vec,antenna_vec)

#custom source powers, thetas and power reception diffs
source_theta_vec = np.radians(np.array([50, 120]))
source_power_vec = np.array([1, 1])

snr_vec = [-10, 0, 10]
for snr_val in snr_vec:
    #generate signal 
    sig_mat, source_theta_vec = gen_signals_mat(n_rx,antenna_vec,n_sources,n_samples,source_theta_vec,source_power_vec,None,snr_val)

    #generate autocorrelation matrix (n_inputs x n_inputs)
    #print("Autocorrelation matrix shape: ",acorr_sig_mat.shape)
    autocorr_mat = np.ndarray([n_rx,n_rx],dtype=complex)
    autocorr_mat = autocorrelate(sig_mat,n_samples)

    pspec_vec = calc_aoa_music(n_sources,n_rx,autocorr_mat,arr_response_mat,arr_response_mat_trans)

    plt.plot(np.degrees(theta_vec),pspec_vec,label ='%d' %snr_val)
    #plot reference - real theta values vertical lines 
for source_theta_val in source_theta_vec:
    plt.axvline(np.degrees(source_theta_val),linewidth = 0.5, color='k')
plt.xlim(0.0,180.0)

plt.title("MUSIC algorithm pseudospectrum")
plt.xlabel("Angle of arrival [°]")
plt.ylabel("Power [dB]")
plt.legend(loc = "lower right",title = "SNR [dB]")
plt.tight_layout()
plt.savefig("aoa_sim_snr_sweep.pdf",dpi=600,bbox_inches = 'tight')
plt.show()

#%%
#N antennas SWEEP

#rng seed
np.random.seed(5)
n_sources = 2               # number of sources
n_rx = 4                    # number of ULA elements 
snr = 10                    # signal to noise ratio
antenna_separation = 0.5    #
pspec_length = 1800         #
n_samples = 1024            #

ant_num_vec = [4,8,16]        # number of ULA elements 
for n_rx in ant_num_vec:
        
    #antenna vector creation
    antenna_vec = gen_antenna_vec(antenna_separation,n_rx)
    #print("Antenna vector: ", antenna_vec)
    theta_vec = gen_theta_vector(pspec_length)
    #print("Theta vector: ", theta_vec)

    arr_response_mat, arr_response_mat_trans = gen_array_response_mat(pspec_length,n_rx,theta_vec,antenna_vec)

    #custom source powers, thetas and power reception diffs
    source_theta_vec = np.radians(np.array([50,120]))
    source_power_vec = np.array([1,1])
    power_diff_vec = np.array([1, 1, 1, 1])

    #generate signal 
    sig_mat, source_theta_vec = gen_signals_mat(n_rx,antenna_vec,n_sources,n_samples,source_theta_vec,source_power_vec,None,snr)

    #generate autocorrelation matrix (n_inputs x n_inputs)
    #print("Autocorrelation matrix shape: ",acorr_sig_mat.shape)
    autocorr_mat = np.ndarray([n_rx,n_rx],dtype=complex)
    autocorr_mat = autocorrelate_fb(sig_mat,n_samples)

    pspec_vec = calc_aoa_music(n_sources,n_rx,autocorr_mat,arr_response_mat,arr_response_mat_trans)

    plt.plot(np.degrees(theta_vec),pspec_vec,label ='%d' %n_rx)


#plot reference - real theta values vertical lines 
for source_theta_val in source_theta_vec:
    plt.axvline(np.degrees(source_theta_val),linewidth = 0.5, color='k')
plt.xlim(0.0,180.0)

plt.title("MUSIC algorithm pseudospectrum")
plt.xlabel("Angle of arrival [°]")
plt.ylabel("Power [dB]")
plt.legend(loc = "lower right",title = "N antennas")
plt.tight_layout()
plt.savefig("aoa_sim_n_rx_sweep.pdf",dpi=600,bbox_inches = 'tight')
plt.show()


#%%
#SNAPSHOT LENGTH SWEEP

#rng seed
np.random.seed(5)
n_sources = 2               # number of sources
snr = 10                    # signal to noise ratio
n_rx = 4                    # number of ULA elements 
antenna_separation = 0.5    #
pspec_length = 1800         #

n_samples_vec =[10,100,1000]#

for snap_size in n_samples_vec:
        
    #antenna vector creation
    antenna_vec = gen_antenna_vec(antenna_separation,n_rx)
    #print("Antenna vector: ", antenna_vec)
    theta_vec = gen_theta_vector(pspec_length)
    #print("Theta vector: ", theta_vec)

    arr_response_mat, arr_response_mat_trans = gen_array_response_mat(pspec_length,n_rx,theta_vec,antenna_vec)

    #custom source powers, thetas and power reception diffs
    source_theta_vec = np.radians(np.array([50, 120]))
    source_power_vec = np.array([1, 1])
    power_diff_vec = np.array([1, 1, 1, 1])

    #generate signal 
    sig_mat, source_theta_vec = gen_signals_mat(n_rx,antenna_vec,n_sources,snap_size,source_theta_vec,source_power_vec,None,snr)

    #generate autocorrelation matrix (n_inputs x n_inputs)
    #print("Autocorrelation matrix shape: ",acorr_sig_mat.shape)
    autocorr_mat = np.ndarray([n_rx,n_rx],dtype=complex)
    autocorr_mat = autocorrelate(sig_mat,n_samples)

    pspec_vec = calc_aoa_music(n_sources,n_rx,autocorr_mat,arr_response_mat,arr_response_mat_trans)

    plt.plot(np.degrees(theta_vec),pspec_vec,label ='%d' %snap_size)


#plot reference - real theta values vertical lines 
for source_theta_val in source_theta_vec:
    plt.axvline(np.degrees(source_theta_val),linewidth = 0.5, color='k')
plt.xlim(0.0,180.0)

plt.title("MUSIC algorithm pseudospectrum")
plt.xlabel("Angle of arrival [°]")
plt.ylabel("Power [dB]")
plt.legend(loc = "lower right",title = "Snapshot length")
plt.tight_layout()
plt.savefig("aoa_snap_size_sweep.pdf",dpi=600,bbox_inches = 'tight')
plt.show()


#%%
#ANTENNA SPACING SWEEP
#rng seed
np.random.seed(5)

n_sources = 2               # number of sourceszz
snr = 10                    # signal to noise ratio
n_rx = 8                    # number of ULA elements 
pspec_length = 1800        #
n_samples = 1024            #

ant_sep_list =[0.4,0.5,0.6]#

for ant_sep in ant_sep_list:
        
    #antenna vector creation
    antenna_vec = gen_antenna_vec(ant_sep,n_rx)
    #print("Antenna vector: ", antenna_vec)
    theta_vec = gen_theta_vector(pspec_length)
    #print("Theta vector: ", theta_vec)

    arr_response_mat, arr_response_mat_trans = gen_array_response_mat(pspec_length,n_rx,theta_vec,antenna_vec)

    #custom source powers, thetas and power reception diffs
    source_theta_vec = np.radians(np.array([20, 30]))
    source_power_vec = np.array([1, 1])
    power_diff_vec = np.array([1, 1, 1, 1])

    #generate signal 
    sig_mat, source_theta_vec = gen_signals_mat(n_rx,antenna_vec,n_sources,n_samples,source_theta_vec,source_power_vec,None,snr)

    #generate autocorrelation matrix (n_inputs x n_inputs)
    #print("Autocorrelation matrix shape: ",acorr_sig_mat.shape)
    autocorr_mat = np.ndarray([n_rx,n_rx],dtype=complex)
    autocorr_mat = autocorrelate(sig_mat,n_samples)

    pspec_vec = calc_aoa_music(n_sources,n_rx,autocorr_mat,arr_response_mat,arr_response_mat_trans)

    plt.plot(np.degrees(theta_vec),pspec_vec,label ='%1.1f' %ant_sep)


#plot reference - real theta values vertical lines 
for source_theta_val in source_theta_vec:
    plt.axvline(np.degrees(source_theta_val),linewidth = 0.5, color='k')
plt.xlim(0.0,180.0)

plt.title("MUSIC algorithm pseudospectrum")
plt.xlabel("Angle of arrival [°]")
plt.ylabel("Power [dB]")
plt.legend(loc = "lower right",title="RX spacing [$\lambda$]")
plt.tight_layout()
plt.savefig("aoa_ant_sep_sweep.pdf",dpi=600,bbox_inches = 'tight')
plt.show()

#%%
#EVAL OF RX POWER DIFFERENCES

np.random.seed(5)
n_sources = 2               # number of sources
n_rx = 4                    # number of ULA elements 
snr = 10                    # signal to noise ratio
antenna_separation = 0.5    #
pspec_length = 1800         #
n_samples = 1024            #

#antenna vector creation
antenna_vec = gen_antenna_vec(antenna_separation,n_rx)
#print("Antenna vector: ", antenna_vec)
theta_vec = gen_theta_vector(pspec_length)
#print("Theta vector: ", theta_vec)

arr_response_mat, arr_response_mat_trans = gen_array_response_mat(pspec_length,n_rx,theta_vec,antenna_vec)

rx_power_coeff_vec = np.linspace(0.5,1.5,5)
source_theta_vec = np.radians(np.array([110, 120]))
source_power_vec = np.array([0.8,1.2])

for rx_power_coeff in rx_power_coeff_vec:
    power_diff_vec = np.array([rx_power_coeff, 1, 1, 1])
    #generate signal 
    sig_mat, source_theta_vec = gen_signals_mat(n_rx,antenna_vec,n_sources,n_samples,source_theta_vec,source_power_vec,None,snr)

    #generate autocorrelation matrix (n_inputs x n_inputs)
    #print("Autocorrelation matrix shape: ",acorr_sig_mat.shape)
    autocorr_mat = np.ndarray([n_rx,n_rx],dtype=complex)
    autocorr_mat = autocorrelate(sig_mat,n_samples)
    pspec_vec = calc_aoa_music(n_sources,n_rx,autocorr_mat,arr_response_mat,arr_response_mat_trans)

    plt.plot(np.degrees(theta_vec),pspec_vec,linewidth = 1, label ='%1.2f' % rx_power_coeff)

for source_theta_val in source_theta_vec:
    tmp = plt.axvline(np.degrees(source_theta_val),linewidth = 0.5, color='k')
tmp.set_label("Real AoA")
plt.xlim(0.0,180.0)

plt.title("MUSIC algorithm pseudospectrum")
plt.xlabel("Angle of arrival [angle]")
plt.ylabel("Power [dB]")
plt.legend(title="RX1 power coefficient:",loc='upper right')
plt.tight_layout()
plt.show()

#%%
#SNR VS RMSE ERROR MONTE CARLO SIMULATION

#rng seed
np.random.seed(5)
n_sources = 1               # number of sources
n_rx = 4                    # number of ULA elements 
snr = 10                    # signal to noise ratio
antenna_separation = 0.5    #
pspec_length = 18000        #
n_samples = 1024            #

#antenna vector creation
antenna_vec = gen_antenna_vec(antenna_separation,n_rx)
#print("Antenna vector: ", antenna_vec)
theta_vec = gen_theta_vector(pspec_length)
#print("Theta vector: ", theta_vec)

arr_response_mat, arr_response_mat_trans = gen_array_response_mat(pspec_length,n_rx,theta_vec,antenna_vec)

#custom source powers, thetas and power reception diffs
angles = [50]
source_theta_vec = np.radians(np.array(angles))
source_power_vec = np.array([1])
power_diff_vec = np.array([1,1,1,1])

n_runs = 500
snr_vec = np.arange(-15,31,1,dtype='int32')
print(snr_vec)

rmse_arr = np.ndarray(len(snr_vec))
for snr_idx in range(len(snr_vec)):
    aoa_estimate = np.ndarray(n_runs)

    for run_idx in range (n_runs):
        #generate signal 
        sig_mat, source_theta_vec = gen_signals_mat(n_rx,antenna_vec,n_sources,n_samples,source_theta_vec,source_power_vec,power_diff_vec,snr_vec[snr_idx])

        #generate autocorrelation matrix (n_inputs x n_inputs)
        #print("Autocorrelation matrix shape: ",acorr_sig_mat.shape)
        autocorr_mat = np.ndarray([n_rx,n_rx],dtype=complex)
        autocorr_mat = autocorrelate(sig_mat,n_samples)

        pspec_vec = calc_aoa_music(n_sources,n_rx,autocorr_mat,arr_response_mat,arr_response_mat_trans)
        peak = np.argmax(pspec_vec)/100
        aoa_estimate[run_idx] = peak
    rmse_arr[snr_idx] = rmse(aoa_estimate,angles[0])

fig, ax = plt.subplots()
plt.plot(snr_vec,rmse_arr,'.-')
plt.yscale('log',basey=2)
ax.yaxis.set_major_formatter(ScalarFormatter())
ax.xaxis.set_major_formatter(ScalarFormatter())

x_tick_vals = np.linspace(-15,30,10)
ax.set_xticks(x_tick_vals)

y_tick_vals = np.power(2,np.linspace(-5,1,7))
print(y_tick_vals)
y_strings = ["%1.5f" % number for number in y_tick_vals]
y_strings = [s.rstrip("0") for s in y_strings]
y_strings = [s.rstrip(".") for s in y_strings]

plt.yticks(y_tick_vals,y_strings)
# # tick_vals = np.power(2,np.linspace(1,10,10))
# # ax.set_xticks(tick_vals)
# # ax.set_xticklabels(tick_vals)

plt.xlim([-20,35])

plt.title("Angle estimation error in regard to signal to noise ratio")
plt.xlabel("Signal to noise ratio [dB]")
plt.ylabel("RMSE of esitmation [°]")
plt.grid(which="both", ls="-")
plt.tight_layout()
plt.savefig("aoa_sim_snr_rmse.pdf",dpi=600,bbox_inches = 'tight')
plt.show()


#%%
#SNAPSHOT LENGTH  VS RMSE ERROR MONTE CARLO SIMULATION

#rng seed
np.random.seed(5)
n_sources = 1               # number of sources
n_rx = 4                    # number of ULA elements 
snr = 10                    # signal to noise ratio
antenna_separation = 0.5    #
pspec_length = 1800         #
n_samples = 1024            #

#antenna vector creation
antenna_vec = gen_antenna_vec(antenna_separation,n_rx)
#print("Antenna vector: ", antenna_vec)
theta_vec = gen_theta_vector(pspec_length)
#print("Theta vector: ", theta_vec)

arr_response_mat, arr_response_mat_trans = gen_array_response_mat(pspec_length,n_rx,theta_vec,antenna_vec)

#custom source powers, thetas and power reception diffs
angles = [50]
source_theta_vec = np.radians(np.array(angles))
source_power_vec = np.array([1])
power_diff_vec = np.array([1,1,1,1])

n_runs = 500
snap_len_vec = np.unique(np.logspace(2,10,50,base=2,dtype='int32'))
rmse_arr = np.ndarray(len(snap_len_vec))

def rmse(predictions, target):
    return np.sqrt(((predictions - target) ** 2).mean())

for snap_idx in range(len(snap_len_vec)):
    aoa_estimate = np.ndarray(n_runs)

    for run_idx in range (n_runs):
        #generate signal 
        sig_mat, source_theta_vec = gen_signals_mat(n_rx,antenna_vec,n_sources,snap_len_vec[snap_idx],source_theta_vec,source_power_vec,power_diff_vec,snr)

        #generate autocorrelation matrix (n_inputs x n_inputs)
        #print("Autocorrelation matrix shape: ",acorr_sig_mat.shape)
        autocorr_mat = np.ndarray([n_rx,n_rx],dtype=complex)
        autocorr_mat = autocorrelate(sig_mat,snap_len_vec[snap_idx])

        pspec_vec = calc_aoa_music(n_sources,n_rx,autocorr_mat,arr_response_mat,arr_response_mat_trans)
        peak = np.argmax(pspec_vec)/10
        aoa_estimate[run_idx] = peak
    rmse_arr[snap_idx] = rmse(aoa_estimate,angles[0])

fig, ax = plt.subplots()
plt.loglog(snap_len_vec,rmse_arr,'.-',base = 2)

ax.yaxis.set_major_formatter(ScalarFormatter())
ax.xaxis.set_major_formatter(ScalarFormatter())

x_tick_vals = np.power(2,np.linspace(1,11,11))
ax.set_xticks(x_tick_vals)

y_tick_vals = np.power(2,np.linspace(-3,3,7))

y_strings = ["%1.3f" % number for number in y_tick_vals]
y_strings = [s.rstrip("0") for s in y_strings]
y_strings = [s.rstrip(".") for s in y_strings]

plt.yticks(y_tick_vals,y_strings)
tick_vals = np.power(2,np.linspace(1,10,10))
ax.set_xticks(tick_vals)

plt.xlim([2,2048])
plt.ylim([0.125,8])

plt.title("Angle estimation error in regard to snapshot length")
plt.xlabel("Length of snapshot")
plt.ylabel("RMSE of esitmation [°]")
plt.grid(which="both", ls="-")
plt.tight_layout()
plt.savefig("aoa_sim_snap_rmse.pdf",dpi=600,bbox_inches = 'tight')
plt.show()


#%%
#ANTENNA SPACING VS RMSE ERROR MONTE CARLO SIMULATION

#rng seed
np.random.seed(5)
n_sources = 1              # number of sources
n_rx = 4                    # number of ULA elements 
snr = 10                    # signal to noise ratio
antenna_separation = 0.5    #
pspec_length = 1800        #
n_samples = 1024            #

angles = [15]
source_theta_vec = np.radians(np.array(angles))
source_power_vec = np.array([1])
power_diff_vec = None

#monte carlo analysis
n_runs = 500
fig, ax = plt.subplots()
ant_arr_spacing_vec = 0.5*np.logspace(-1,0,50)
rmse_arr = np.ndarray(len(ant_arr_spacing_vec))

def rmse(predictions, target):
    return np.sqrt(((predictions - target) ** 2).mean())

for spacing_idx in range(len(ant_arr_spacing_vec)):
    aoa_estimate = np.ndarray(n_runs)
    ant_spacing_tmp = ant_arr_spacing_vec[spacing_idx]

    #antenna vector creation
    antenna_vec = gen_antenna_vec(ant_spacing_tmp,n_rx)
    #print("Antenna vector: ", antenna_vec)
    theta_vec = gen_theta_vector(pspec_length)
    #print("Theta vector: ", theta_vec)

    arr_response_mat, arr_response_mat_trans = gen_array_response_mat(pspec_length,n_rx,theta_vec,antenna_vec)

    for run_idx in range (n_runs):
        #generate signal 
        sig_mat, source_theta_vec = gen_signals_mat(n_rx,antenna_vec,n_sources,n_samples,source_theta_vec,source_power_vec,power_diff_vec,snr)

        #generate autocorrelation matrix (n_inputs x n_inputs)
        #print("Autocorrelation matrix shape: ",acorr_sig_mat.shape)
        autocorr_mat = np.ndarray([n_rx,n_rx],dtype=complex)
        autocorr_mat = autocorrelate(sig_mat,n_samples)

        pspec_vec = calc_aoa_music(n_sources,n_rx,autocorr_mat,arr_response_mat,arr_response_mat_trans)

        peak = np.argmax(pspec_vec)/10
        aoa_estimate[run_idx] = peak
    rmse_arr[spacing_idx] = rmse(aoa_estimate,angles[0])

plt.loglog(ant_arr_spacing_vec,rmse_arr,'.-',base=2)

ax.yaxis.set_major_formatter(ScalarFormatter())
ax.xaxis.set_major_formatter(ScalarFormatter())

x_tick_vals = np.power(2,np.linspace(-4,-1,4))
plt.xticks(x_tick_vals,x_tick_vals)

y_tick_vals = np.power(2,np.linspace(-1,3,5))

y_strings = ["%1.3f" % number for number in y_tick_vals]
y_strings = [s.rstrip("0") for s in y_strings]
y_strings = [s.rstrip(".") for s in y_strings]

plt.yticks(y_tick_vals,y_strings)

plt.ylim([0.25,16])
plt.xlim([0.04,0.75])

plt.title("Angle estimation error in regard to antenna spacing")
plt.xlabel("Antenna spacing $[\lambda]$")
plt.ylabel("RMSE of esitmation [°]")
plt.grid(which="both", ls="-")
plt.tight_layout()
plt.savefig("aoa_sim_ant_spacing_rmse.pdf",dpi=600,bbox_inches = 'tight')
plt.show()

#%%
#Music POWER DIFF MONTE CARLO SIMULATION
#rng seed
np.random.seed(5)

n_sources = 1              # number of sources
n_rx = 4                    # number of ULA elements 
snr = 10                    # signal to noise ratio
antenna_separation = 0.5    #
pspec_length = 1800         #
n_samples = 1024            #

angles = [15]
source_theta_vec = np.radians(np.array(angles))
source_power_vec = np.array([1])

#monte carlo analysis
n_runs = 50
fig, ax = plt.subplots()
ant_spacing  = 0.5

pow_vec = np.linspace(0.1,2,30)
rmse_arr = np.ndarray(len(pow_vec))

def rmse(predictions, target):
    return np.sqrt(((predictions - target) ** 2).mean())

for pow_idx in range(len(pow_vec)):
    ampl_val = pow_vec[pow_idx]
    power_diff_vec = [ampl_val,1,1,1]

    aoa_estimate = np.ndarray(n_runs)

    #antenna vector creation
    antenna_vec = gen_antenna_vec(ant_spacing,n_rx)
    #print("Antenna vector: ", antenna_vec)
    theta_vec = gen_theta_vector(pspec_length)
    #print("Theta vector: ", theta_vec)

    arr_response_mat, arr_response_mat_trans = gen_array_response_mat(pspec_length,n_rx,theta_vec,antenna_vec)

    for run_idx in range (n_runs):
        #generate signal 
        sig_mat, source_theta_vec = gen_signals_mat(n_rx,antenna_vec,n_sources,n_samples,source_theta_vec,source_power_vec,power_diff_vec,snr)

        #generate autocorrelation matrix (n_inputs x n_inputs)
        #print("Autocorrelation matrix shape: ",acorr_sig_mat.shape)
        autocorr_mat = np.ndarray([n_rx,n_rx],dtype=complex)
        autocorr_mat = autocorrelate(sig_mat,n_samples)

        pspec_vec = calc_aoa_music(n_sources,n_rx,autocorr_mat,arr_response_mat,arr_response_mat_trans)

        peak = np.argmax(pspec_vec)/100
        aoa_estimate[run_idx] = peak
    rmse_arr[pow_idx] = rmse(aoa_estimate,angles[0])

print("FINISHED!")

plt.loglog(pow_vec**2,rmse_arr,'.-')

x_tick_vals = np.power(2,np.linspace(-4,-1,4))
plt.xticks(x_tick_vals,x_tick_vals)

y_tick_vals = np.power(2,np.linspace(-1,3,5))

y_strings = ["%1.3f" % number for number in y_tick_vals]
y_strings = [s.rstrip("0") for s in y_strings]
y_strings = [s.rstrip(".") for s in y_strings]

plt.yticks(y_tick_vals,y_strings)

plt.ylim([0.25,16])
plt.xlim([0.04,0.75])

plt.title("Angle estimation error in regard to antenna spacing")
plt.xlabel("Antenna spacing $[\lambda]$")
plt.ylabel("RMSE of esitmation [°]")
plt.grid(which="both", ls="-")
plt.tight_layout()
plt.savefig("pow_diff.pdf",dpi=600,bbox_inches = 'tight')
plt.show()