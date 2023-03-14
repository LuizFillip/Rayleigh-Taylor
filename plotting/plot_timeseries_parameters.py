import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import setup as s
from Results.utils import get_dusk
from Digisonde.drift import load_DRIFT
from FabryPerot.core import load_FPI
from RayleighTaylor.core import timerange_msise
from RayleighTaylor.base.neutral import eff_wind

def load_ROTI():
    infile = "salu_2013.txt"
    df = pd.read_csv(infile, index_col = 0)
    df.index = pd.to_datetime(df.index)
    return df


def filter_times(start, df):
    
    end = start + dt.timedelta(hours = 11)
    return df.loc[(df.index >= start) & 
                 (df.index <= end), :]


start = dt.datetime(2013, 1, 1, 20)

ROTI = filter_times(start, 
                    load_ROTI())


DRF = filter_times(
    start, 
    load_DRIFT(smoothed = True)
    )
FPI = filter_times(
    start, 
    load_FPI(resample = None)
    )

FPI["U"] = eff_wind(FPI.zon, 
         FPI.mer, 
         year = 2013, 
         site = "saa").Nogueira
print(FPI)
#%%


ts = timerange_msise(start)

#%%

fig, ax = plt.subplots(nrows = 4, 
                       figsize = (12, 12), 
                       sharex = True)

plt.subplots_adjust(hspace = 0.1)
ax[0].plot(DRF["vz"])

ax[0].set(ylim = [-40, 40], 
          ylabel = r"$V_z ~ (ms^{-1})$")

ax[1].plot(FPI, label = ["zon", "mer", "U"])
ax[1].legend()
ax[1].set(ylabel = r"Velocidade $~(ms^{-1})$", 
          ylim = [-50, 200])
ax[2].plot(9.81 / ts["nu"])

ax[2].set(ylabel = r"$g/\nu_{in} ~(s^{-1})$")

ax1 = ax[2].twinx()

ax1.plot(ts["R"]*10e3, color = "k")
ax1.set(ylabel = r"$R~(10^{-3} s^{-1})$")

ax[3].plot(ROTI)

s.format_axes_date(
    ax[3], 
    time_scale = "hour", 
    interval = 2
    )

ax[3].set(ylabel = "ROTI (TECU/min)", 
          xlabel = "Hora universal", 
          ylim = [0, 6])