from utils import translate
import matplotlib.pyplot as plt
import RayleighTaylor as rt
from settings import axes_hour_format, secondary_axis, axes_date_format
from results import plot_roti_maximus
from utils import save_but_not_show
import os

def plot_roti(ax, ds):
    
    plot_roti_maximus(
        ax, 
        "database/Results/maximus/2013.txt", 
        start = ds.index[0], 
        delta_hours = ds.index[-1],
        station = "salu")
    
    axes_hour_format(ax, hour_locator = 6, tz = "UTC")
    
    ax1 = secondary_axis(ax)
    ax.set(xlabel = "Hora universal")
    axes_date_format(ax1)

def plot_winds_ts(ax, ds, cols, sign = -1):
    
    if "zon" in cols:
        coord =  "Zonal"
    else:
        coord = "Meridional"

    for wd in cols:
        gamma = rt.effects_due_to_winds(
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
        
    ax.set(ylim = [-15, 15])
    
    


def plot_winds_and_roti(infile, hemisphere):
    
    fig, ax = plt.subplots(
        figsize = (12, 8), 
        sharex = True,
        sharey = "row",
        ncols = 2, 
        nrows = 3, 
        dpi = 300
        )
        
    plt.subplots_adjust(
        wspace = 0.05, hspace = 0.05)
    
    ds = rt.set_data(infile, hemisphere, alt = 300)
            
    eq = rt.EquationsFT(wind_sign = "negative")
    
        
    for num in range(2):
        ax[num, 0].set(ylabel = eq.label)
        
    eq = rt.EquationsFT(
        wind_sign = "negative"
        )
    
    ax[0, 0].set(title = eq.winds)
    
    plot_winds_ts(ax[0, 0], ds, ["zon", "zon_ef"])
    plot_winds_ts(ax[1, 0], ds, ["mer", "mer_ef"])
    
    eq = rt.EquationsFT(
        wind_sign = "positive"
        )
    
    ax[0, 1].set(title = eq.winds)
    
    plot_winds_ts(ax[0, 1], ds, ["zon", "zon_ef"], sign = 1)
    plot_winds_ts(ax[1, 1], ds, ["mer", "mer_ef"], sign = 1)

    plot_roti(ax[2, 0], ds)
    plot_roti(ax[2, 1], ds)
    
    ax[2, 1].set(ylabel = "")
    
    fig.suptitle(translate(hemisphere.title()))
    
    return fig
    
infile = "database/RayleighTaylor/process/"
filename = "12.txt"


for hemisphere in ["south", "north"]:
    
    fig = plot_winds_and_roti(
        os.path.join(infile, filename), 
        hemisphere)
    
    FigureName = filename.replace(".txt", ".png")
    save_in = f"D:\\plots\\winds_effect\\{hemisphere}_{FigureName}"
    
    save_but_not_show(fig, save_in)

