from utils import translate
import matplotlib.pyplot as plt
import RayleighTaylor as rt
from common import plot_roti, plot_terminators
import pandas as pd


def sum_gravity(df, recom = False):
    res = []
    for hem in ["south", "north"]:
        ds = df.loc[df["hem"] == hem]
        
        gamma = rt.effects_due_to_gravity(
            ds, recom = recom)
        
        res.append(gamma)
    
    return pd.concat(res, axis = 1).sum(axis = 1)


def sum_drift(df, recom  = False, drift = "vz"):
    res = []
    for hem in ["south", "north"]:
        ds = df.loc[df["hem"] == hem]
        
        gamma = rt.effects_due_to_drift(
                        ds, 
                        recom = recom, 
                        col = drift
                        )
        
        res.append(gamma)
    
    return pd.concat(res, axis = 1).sum(axis = 1)


def plot_gravity(ax, ds, recom  = False):
    
    gamma = sum_gravity(ds, recom = recom)
     
    ax.plot(gamma * 1e4)
                
    ax.set(ylim = [-40, 40], 
           xlim = [ds.index[0], ds.index[-1]])
    
    ax.axhline(0, linestyle = "--")
    ax.text(0.05, 0.85, "Efeitos devido apenas a gravidade", 
            transform = ax.transAxes)


def plot_drift(
        ax, 
        ds, 
        recom = False,
        drift = "vz"
        ):
    
    gamma = sum_drift(ds, drift = drift, recom = recom)
     
    ax.plot(gamma * 1e4, label = f"$V_P = {drift}$")
                
    ax.set(ylim = [-40, 40], 
           xlim = [ds.index[0], ds.index[-1]])
    
    ax.axhline(0, linestyle = "--")
    ax.text(0.05, 0.85, "Efeitos devido a deriva vertical", 
            transform = ax.transAxes)
    ax.legend(loc = "lower left")




def plot_total_gravity_drift_effect(ds):
    fig, ax = plt.subplots(
        figsize = (14, 10),
        nrows = 3,
        ncols = 2,
        dpi = 300,
        sharex = True,
        sharey = "row"
        )
    
    plt.subplots_adjust(
        wspace = 0.08, 
        hspace = 0.22
       )

    eq = rt.EquationsFT()
    
    for col, rc in enumerate([False, True]):
        
        ax[0, col].set(title = eq.gravity(recom = rc))
        plot_gravity(ax[0, col], ds, recom = rc)
        
        ax[1, col].set(title = eq.drift(recom = rc))
        
        ax[col, 0].set(ylabel = eq.label)
        for drift in ["vz", "vzp"]:
            plot_drift(ax[1, col], ds, recom = rc, drift = drift)
            
            
    plot_roti(ax[2, 0], ds)
    plot_roti(ax[2, 1], ds)
    
    ax[2, 1].set(ylabel = '')
    
    for ax in ax.flat:
        plot_terminators(ax, ds)
        
    fig.suptitle("Efeitos devidos a gravidade e a deriva vertical")
        
    return fig


def main():
    infile = "database/RayleighTaylor/reduced/300.txt"
    
    df = rt.load_process(infile, apex = 300)
    
    ds = rt.split_by_freq(df)[0]
    fig = plot_total_gravity_drift_effect(ds)
    
    plt.show()
    
# main()