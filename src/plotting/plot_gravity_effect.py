from utils import translate
import matplotlib.pyplot as plt
import RayleighTaylor as rt
from utils import save_but_not_show
import os
from common import plot_roti, plot_terminators




infile = "database/RayleighTaylor/process2/4.txt"

def plot_gravity_effect(infile):
    
    fig, ax = plt.subplots(
        figsize = (12, 6), 
        sharex = True,
        sharey = "row",
        ncols = 2, 
        nrows = 2, 
        dpi = 300
        )
    
    plt.subplots_adjust(
        hspace = 0.1, 
        wspace = 0.1
        )
    
    for col, recom in enumerate([False, True]):
        
        for hem in ["north", "south"]:
            
            ds = rt.set_data(infile, hem, alt = 300)
            gamma = rt.effects_due_to_gravity(ds, recom = recom)
            
            ax[0, col].plot(gamma * 1e4, label = translate(hem))
            ax[0, col].legend(loc = "upper left")
            ax[0, col].axhline(0, linestyle = "--")
            
        plot_roti(ax[1, col], ds)
        
    
        eq =  rt.EquationsFT()
    
        ax[0, col].set(ylim = [-10, 10], 
                     ylabel = eq.label, 
                     title = eq.gravity(recom = recom))
       
        
    ax[1, 1].set(ylabel = '')
    ax[0, 1].set(ylabel = '')
    
    for ax in ax.flat:
        plot_terminators(ax, ds)
        
    return fig
    
fig = plot_gravity_effect(infile)