import matplotlib.pyplot as plt
from common import plot_roti, plot_terminators, load_by_alt_time
import RayleighTaylor as rt
import pandas as pd
import datetime as dt
import numpy as np
import digisonde as dg





def set_data(dn, hem = 'south', alt = 300):
    infile = 'wind_perp.txt'
    
    df = pd.read_csv(infile, index_col=0)
    
    df = df.loc[(df.index ==  alt) & 
                (df['hem'] == hem)]
    
    df = df.set_index('dn')


    df.index = pd.to_datetime(df.index)
    
    delta = dt.timedelta(seconds = 43200)

    return df.loc[(df.index >= dn) & (df.index <= dn + delta)]

def set_data_2( dn, hem):
    infile = 'database/RayleighTaylor/reduced/300.txt'
    
    ds = pd.read_csv(infile, index_col = 0)
    
    ds.index = pd.to_datetime(ds.index)
    
    delta = dt.timedelta(seconds = 43200)

    ds = ds.loc[(ds.index >= dn) & (ds.index <= dn + delta) & 
                (ds['hem'] == hem)]
    
    return ds


def comp_gamma(dn, hem = 'south'):
    df  = set_data_2(dn, hem = hem)
    
    vz = dg.add_vzp()
    
    vzp = vz[vz.index == dn.date()]["vzp"].item()
    
    base = df["ratio"] * df["K"] 
    
    return [base * (df["ge"] / df["nui"]), 
            base * (- df['mer_ef']),
            base * (vzp)]
    
    


def plot_gammas(ax, dn):
    s_dfs =  comp_gamma(dn, hem = 'south')
    
    n_dfs =  comp_gamma(dn, hem = 'north')
    
    eq = rt.EquationsFT()
    
    vz = dg.add_vzp()
    
    vzp = vz[vz.index == dn.date()]["vzp"].item()
    
    names = [eq.gravity(), eq.winds(), eq.drift()]
    
    for n, s, label in zip(n_dfs, s_dfs, names):
        
        ax.plot((n + s) * 1e4, label = label)
        ax.axhline(0, linestyle = '--')
        ax.set(ylim = [-10, 20], 
               title = f'Vzp = {vzp} m/s')
        
    return s_dfs[0]

def plot_compare_fluxtube():
    fig, ax = plt.subplots(
        figsize = (16, 8),
        sharey = "row",
        sharex= 'col',
        ncols = 3,
        nrows = 2,
        dpi = 300
        )
    
    plt.subplots_adjust(
        hspace = 0.1, 
        wspace = 0.1)
    
    dates = pd.date_range(
        "2013-3-16 20:00", 
        freq = "1D", 
        periods = 3)
    
            
    for i, dn in enumerate(dates):
    
        df = plot_gammas(ax[0, i], dn)
        
        plot_roti(ax[1, i], df, hour_locator = 1)
        
        if i >= 1:
            ax[1, i].set(ylabel = '')
    
    eq = rt.EquationsFT()
    
    ax[0, 0].set(ylabel = eq.label)
        
    ax[0, 1].legend(
        bbox_to_anchor = (0.5, 1.35), 
        ncol = 3, 
        loc = 'upper center'
        )
    
    
    fig.suptitle('Efeitos integrados com vento paralelo a B', y = 1.05)
    
    return fig


fig = plot_compare_fluxtube()


# fig.savefig("RayleighTaylor/figures/paralelo_winds_effects_ft.png")