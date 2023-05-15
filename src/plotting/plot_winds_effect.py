from utils import translate
import matplotlib.pyplot as plt
import RayleighTaylor as rt
import os
from common import plot_roti, plot_terminators
from utils import save_but_not_show, fname_to_save

def plot_winds_ts(
        ax, 
        ds, 
        cols, 
        sign = -1, 
        recom = False,
        hem = "north"):
    
    hem = translate(hem)
    
    if "zon" in cols:
        coord =  "Zonal"
    else:
        coord = "Meridional"

    for wd in cols:
            
        gamma = rt.effects_due_to_winds(
                ds, 
                wind = wd,
                sign_wd = sign, 
                recom = recom)
      
        if "ef" in wd:
            label = f"Efetivo ({hem})"
        else:
            label = f"Geográfico ({hem})"
        
        ax.plot(gamma * 1e4, label = label)
        
    ax.legend(ncol= 2, loc = "lower left")
    ax.text(0.05, 0.85, coord, transform = ax.transAxes)
    ax.axhline(0, linestyle = "--")
        
    ax.set(ylim = [-20, 20], 
           xlim = [ds.index[0], 
                   ds.index[-1]]
           )
    return ax

def plot_winds_effect(df, recom = False, alt = 300):
    
    fig, ax = plt.subplots(
        figsize = (20, 12), 
        sharex = True,
        sharey = "row",
        ncols = 2, 
        nrows = 3, 
        dpi = 300
        )
        
    plt.subplots_adjust(
        wspace = 0.08, 
        hspace = 0.05
        )
    
    eq = rt.EquationsFT()
        
    for hem in ["north", "south"]:
        
        ds = df.loc[df["hem"] == hem]
        
        for row, wd in enumerate(["zon", "mer"]):
        
            cols = [wd, f"{wd}_ef"]
            
            ax[row, 0].set_ylabel(eq.label)
            
            for col, sign in enumerate([1, -1]):
         
                plot_winds_ts(ax[row, col], ds, cols, 
                              sign = sign, 
                              recom = recom, 
                              hem = hem)
                
                title = eq.winds(
                    wind_sign = sign, 
                    recom = recom
                    )
                
                ax[0, col].set(title = title)
        
    
    plot_roti(ax[2, 0], ds)
    plot_roti(ax[2, 1], ds)
    
    ax[2, 1].set(ylabel = "")
    
    for ax in ax.flat:
        plot_terminators(ax, ds)
        
    return fig

import pandas as pd


def save(recom = True):
    
    if recom:
        save_in = "D:\\plots\\recombination_winds_effect\\"
        
    else:
        save_in = "D:\\plots\\winds_effect\\"
    
    path = "database/RayleighTaylor/process2/"
    
    for filename in os.listdir(path):
    
        infile = os.path.join(path, filename) 
        
        print("saving...", filename)
        

        df = pd.read_csv(infile, index_col = 0).sort_index()

        df.index = pd.to_datetime(df.index)

        times = pd.date_range(
            df.index[0], df.index[-1], freq = "5D"
            )

        last = len(times) - 1

        for i in range(last):
            
            ds = df[(df.index >= times[i]) & 
                    (df.index <= times[i + 1])]
                    
            fig = plot_winds_effect(ds, recom = recom)
        
            save_but_not_show(
                    fig, 
                    os.path.join(save_in, fname_to_save(ds))
                    )
            
for rc in [True, False]:      
    save(recom = rc)
