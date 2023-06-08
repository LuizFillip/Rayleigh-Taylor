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
    
    gammas = [df["L"] * ( 9.81 / df["nui"]) - df["R"], 
              df["L"] * (-df[wind]) - df["R"], 
              df["L"] * (vzp ) - df["R"]] #- df[wind] + (9.81 / df["nui"])
    
    lbs = rt.EquationsRT()

    names = [lbs.gravity( rc = True),
             lbs.winds(sign = -1, rc = True), 
             lbs.complete(sign = -1, rc = True)]
    
    for i, gamma in enumerate(gammas):
        ax.plot(gamma *1e4, label = names[i])
        
    ax.axhline(0, linestyle = "--")
    ax.set(title = f'Vzp = {vzp} m/s')
    
def plot_compare_dates(alt = 300, wind = 'mer_ef'):
    
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
        wspace = 0.1)
    
    dates = pd.date_range(
        "2013-3-16 20:00", 
        freq = "1D", 
        periods = 3)
    
    for i, dn in enumerate(dates):
        
        infile = "gamma_perp_mer.txt"
    
        df = load_by_alt_time(infile, alt, dn)
    
        plot_roti(ax[1, i], df,  hour_locator = 1)
        
        plot_gamma(
            ax[0, i], df, wind =  wind
            )
            
        if i >= 1:
            ax[1, i].set(ylabel = '')
    
    lbs = rt.EquationsRT()
    ax[0, 0].set(ylabel = lbs.label, ylim = [-50, 50])
    
    ax[0, 1].legend(
        bbox_to_anchor = (0.5, 1.4), 
        ncol = 3, 
        loc = 'upper center'
        )
    if wind == 'mer_ef':
        fig.suptitle('Efeitos com vento paralelo a B', y = 1.1)
    else:
        fig.suptitle('Efeitos com vento perpendicular a B', y = 1.1)
    
    return fig

fig = plot_compare_dates(alt = 300)


# fig.savefig('RayleighTaylor/figures/parallel_winds_effects.png', dpi = 300)

