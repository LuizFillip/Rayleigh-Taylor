import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib.ticker as ticker
import numpy as np
from plotConfig import *
infile = "database/growthRates/gammas250_350km.txt"


def text_painels(axs, x = 0.8, y = 0.8, 
                 fontsize = 30):
    """Plot text for enumerate painels by letter"""
    chars = list(map(chr, range(97, 123)))
    
    for num, ax in enumerate(axs):
        char = chars[num]
        ax.text(x, y, f"({char})", 
                transform = ax.transAxes, 
                fontsize = fontsize)

def plotAnnualVariation(infile, year = 2014):
    df = pd.read_csv(infile, index_col = 0)
    
    df.index = pd.to_datetime(df.index)
    
    df = df.loc[df.index.year == year]
    
    fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(nrows = 5,
                                                  figsize = (15, 20), 
                                                  sharex = True)
    
    plt.subplots_adjust(hspace = 0.1)
    
    axs = list((ax1, ax2, ax3, ax4, ax5))
    
    col = df.columns
    names = [r"$(V_{zp} - U + \frac{g}{\nu_{in}})\frac{1}{n_e} \frac{\partial n_e}{\partial y} - R$",
             r"$(V_{zp} + \frac{g}{\nu_{in}})\frac{1}{n_e} \frac{\partial n_e}{\partial y} - R$", 
             r"$(V_{zp} - U + \frac{g}{\nu_{in}})\frac{1}{n_e} \frac{\partial n_e}{\partial y}$", 
             r"$(V_{zp} + \frac{g}{\nu_{in}})\frac{1}{n_e} \frac{\partial n_e}{\partial y}$", 
             r"$(\frac{g}{\nu_{in}})\frac{1}{n_e} \frac{\partial n_e}{\partial y}$"]
    
    from math import floor, log10, inf
    
    def num_zeros(decimal):
        return inf if decimal == 0 else -floor(log10(abs(decimal))) - 1
    
    for num, ax in enumerate(axs):
        
        if num == 4:
            
            df[col[num]] = df[col[num]] * 10
            
            name = "$\gamma_{RT} ~(10^{-4}~s^{-1})$"
            
        else:
            name = "$\gamma_{RT} ~(10^{-3}~s^{-1})$"
            
    
        ax.plot(df[col[num]], 
                lw = 3, 
                color = "k")
        
        
        ax.text(0.95, 0.8, names[num],  
                horizontalalignment ='right',
                transform = ax.transAxes) 
        
       
        ax.set(ylim = [-0.3e-3, 3e-3], 
               yticks = np.arange(-0.3e-3, 3e-3, 0.9e-3),
               ylabel = name)
        
        
        ax.yaxis.set_major_formatter(
                        ticker.FuncFormatter(lambda y, _: '{:g}'.format(y/1e-3)))
    
    ax5.set(xlabel = "Meses")
    ax4.xaxis.set_major_formatter(dates.DateFormatter('%b'))
    ax4.xaxis.set_major_locator(dates.MonthLocator(interval = 1))
    

    
    text_painels(axs, x = 0.01, y = 0.8, fontsize = 35)
    
    
    return fig


fig  = plotAnnualVariation(infile, year = 2014)
    
#fig.savefig(path_tex("results") + "\\annual_growth_rates.png")