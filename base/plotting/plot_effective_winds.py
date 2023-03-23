import datetime as dt
import matplotlib.pyplot as plt
from RayleighTaylor.src.common import load
import setup as s
from RayleighTaylor.base.winds import effective_wind
from GEO.core import run_igrf


mag = {
           "car": (-7.38, -36.528),  # Cariri
            "for": (-3.73, -38.522),  # Fortaleza
            "saa": (-2.53, -44.296),  # Sao Luis
            "boa": (-14, 22),      # Boa Vista
            "ccb": (-16.7, -4.2),     # Cachimbo
            "cgg": (-15.1, -22.3) # Campo Grande
              }  
  
def plot_zonal(ax, U, df, d, site, color):

    Uy = U.eff_zonal(df["zon"], df["mer"], d)
    
    ax.plot(Uy, label = f"{site}: D = {d}°", color = color)
    ax.legend(loc = "lower left")
        
    ax.grid()
    ax.set(xlabel = "Hora local", 
           ylabel = "Velocidade zonal [+L] (m/s)", 
           ylim = [-200, 240])
    
    s.format_axes_date(
        ax, 
        time_scale = "hour", 
        interval = 4)
    
def plot_meridional(ax, U, df, d, i, site, color):

    Ux = U.eff_meridional(df.zon, df.mer, d, i)
    ax.plot(Ux, label = f"{site}: D = {d}°, I = {i}°", color = color)
    ax.legend(loc = "lower left")
        
    ax.grid()
    
    ax.set(xlabel = "Hora local", 
           ylabel = "Velocidade meridional [+S] (m/s)", 
           ylim = [-120, 120])
    
    s.format_axes_date(
        ax, 
        time_scale = "hour", 
        interval = 4
        )
    
def plot_effective_winds(
        date = dt.datetime(2002, 10, 11), 
        alt = 350
        ):
    
    fig, ax = plt.subplots(
        figsize = (15, 5), 
        ncols = 2, 
        sharex = True
        )    
    plt.subplots_adjust(wspace = 0.2)
    
    names = ["Boa Vista", "Cachimbo", "Campo Grande"]
    
    colors = ["red", "black", "blue"]
    
    for n, site in enumerate(["boa", "ccb", "cgg"]):
        
        ts = load()
    
        df = ts.HWM(infile = f"database/HWM/HWM93/{site}3502002.txt")
        
        df.index = df.index - dt.timedelta(hours = 3)
        
        df = df.loc[df.index.date == date.date()]
        
        df["mer"] = df["mer"] * (-1) # if south is positive
        
        U = effective_wind()
        d, i = run_igrf(date, 
                        site = site, 
                        alt = alt)
        
        d, i = round(d, 2), round(i, 2)
        
        #d, i = mag[site]
        
        plot_meridional(ax[0], U, df, d, i, names[n], colors[n])
        plot_zonal(ax[1], U, df, d, names[n], colors[n])
        
    fig.suptitle(date.strftime("%d/%m/%Y - (%j)") + " - HWM93")
    return fig

plot_effective_winds(
        date = dt.datetime(2002, 10, 11), 
        alt = 350
        )