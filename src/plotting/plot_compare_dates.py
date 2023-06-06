import matplotlib.pyplot as plt
from common import plot_roti, load_by_alt_time
import RayleighTaylor as rt
import pandas as pd
import digisonde as dg
import numpy as np

def label_wind(wind = "mer_ef"):
    if wind == "mer_ef":
        return 'Paralelo a $\\vec{B}$'
    else:
        return 'Perpendicular a $\\vec{B}$'

def plot_gamma(ax, df, wind = "mer_ef"):
    
    dn = df.index[0]
    vz = dg.add_vzp()
    vzp = vz[vz.index == dn.date()]["vzp"].item()
    
    gamma = df["L"] * (
        + (9.81 / df["nui"])# vzp - df[wind]
        ) - df["R"]
    
    
    ax.plot(gamma *1e4, label = label_wind(wind))
    ax.axhline(0, linestyle = "--")
    #ax.set(title = f'Vzp = {vzp} m/s')
    
def plot_compare_dates(alt = 300):
    
    fig, ax = plt.subplots(
        figsize = (16, 6),
        sharey = "row",
        sharex= 'col',
        ncols = 3,
        nrows = 2,
        dpi = 300
        )
    
    plt.subplots_adjust(
        hspace = 0.1, 
        wspace = 0.05)
    
    dates = pd.date_range(
        "2013-3-16 20:00", 
        freq = "1D", 
        periods = 3)
    
    for i, dn in enumerate(dates):
        
        infile = "gamma_perp_mer.txt"
    
        df = load_by_alt_time(infile, alt, dn)
    
        plot_roti(ax[1, i], df,  hour_locator = 1)
        
        for wind in ["mer_ef", "mer_perp"]:
            plot_gamma(
                ax[0, i], df, wind = wind
                )
            
        if i >= 1:
            ax[1, i].set(ylabel = '')
    
    lbs = rt.EquationsRT()
    
    ax[0, 0].set(ylabel = lbs.label, ylim = [-60, 60])
    
    ax[0, 1].legend(
        bbox_to_anchor = (0.5, 1.4), 
        ncol = 2, 
        loc = 'upper center'
        )
    title = lbs.gravity( rc = True)
    fig.suptitle(title + ' (300 km)', y = 1.1)
    
    return fig

# fig = plot_compare_dates(alt = 300)


# fig.savefig('RayleighTaylor/figures/local_all_dates.png', dpi = 300)

