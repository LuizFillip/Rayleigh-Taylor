import pandas as pd
from common import load, plot_times_axes
import numpy as np
import matplotlib.pyplot as plt
import settings as s
from labels import Labels

def plot_winds(ax, df):
    ax.plot(df[['zon_ef', "zon"]])
    
    ax.set(ylim = [-150, 150], 
           ylabel = "Velocidade\n zonal (m/s)")
    
    ax.legend(["Geográfico", "Efetivo"], 
                 loc = "upper right",
                 ncol = 2)




def plot_contour(ax, ds, val):
    
    vls = ds.values

    vmin, vmax = np.min(vls), np.max(vls)
    
    img = ax.contourf(
        ds.columns, 
        ds.index, 
        ds.values, 30, 
        cmap = "rainbow"
        )
    
    ticks = np.linspace(vmin, vmax, 5)
    
    lbs  = Labels().infos[val]
    
    s.colorbar_setting(
            img, ax, ticks, 
            label = f"{lbs['symbol']} ({lbs['units']})", 
            bbox_to_anchor = (.54, 0., 1, 1), 
            ) 
    
    name = lbs["name"].replace("\n", " ")
    
    ax.set(title = f"{name}")
    
def plot_iono_parameters(infile):
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (12, 8),
        ncols = 2,
        nrows = 2,
        sharex = True,
        sharey = True
        )
    
    plt.subplots_adjust(
        hspace = 0.1, 
        wspace = 0.3
        )
    
   
    
    cols = ["N", "K", "nui", "ratio"]
    
    for i in range(2):
        ax[i, 0].set(ylabel = "Altura de Apex (km)")
    
    for index, ax in enumerate(ax.flat):
        
        ds = load(infile, parameter = cols[index])
        
        plot_contour(ax, ds, cols[index])
        
        if index == 2 or index == 3:
            plot_times_axes(ax)
            plot_times_axes(ax)
        

infile = "database/RayleighTaylor/process2/4.txt"