#Simple script performing phase and amplitude 
#correction and printing out calculation steps
#%%
import numpy

#create two signal samples of different amplitude and phase
ref_sig = complex(3,3)
sec_sig = complex (3,2)
print("Ref signal: %.2f  %.2fj" %(ref_sig.real, ref_sig.imag))
print("Sec signal: %.2f  %.2fj\n" %(sec_sig.real, sec_sig.imag))

#show angles of samples (arg)
ref_sig_ang = numpy.angle(ref_sig)
sec_signal_ang = numpy.angle(sec_sig)

ref_sig_mag = numpy.absolute(ref_sig)
sec_sig_mag = numpy.absolute(sec_sig)

print("Ref signal amplitude: %.2f, phase: %.2f" %(ref_sig_mag,ref_sig_ang))
print("Sec signal amplitude: %.2f, phase: %.2f\n" %(sec_sig_mag, sec_signal_ang))
#PHASE CORRECTION
print("PHASE CORRECTION\n")
#calculate conjungate of second signal
sec_conj = numpy.conj(sec_sig)
print("Sec signal conjugate: %.2f  %.2fj" %(sec_conj.real, sec_conj.imag))

#multiply conjugate with reference signal
mult_conjg = sec_conj*ref_sig
print("Multiply conjugate (with ref): %.2f  %.2fj" %(mult_conjg.real, mult_conjg.imag))

#calculate the shift angle corrections
conjg_arg = numpy.angle(mult_conjg)
print("Angle (arg) of conjugate: %.2f" %(conjg_arg))

#calculate the normalized coefficient (A = 1) to multiply the seconday signalS
phase_coeff = numpy.exp(1j*conjg_arg)
print("Phase corr coeff (normalized): %.2f  %.2fj\n" %(phase_coeff.real, phase_coeff.imag))

#correcting phase - multiply by phase corrector
shifted_sec_sig = phase_coeff*sec_sig
print("Shifted sec signal: %.2f  %.2fj" %(shifted_sec_sig.real, shifted_sec_sig.imag))

#calculate corrected signal params
shifted_sec_sig_angle = numpy.angle(shifted_sec_sig)
shifted_sec_sig_mag = numpy.absolute(shifted_sec_sig)
#print
ref_sig_mag = numpy.absolute(ref_sig)
print("Ref signal amplitude: \t\t\t%.2f, phase: %.2f" %(ref_sig_mag,ref_sig_ang))
print("Phase corrected sec signal amplitude: \t%.2f, phase: %.2f\n" %(shifted_sec_sig_mag, shifted_sec_sig_angle))

#AMPLITUDE CORRECTION
#*** Simplification - REF signal is considered to always have the greates amplitude, in any other case first perform search for maximum and mark it as reference
print("AMPLITUDE CORRECTION\n")

#calculate magnitude correction coefficient
mag_coeff = (ref_sig_mag-sec_sig_mag)/sec_sig_mag + 1

print("Amplitude corr coeff %.2f\n" %(mag_coeff))
#muliply sec signal by coeff
amplified_sec_sig = mag_coeff*shifted_sec_sig

#calculate corrected signal params
amplified_sec_sig_angle = numpy.angle(amplified_sec_sig)
amplified_sec_sig_mag = numpy.absolute(amplified_sec_sig)
#print
ref_sig_mag = numpy.absolute(ref_sig)
print("Ref signal amplitude: \t\t\t%.2f, phase: %.2f" %(ref_sig_mag,ref_sig_ang))
print("Phase corrected sec signal amplitude: \t%.2f, phase: %.2f\n" %(amplified_sec_sig_mag, amplified_sec_sig_angle))
