from utils import translate
import matplotlib.pyplot as plt
import RayleighTaylor as rt
import os
from common import plot_roti, plot_terminators

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
            label = f"{coord} efetivo ({hem})"
        else:
            label = f"{coord} geográfico ({hem})"
        
        ax.plot(gamma * 1e4, label = label)
        
    ax.legend(ncol= 2, loc = "upper left")
    
    ax.axhline(0, linestyle = "--")
        
    ax.set(ylim = [-20, 20], 
           xlim = [ds.index[0], 
                   ds.index[-1]]
           )
    




def plot_winds_effect(infile, filename, recom):
    fig, ax = plt.subplots(
        figsize = (17, 10), 
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
    
    infile = os.path.join(infile, filename)
            
    eq = rt.EquationsFT()
    
    for hem in ["north", "south"]:
        
        ds = rt.set_data(infile, hem, alt = 300)
        
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

def main():
    infile = "database/RayleighTaylor/process/"
    filename = "04.txt"
    recom = True
    
    fig = plot_winds_effect(infile, filename, recom)
    
    plt.show()