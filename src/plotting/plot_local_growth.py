import matplotlib.pyplot as plt
from GEO import load_meridian
import datetime as dt
import ionosphere as io
import matplotlib.ticker as ticker
from utils import order_magnitude


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
    




