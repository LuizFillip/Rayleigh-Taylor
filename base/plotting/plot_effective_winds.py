import datetime as dt
import matplotlib.pyplot as plt
from RayleighTaylor.src.common import load
import settings as s
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
  
def plot_zonal(ax, df, d, **kargs):
     
    eq = r"$U_y = (U_\phi \cos D + U_\theta \sin D)$"
    
    U = effective_wind()
    
    d, i = run_igrf(**kargs)

    Uy = U.eff_zonal(df["zon"], df["mer"], d)
    
    d = round(d, 2)
    
    ax.plot(Uy, label = f"{eq}\nD = {d}°", 
            lw = 2, color = "k")
    ax.legend(loc = "upper right")
        
    ax.grid()
    ax.set(
           ylabel = "$U_x^{ef}$ (m/s)", 
           ylim = [-100, 200])
    
    s.format_axes_date(
        ax, 
        time_scale = "hour", 
        interval = 4)
    
    return Uy


kargs = dict(date = 2013, 
             site = "saa", 
             alt = 300)
    
def plot_meridional(
        ax, 
        df, 
        **kargs
        ):
    
    U = effective_wind()
    
    #d, i = run_igrf(**kargs)\\
        
    d, i = -19.6, -6
    
    Ux = U.eff_meridional(df.zon, df.mer, d, i)
    
    d, i = round(d, 2), round(i, 2)
    
    eq = r"$U_x = (U_\theta \cos D + U_\phi \sin D)\cos I$"
    
    ax.plot(Ux, 
            label = f"{eq}\nD = {d}°, I = {i}°", 
            lw = 2, 
            color = "k"
            )
    ax.legend(loc = "upper right")
             
    ax.set(
        ylabel = "$U_y^{ef}$ (m/s)", 
        ylim = [-100, 100]
        )
    
    s.format_axes_date(
        ax, 
        time_scale = "hour", 
        interval = 1
        )
    return Ux 
    
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
        
        #df["mer"] = df["mer"] * (-1) # if south is positive
        
        U = effective_wind()
        d, i = run_igrf(date, 
                        site = site, 
                        alt = alt)
        
        d, i = round(d, 2), round(i, 2)
        
        #d, i = mag[site]
        
        plot_meridional(ax[0], df, d, i, names[n], colors[n])
        plot_zonal(ax[1], df, d, names[n], colors[n])
        
    fig.suptitle(date.strftime("%d/%m/%Y - (%j)") + " - HWM93")
    return fig

# plot_effective_winds(
#         date = dt.datetime(2002, 10, 11), 
#         alt = 350
#         )