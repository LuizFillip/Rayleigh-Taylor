import matplotlib.pyplot as plt
from GEO import load_meridian
import datetime as dt
import ionosphere as io
import matplotlib.ticker as ticker
from utils import order_magnitude


def plot_local_growth_rate(
        gamma, 
        alts, 
        factor = 1e4, 
        xlim = 0.5
        ):

    fig, ax = plt.subplots(dpi = 300)
    
    ax.plot(gamma, alts)
    
    ax.axvline(0, linestyle = "--")
    
    gmax = round(gamma.max(), 5)

    ax.set(ylabel = "Altura (km)", 
           xlabel = "$\gamma_{RT} ~(s^{-1})$", 
           xlim = [-gmax, gmax])
    
    factor = pow(10, order_magnitude(gmax))
    
    ax.xaxis.set_major_formatter(
        ticker.FuncFormatter(lambda y, _: '{:g}'.format(y/factor)))
    
    
def local_growth_rate(dn):
    
    mlon, mlat, _, _, = load_meridian()

    kwargs = dict(
         dn = dn, 
         glat = mlat, 
         glon = mlon,
         hmin = 150,
         hmax = 500
         )
     
    base = io.test_data(**kwargs)
    
    return ((9.81/ base["nui"]) * io.scale_gradient(base["ne"]))
    


dn = dt.datetime(2013, 1, 1, 21, 0) 


gamma = local_growth_rate(dn)
alts = gamma.index

plot_local_growth_rate(
        gamma, 
        alts, 
        factor = 1e4, 
        xlim = 0.5
        )





