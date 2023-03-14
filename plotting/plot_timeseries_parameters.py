import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import setup as s
from Results.utils import get_dusk
from Digisonde.drift import load_DRIFT
from FabryPerot.core import load_FPI

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

fig, ax = plt.subplots(nrows = 3, 
                       figsize = (10, 6), 
                       sharex = True)


ax[0].plot(DRF["vz"])

ax[0].set(ylim = [-40, 40])

ax[1].plot(FPI)

ax[2].plot(ROTI)


s.format_axes_date(
    ax[2], 
    time_scale = "hour", 
    interval = 2
    )

ax[2].set(ylabel = "ROTI (TECU/min)", 
          xlabel = "Hora universal", 
          ylim = [0, 6])