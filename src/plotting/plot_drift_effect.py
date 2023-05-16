from utils import translate, fname_to_save
import matplotlib.pyplot as plt
import RayleighTaylor as rt
from utils import save_but_not_show
import os
from common import plot_roti, plot_terminators



def plot_drift_ts(
        ax, 
        ds, 
        recom = False,
        effect = "vz"
        ):
    
    gamma = rt.effects_due_to_drift(
                    ds, 
                    recom = recom, 
                    col = effect
                    )
    
    eq = rt.EquationsFT()
    
    label = eq.drift(recom = recom)
    
    ax.plot(gamma * 1e4, 
            label = label)
                
    ax.set(ylim = [-20, 20], 
           xlim = [ds.index[0], 
                   ds.index[-1]]
           )
    
    ax.axhline(0, linestyle = "--")

def plot_drift_effect(df):
    
    fig, ax = plt.subplots(
        figsize = (12, 8), 
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
    
    for col, hem in enumerate(["north", "south"]):
        
        ds = df.loc[df["hem"] == hem]
        
        ax[0, col].set(title = translate(hem.title()))
        
        ax[col, 0].set_ylabel(rt.EquationsFT().label)
        
        plot_roti(ax[2, col], ds)
        
        names = ["Variação da deriva", 
                 "Pico pré reversão"]
        
        for row, effect in enumerate(["vz", "vzp"]):
            
            ax[row, col].text(
                0.05, 0.8, 
                f"{names[row]} ({effect})", 
                transform = ax[row, col].transAxes
                )
            
            plot_drift_ts(ax[row, col], ds, 
                      effect = effect)
        
            plot_drift_ts(ax[row, col], ds, 
                      effect = effect, recom = True)
        
    
    ax[0, 0].legend(loc = "upper left", 
                    ncols = 2, 
                    bbox_to_anchor = (0.25, 1.4))
    
    
    ax[2, 1].set(ylabel = "")
    
    for ax in ax.flat:
        plot_terminators(ax, ds)
    
    return fig


def save():
    
    save_in = "D:\\plots\\drift_effect\\"
    
    infile = "database/RayleighTaylor/reduced/300km.txt"
    df = rt.load_process(infile, apex = 300)
    
    for ds in rt.separeting_times(df):
        fig = plot_drift_effect(ds)
    
        save_it = os.path.join(save_in, fname_to_save(ds))
        save_but_not_show(fig, save_it)
            
            
# save()

infile = "database/RayleighTaylor/reduced/300km.txt"
df = rt.load_process(infile, apex = 300)

ds = rt.separeting_times(df)[0]
fig = plot_drift_effect(ds)


plt.show()