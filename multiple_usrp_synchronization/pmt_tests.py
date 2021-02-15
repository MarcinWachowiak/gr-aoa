#%%
import gnuradio
import pmt

print("GNU Radio PMT test")

cmd = pmt.make_dict()
cmd = pmt.dict_add(cmd, pmt.intern("time"), pmt.from_long(10))
cmd = pmt.dict_add(cmd, pmt.intern("freq"), pmt.from_double(94.6e+6))

print(cmd)

cmd = pmt.dict_add(cmd, pmt.intern("time"), pmt.PMT_NIL)

print(cmd)

# %%
