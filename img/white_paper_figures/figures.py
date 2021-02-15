#%%
#Recreate figures in latex publication style from following white papers:
#https://www.ericsson.com/en/mobility-report/reports/november-2020
#https://www.cisco.com/c/en/us/solutions/collateral/executive-perspectives/annual-internet-report/white-paper-c11-741490.html

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
#plot user growth
y_usr = [5.1,5.2,5.3,5.5,5.6,5.7]
x_years = [2018,2019,2020,2021,2022,2023]

fig, ax = plt.subplots()

plt.bar(x_years,y_usr,width=0.65, alpha=.75)

ax.set_axisbelow(True)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.tick_params(axis=u'both', which=u'both',length=0)
plt.title("Predicted mobile user growth")
plt.ylabel("Billions of mobile subscribers")
plt.xlabel("Year")
plt.ylim([4.6,5.8])
plt.tight_layout()
plt.grid(axis='y')
plt.savefig("cisco_mobile_usr_growth.pdf", dpi=600,bbox_inches = 'tight')
plt.show()

#%%
#plot mobile traffic growth
y_rest = [4,8,15,24,34,48,62,74,86,94,100,106]
y_5g =   [0,0,0,0,0,4,8,20,34,56,88,124]
x_years = np.arange(2015,2027,1)

fig, ax = plt.subplots()

plt.stackplot(x_years,y_rest,y_5g, alpha=.75)

ax.set_axisbelow(True)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.tick_params(axis=u'both', which=u'both',length=0)
plt.title("Global mobile traffic prediction")
plt.ylabel("Exa bytes per month $(10^{18}$B)")
plt.xlabel("Year")

ax.text(0.85,0.52,'5G',
        horizontalalignment='center',
        verticalalignment='center',
        fontsize=14,
        transform=ax.transAxes)

ax.text(0.7,0.15,'2G/3G/4G',
horizontalalignment='center',
verticalalignment='center',
fontsize=14,
transform=ax.transAxes)

plt.ylim([0,250])
plt.xticks(x_years)

plt.tight_layout()
plt.grid(axis='y')
plt.savefig("ericsson_global_mobile_data.pdf", dpi=600,bbox_inches = 'tight')
plt.show()

# %%
