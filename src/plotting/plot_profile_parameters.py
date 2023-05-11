import matplotlib.pyplot as plt
from labels import Labels
import numpy as np
import settings as s
from RayleighTaylor import build
    
def plot_recombination_freq(ax, r, alts):
    
    
    
    
    ax.plot(r, alts, color = "k", lw = 2) 
    ax.set(
        title = name,
        xlabel = (f"{symbol} ({units})"),
        xscale = "log", 
        xlim = [1e-10, 1e3]
            )

def plot_winds(ax, u, alts):
    name = "Ventos termosféricos"
    units = "m/s"
    symbol = "U"
    
    ax.plot(u, alts, color = "k", lw = 2)
    ax.axvline(0, linestyle = "--", color = "r", lw = 2)
    
    ax.set(
        title = name,
        xlabel = (f"{symbol} ({units})"), 
        xlim = [-120, 120], 
        xticks = np.arange(-120, 140, 40)
        )
    ax.legend(loc = "upper right")
    

    
def plot_growth_rate_RT(
        ax, 
        nu, l, r, vz, u, alts
        ):
    
    name = "Taxa de crescimento Rayleigh-Taylor"
    symbol = "$\gamma_{RT}$"
    units = "$10^{-3} s^{-1}$"
    
    ax.plot(growth_rate_RT(nu, l, r, vz, u), alts, 
               color = "k", lw = 2)
    
    ax.plot(growth_rate_RT(nu, l, 0, vz, u), alts, 
               label = r"$R = 0 $", lw = 2)
    
    ax.plot(growth_rate_RT(nu, l, r, vz, 0), alts, 
               label = r"$U = 0 $", lw = 2)
    
    ax.legend()
    ax.set(
        title = name,
        xlim = [-6e-3, 6e-3], 
        xlabel = (f"{symbol} ({units})")
        )
    
def plot_profiles_parameters(date):
    infile = "database/FluxTube/201301012100.txt"

    


    fig, ax = plt.subplots(
        figsize = (12, 6), 
        sharey = True,
        ncols = 5,
        dpi = 300)

    plt.subplots_adjust(wspace = 0.05)

    def adding_labels(ax):

        cols = ['ratio', 'K', 'nui', "U", "U"]
        other =  ["", "", "", "\ngeográfico", "\nefetivo"]
        l = Labels().infos
        for i, col in enumerate(cols):
            info = l[col]
         
            ax[i].set(title = info["name"] + other[i],
                xlabel = f"{info['symbol']} ({info['units']})")
        
       
        
    for hem in ["north", "south"]:

        cols = ['ratio', 'K', 'nui', 'zon', 'zon_ef']
        
        ds = build(infile, hemisphere = hem, 
                   remove_smooth = 15)
            
        for i, col in enumerate(cols):
            
            ax[i].plot(ds[col], ds.index, 
                       label = translate(hem).title())
            
            ax[i].legend(loc = "upper left")
            
            if "zon" in col:
                ax[i].set(xlim = [-50, 50])
           
                

    adding_labels(ax)
    ax[0].set(ylabel  = "Altura de apex (km)", 
              yticks = np.arange(210, 600, 50), 
              ylim = [210, 600])

    plt.show()