from utils import translate
import matplotlib.pyplot as plt
import RayleighTaylor as rt
from utils import save_but_not_show, fname_to_save
import os
from common import plot_roti, plot_terminators
import pandas as pd


def plot_gravity_effect(df):
    
    fig, ax = plt.subplots(
        figsize = (15, 6), 
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
    
    
    for i, hem in enumerate(["north", "south"]):
        
        ds = df.loc[df["hem"] == hem]

        plot_roti(ax[1, i], ds)
        
        
        for col, recom in enumerate([False, True]):
        
            gamma = rt.effects_due_to_gravity(ds, recom = recom)
            
            ax[0, col].plot(gamma * 1e4, 
                            label = translate(hem).title()
                            )
            
            ax[0, col].legend(loc = "lower left")
            ax[0, col].axhline(0, linestyle = "--")
            

            eq =  rt.EquationsFT()
        
            ax[0, col].set(ylim = [-20, 20], 
                         ylabel = eq.label, 
                         title = eq.gravity(recom = recom))
           
        
    ax[1, 1].set(ylabel = '')
    ax[0, 1].set(ylabel = '')
    
    for ax in ax.flat:
        plot_terminators(ax, ds)
        
    return fig
    

def save():
    path = "database/RayleighTaylor/process2/"
    save_in =  "D:\\plots\\gravity_effect\\"
    
    for filename in os.listdir(path):
    
        
        print("saving...", filename)
            
        df = rt.load_process(os.path.join(path, filename))
    
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
# save()

path = "database/RayleighTaylor/process2/1.txt"

df = rt.load_process(path)
ds = rt.separeting_times(df)[0]


fig = plot_gravity_effect(ds)
plt.show(
    )

