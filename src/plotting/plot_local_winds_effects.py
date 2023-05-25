# -*- coding: utf-8 -*-
"""
Created on Thu May 25 09:36:52 2023

@author: Luiz
"""

import matplotlib.pyplot as plt
from common import plot_roti, plot_terminators
import RayleighTaylor as rt
from utils import save_img
import pandas as pd
import datetime as dt


fig, ax = plt.subplots(
            figsize = (8, 10),
            sharex = True,
            nrows = 3,
            dpi = 300
            )

plt.subplots_adjust(hspace = 0.3)


df = pd.read_csv("gamma_parameters.txt", index_col = 0)
df.index = pd.to_datetime(df.index)


dn = dt.datetime(2013, 3, 17, 20)
alt = 250

delta = dt.timedelta(seconds = 43200)

df = df.loc[(df["alt"] == alt) & 
            (df.index >= dn) &
            (df.index <= dn + delta)]

    
gamma = (df["vz"] + df["U"] + (9.81 / df["nui"])) * df["L"] 
ax[0].plot(gamma *1e4, label = "zonal")
gamma = (df["vz"] + df["V"] + (9.81 / df["nui"])) * df["L"] 

ax[1].plot(gamma *1e4, label = "meridional")

ax[1].set(ylim = [-10, 20])
plot_roti(ax[2], df, hour_locator = 1, station = "ceft")