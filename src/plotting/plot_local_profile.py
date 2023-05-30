import matplotlib.pyplot as plt
from GEO import load_meridian
import datetime as dt
import ionosphere as io
import matplotlib.ticker as ticker
from utils import order_magnitude
from labels import Labels
import pandas as pd


def plot_local_growth_rate(
        ax,
        gamma, 
        alts, 
        label        ):

    
    ax.plot(gamma, alts, label = label)
    
    ax.axvline(0, linestyle = "--")
    gmax = 4e-4
    ax.set(ylabel = "Altura (km)", 
           xlabel = "$\gamma_{RT} ~(10^{-4}~s^{-1})$", 
           xlim = [-gmax, gmax], 
           title = "$\gamma_{RT} = \\frac{g}{\\nu_{in}} \\frac{1}{n_0} \\frac{\partial n_0}{\\partial y}$")
    
    factor = pow(10, order_magnitude(gmax))
    ax.legend()
    ax.xaxis.set_major_formatter(
        ticker.FuncFormatter(lambda y, _: '{:g}'.format(y/factor)))
    
    
def local_growth_rate(**kwargs):
      
    base = io.test_data(**kwargs)
    
    return ((9.81/ base["nui"]) * io.scale_gradient(base["ne"]))
    



def plot_local_effect():
    dn = dt.datetime(2013, 1, 1, 21, 0) 
    
    mlon, mlat, _, _, = load_meridian()
    
    fig, ax = plt.subplots(figsize = (5, 4), 
                           dpi = 300)
    
    
    for lat in [-5, round(mlat, 3), 5]:
        
        kwargs = dict(
             dn = dn, 
             glat = lat, 
             glon = mlon,
             hmin = 100,
             hmax = 500
             )
        gamma = local_growth_rate(**kwargs)
        alts = gamma.index
    
        plot_local_growth_rate(
            ax,
            gamma, 
            alts, 
            label = f"latitude: {lat}°")
        
    
    
    
    
infile = "parameters_caj.txt"

df = pd.read_csv(infile, index_col = 0)

df.index = pd.to_datetime(df.index)


def growth_rate_from_df(df):
    df["g"] = df["L"] * (
        (9.81 / df["nui"]) + df["zon"] + df["vz"])
    return df

df = growth_rate_from_df(df).dropna()

times = df.index.unique()

dn = dt.datetime(2013, 3, 17, 0)

ds = df.loc[df.index == dn]



fig, ax = plt.subplots(figsize = (5, 4), 
                       dpi = 300)

ax.plot(ds["g"] *1e4, ds["alt"])

lim_max = ds["g"].max() *1e4 + 2

ax.set(xlim = [-lim_max, lim_max])

def find_alt_maximum(ds):

    ds = ds.set_index("alt")
    return ds["g"].idxmax()


# for alt in [find_alt_maximum(ds), 
#             250, 300, 350]:
#     ax.axhline(alt)


ds