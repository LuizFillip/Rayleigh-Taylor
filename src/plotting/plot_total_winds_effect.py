import pandas as pd
import RayleighTaylor as rt
import matplotlib.pyplot as plt
from common import plot_roti, plot_terminators



def sum_gammas(df, sign = 1, wind = "zon", recom = False):
    res = []
    for hem in ["south", "north"]:
        ds = df.loc[df["hem"] == hem]
        
        gamma = rt.effects_due_to_winds(
                ds, 
                wind = wind,
                sign_wd = sign, 
                recom = recom
                )
        
        res.append(gamma)
    
    return pd.concat(res, axis = 1).sum(axis = 1)



def plot_gamma(ax, df, coord = "zonal", rc = False, sign = 1):
    
    winds = [coord[:3], coord[:3] + "_ef"]
    
    labels = ["Geográfico", "Efetivo"]
    
    for i in range(2):
  
        gamma = sum_gammas(
            df, sign = sign, wind = winds[i], recom = rc
            )
        
        ax.plot(gamma * 1e4, 
                label = labels[i])
        
    ax.text(0.05, 0.85, coord.title(), transform = ax.transAxes)
    
    ax.axhline(0, linestyle = "--")
    ax.set(ylim  = [-40, 40], 
           xlim = [df.index[0], df.index[-1]])
    return ax



def plot_total_winds_effect(df, rc = False):
    
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
        hspace = 0.05
       )
    
    eq = rt.EquationsFT()
    
    for row, coord in enumerate(["zonal", 
                                 "meridional"]):
        
        ax[row, 0].set_ylabel(eq.label)
        
    
        for col, sign in enumerate([1, -1]):
            
            ax[0, col].set(
                title = eq.winds(wind_sign = sign, recom = rc)
                )
            plot_gamma(
                ax[row, col], df, 
                coord = coord, rc = rc, sign = sign
                )
         
    plot_roti(ax[2, 0], df)
    plot_roti(ax[2, 1], df)
    ax[0, 0].legend(
        ncol = 4, 
        bbox_to_anchor = (1., 1.35),
        loc = "upper center"
        )
    
    ax[2, 1].set(ylabel = "")
    
    for ax in ax.flat:
        plot_terminators(ax, df)
        
    if rc:
        w = "com"
    else:
        w = "sem"
    
    fig.suptitle(f"Taxas de crescimento totais devido aos ventos neutros {w} recombinação")
    plt.show()
    
    return fig
    
    

