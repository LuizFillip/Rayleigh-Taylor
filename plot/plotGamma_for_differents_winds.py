from core import get_max
import matplotlib.pyplot as plt
import numpy as np 
import setup as s
import matplotlib.ticker as ticker
import pandas as pd

def load(infile):

    df = pd.read_csv(infile, index_col = 0)
    
    df.index = pd.to_datetime(df.index)
    
    df["date"] = df.index.date
    
    return df

def plot_gammas(ax, df, times, n):
    gs = get_max(df, times)
    ax.plot(times, gs, color = "k")


    ax.yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda y, _: '{:g}'.format(y/1e-3)))

    ax.set(ylabel = "$\gamma_{RT} \\times 10^{-3} ~ s^{-1}$")
    
    if n == 0:
        ax.set(title = r"$(V_{zp} - U_{eff} + \frac{g}{\nu_{in}})" +
           "\frac{1}{n_e} \frac{\partial n_e}{\partial y} - R$")

fig, ax = plt.subplots(nrows = 3, 
                       figsize = (8, 6),
                       sharey = True,
                       sharex = True)    

plt.subplots_adjust(hspace = 0.05)

s.config_labels()

for n, ax in enumerate(ax.flat):
    
    infile = f"database/data/2014_U{n + 1}.txt"

    df = load(infile)
    
    times = pd.to_datetime(np.unique(df.index))
    ax.axhline(0, color = "r", linestyle = "--")
    
    plot_winds(ax, df, n)
    
    s.format_axes_date(ax)
    