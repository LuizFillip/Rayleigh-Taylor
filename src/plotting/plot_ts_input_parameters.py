import os
from common import load, plot_times_axes
import numpy as np
import matplotlib.pyplot as plt
import settings as s
from labels import Labels
from utils import fname_to_save, save_but_not_show




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
    
def plot_input_parameters(infile, cols):
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (15, 8),
        ncols = 2,
        nrows = 2,
        sharex = True,
        sharey = True
        )
    
    plt.subplots_adjust(
        hspace = 0.3, 
        wspace = 0.3
        )
    
    
    for i in range(2):
        ax[i, 0].set(ylabel = "Altura de Apex (km)")
    
    for index, ax in enumerate(ax.flat):
        
        fname, ds = load(infile, parameter = cols[index])
        
        plot_contour(ax, ds, cols[index])
        
        if index == 2 or index == 3:
            plot_times_axes(ax)
            plot_times_axes(ax)
            
    return fig, fname

def save():

    cols = ["zon", "zon_ef", "mer", "mer_ef"]
    #cols = ["N", "K", "nui", "ratio"]
    
    
    path = "database/RayleighTaylor/process3/"
    save_in = "D:\\plots\\parameters\\winds\\"
    
    for filename in os.listdir(path):
    
        infile = os.path.join(path, filename) 
        
        
        print("saving...", filename)
        try:
            
            fig, fname = plot_input_parameters(infile, cols)
        
            save_but_not_show(
                    fig, 
                    os.path.join(save_in, fname)
                    )
        except:
            continue