import FluxTube as ft
import ionosphere as io
from utils import smooth2, translate
import matplotlib.pyplot as plt



def effects_due_to_winds(infile, 
        wind_type = "zon",
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
    
    gamma = ratio * (- ds[wind_type] + (9.81 / ds["nui"])) * K 
    return alts, gamma




def plot_FT_growth_rate(
        infile,
        ax, 
        hemisphere = "north", 
        wind = "zon"
        ):
    
    alts, gamma = effects_due_to_winds(infile, 
            wind_type = wind,
            hemisphere = hemisphere
            )
    
    gamma = smooth2(gamma, 10)
    
    if wind == "zon":
        label = "Geográfico"
    else:
        label = "Efetivo"
        
    ax.plot(gamma * 1e4, alts, label = label)
    ax.set(xlim = [-4, 4],
           title = translate(hemisphere).title(),
           ylabel = "Altura de Apex (km)", 
           xlabel = "$\gamma_{FT} ~(\\times 10^{-4}~s^{-1})$", )
    ax.axvline(0, linestyle = "--")
    
    ax.legend(loc = "upper right")
    
    return ax
    

fig, ax = plt.subplots(
    figsize = (7, 6), 
    sharey = True,
    ncols = 2,
    dpi = 300)

plt.subplots_adjust(wspace = 0.05)

infile = "database/FluxTube/201301012100.txt"

for wind in ["zon", "zon_ef"]:
    
    plot_FT_growth_rate(infile, ax[0], "north", wind)
    ax1 = plot_FT_growth_rate(infile, ax[1], "south", wind)
    ax1.set(ylabel = "")

name = "$\gamma_{FT} = \\frac{\Sigma_P^F}{\Sigma_P^E + \Sigma_P^F}(-U_L^P + \\frac{g_e}{\\nu_{eff}^{F}})K^F$"
# name = "$$"
#ax[0].text(1.2, 0.05, name, transform = ax[0].transAxes)
fig.suptitle(name)

plt.show()