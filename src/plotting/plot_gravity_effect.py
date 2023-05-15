from utils import translate
import matplotlib.pyplot as plt
import RayleighTaylor as rt
from utils import save_but_not_show, fname_to_save
import os
from common import plot_roti, plot_terminators
import pandas as pd


def plot_gravity_effect(ds):
    
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
            
            gamma = rt.effects_due_to_gravity(ds, recom = recom)
            
            ax[0, col].plot(gamma * 1e4, 
                            label = translate(hem).title())
            ax[0, col].legend(loc = "lower left")
            ax[0, col].axhline(0, linestyle = "--")
            
        plot_roti(ax[1, col], ds)
        
    
        eq =  rt.EquationsFT()
    
        ax[0, col].set(ylim = [-20, 20], 
                     ylabel = eq.label, 
                     title = eq.gravity(recom = recom))
       
        
    ax[1, 1].set(ylabel = '')
    ax[0, 1].set(ylabel = '')
    
    for ax in ax.flat:
        plot_terminators(ax, ds)
        
    return fig
    


path = "database/RayleighTaylor/process2/"
save_in =  "D:\\plots\\gravity_effect\\"

for filename in os.listdir(path):

    infile = os.path.join(path, filename) 
    
    print("saving...", filename)
    
    def load_process(infile):
        df = pd.read_csv(infile, index_col = 0).sort_index()
    
        df.index = pd.to_datetime(df.index)
        
        return df
    
    df = load_process(infile)

    times = pd.date_range(
        df.index[0], df.index[-1], freq = "5D"
        )

    for i in range(len(times) - 1):
        
        ds = df[(df.index >= times[i]) & 
                (df.index <= times[i + 1])]
                
        fig = plot_gravity_effect(ds)
        
        save_but_not_show(
                fig, 
                os.path.join(save_in, fname_to_save(ds))
                )
