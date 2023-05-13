from utils import translate
import matplotlib.pyplot as plt
import RayleighTaylor as rt
from utils import save_but_not_show
import os
import numpy as np
from common import plot_roti, plot_terminators


def plot_winds_ts(
        ax, 
        ds, 
        cols, 
        sign = -1, 
        effect = "winds"
        ):
    
    if "zon" in cols:
        coord =  "Zonal"
    else:
        coord = "Meridional"

    for wd in cols:
        if effect == "winds":
            
            gamma = rt.effects_due_to_winds(
                    ds, 
                    wind = wd,
                    sign = sign)
        else:
        
            gamma = rt.effects_due_to_recombination(
                    ds, 
                    wind = wd,
                    sign = sign)
        
        if "ef" in wd:
            label = f"{coord} efetivo"
        else:
            label = f"{coord} geográfico"
        
        ax.plot(gamma * 1e4, label = label)
        
    ax.legend(loc = "lower left")
    
    ax.axhline(0, linestyle = "--")
        
    ax.set(ylim = [-20, 20], 
           xlim = [ds.index[0], 
                   ds.index[-1]]
           )
    
def plot_by_sign(
        ax, col, ds, 
        wind_sign = "positive", 
        effect = "winds"
        ):
    
    if wind_sign == "positive":
        sign = 1
    else:
        sign = -1
        
    eq = rt.EquationsFT(
        wind_sign = wind_sign
        )
    
    if effect == "winds":
        title = eq.winds
    else:
        title = eq.recombination
        
    ax[0, col].set(title = title)
    
    plot_winds_ts(ax[0, col], ds, ["zon", "zon_ef"], 
                  sign = sign, effect = effect)
    plot_winds_ts(ax[1, col], ds, ["mer", "mer_ef"], 
                  sign = sign, effect = effect)
    
    if col == 0:
        for num in range(2):
            ax[num, col].set(ylabel = eq.label)


def plot_winds_effect_and_recombination(
        infile, 
        hemisphere, 
        effect = "recombination"
        ):
    
    fig, ax = plt.subplots(
        figsize = (15, 8), 
        sharex = True,
        sharey = "row",
        ncols = 2, 
        nrows = 3, 
        dpi = 300
        )
        
    plt.subplots_adjust(
        wspace = 0.05, 
        hspace = 0.05
        )
    
    ds = rt.set_data(infile, hemisphere, alt = 300)
            
    plot_by_sign(
            ax, 0, ds, 
            wind_sign = "negative", 
            effect =  effect 
            )
    
    plot_by_sign(
            ax, 1, ds, 
            wind_sign = "positive", 
            effect =  effect 
            )
    
    plot_roti(ax[2, 0], ds)
    plot_roti(ax[2, 1], ds)
    
    ax[2, 1].set(ylabel = "")
    
    fig.suptitle(translate(hemisphere.title()))
    
    for ax in ax.flat:
        plot_terminators(ax, ds)
    
    plt.show()
    return fig
    


def save_plot(infile, filename, to_folder):
    
    effect = to_folder.split("_")[0]
    
    for hemisphere in ["south", "north"]:
        
        fig = plot_winds_effect_and_recombination(
            os.path.join(infile, filename), 
            hemisphere, effect = effect)
        
        FigureName = filename.replace(".txt", ".png")
        save_in = f"D:\\plots\\{to_folder}\\{hemisphere}_{FigureName}"
        
        save_but_not_show(fig, save_in)
        
  
def main():
    infile = "database/RayleighTaylor/process/"
    
    for to_folder in ["winds_effect",
                      "recombination_winds_effect"]:
    
        for filename in os.listdir(infile):
            print("saving...", filename)
            save_plot(infile, filename, to_folder)