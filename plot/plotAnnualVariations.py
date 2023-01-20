import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib.ticker as ticker
import numpy as np


infile = "database/growthRates/growth_rate_wind_modify.txt"


df = pd.read_csv(infile, index_col = 0)

df.index = pd.to_datetime(df.index)

fig, ax = plt.subplots(nrows = 5, figsize = (12, 10), sharex = True)

names = [r"$(V_{zp} - U + \frac{g}{\nu_{in}})\frac{1}{n_e} \frac{\partial n_e}{\partial y} - R$",
          r"$(V_{zp} + \frac{g}{\nu_{in}})\frac{1}{n_e} \frac{\partial n_e}{\partial y}$", 
          r"$(- U + \frac{g}{\nu_{in}})\frac{1}{n_e} \frac{\partial n_e}{\partial y}$ - R", 
          r"$(V_{zp} - U + \frac{g}{\nu_{in}})\frac{1}{n_e} \frac{\partial n_e}{\partial y}$", 
          r"$(V_{zp} + \frac{g}{\nu_{in}})\frac{1}{n_e} \frac{\partial n_e}{\partial y} - R$", ]


for num, col in enumerate(df.columns):
    
    ax[num].plot(df[col], label = f"{names[num]}", color = "k", 
                 lw = 2)
    
    ax[num].set(ylim = [-0.4e-3, 2e-3], 
                ylabel = "$\gamma_{RT} ~(10^{-3}~s^{-1})$")

    ax[num].legend(loc = "center")

    if num == 4:
        ax[num].set(xlabel = "meses")


        ax[num].xaxis.set_major_formatter(dates.DateFormatter('%b'))
        ax[num].xaxis.set_major_locator(dates.MonthLocator(interval = 1))