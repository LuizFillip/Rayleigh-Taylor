import matplotlib.pyplot as plt
import ionosphere as io
from utils import smooth2, translate
import FluxTube as ft
import datetime as dt


def effects_due_gravity(infile, 
        hemisphere = "north"
        ):
    
    base = io.load_calculate(infile)
    ds = ft.IntegratedParameters(
        base, 
        hemisphere = hemisphere
        )
    
    alts = ds.index
    
    r = ft.ratio(base)
    
    K = ft.gradient_integrated(ds["N"], alts)
    
    if  hemisphere == "north":
        ratio = r.north.dropna()
    else:
        ratio = r.south.dropna()
    
    gamma = ratio * (9.81 / ds["nui"]) * K 
    return alts, gamma


fig, ax = plt.subplots(
    figsize = (4, 5),
    dpi = 300)

infile = "database/FluxTube/201301012100.txt"


for hem in ["south", "north"]:
    alts, gamma = effects_due_gravity(infile, 
            hemisphere = hem
            )
    
    gamma = smooth2(gamma, 10)
    
    label = translate(hem).title()
    ax.plot(gamma * 1e4, alts, label = label)
    
gmax = 2
ax.legend(loc = "upper right")
ax.axvline(0, linestyle = "--")

name = "$\gamma_{FT} = \\frac{\Sigma_P^F}{\Sigma_P^E + \Sigma_P^F}(\\frac{g_e}{\\nu_{eff}^{F}})K^F$"

ax.set(ylabel = "Altura (km)", 
       xlabel = "$\gamma_{RT} ~(10^{-4}~s^{-1})$", 
       xlim = [-gmax, gmax], 
       title = name)


