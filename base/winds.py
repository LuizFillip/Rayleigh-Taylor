import numpy as np 
from GEO.core import run_igrf
import pandas as pd
import setup as s
from RayleighTaylor.core import load_HWM
import datetime as dt
import matplotlib.pyplot as plt

mag = {
         "car": (-7.38, -36.528),  # Cariri
          "for": (-3.73, -38.522),  # Fortaleza
          "saa": (-2.53, -44.296),  # Sao Luis
          "boa": (-14, 22),      # Boa Vista
          "ccb": (-16.7, -4.2),     # Cachimbo
          "cgg": (-15.1, -22.3) # Campo Grande
            }     
class effective_wind(object):
    
    """
    Effective wind along and perpendicular of 
    magnetic field
    
    Pag. 27 e 28 (Tese Ely, 2016)
    
    U_theta (mer) = meridional component (positiva para sul)
    U_phi (zon) = zonal component (positiva para leste)
    
    """
    
    @staticmethod
    def eff_zonal(zon, mer, D): 
        D = np.radians(D)
        # Ueff_y (positiva para leste)
        return (zon * np.cos(D) + mer * np.sin(D))
    
    @staticmethod
    def eff_meridional(zon, mer, D, I):
        D = np.radians(D)
        I = np.radians(I)
        # Ueff_x (positiva para sul)
        return (
            mer * np.cos(D) - zon * np.sin(D)
                ) * np.cos(I)

    

def plot_zonal(ax, U, df, d, site):

    Ux = U.eff_zonal(df.zon, df.mer, d)
    ax.plot(Ux, label = f"{site}: D = {d}°")
    ax.legend()
        
    ax.axhline(0, color = "r", linestyle = "--")

    ax.set(xlabel = "Hora universal (UT)", 
           
           title = "Zonal", 
           ylim = [-200, 240])
    
    s.format_axes_date(
        ax, 
        time_scale = "hour", 
        interval = 4)
    
def plot_meridional(ax, U, df, d, i, site):

    Ux = U.eff_meridional(df.zon, df.mer, d, i)
    ax.plot(Ux, label = f"{site}: D = {d}°, I = {i}°")
    ax.legend()
        
    ax.axhline(0, color = "r", linestyle = "--")
    
    ax.set(xlabel = "Hora universal (UT)", 
           ylabel = "Velocidade (m/s)",
           title = "Meridional", 
           ylim = [-120, 120])
    s.format_axes_date(
        ax, 
        time_scale = "hour", 
        interval = 4)
    
    
fig, ax = plt.subplots(figsize = (12, 5), 
                       ncols = 2, 
                       sharex = True)    

date = dt.datetime(2002, 10, 11)
alt = 350
names = ["Boa Vista", "Cachimbo", "Campo Grande"]
labels = ["BV", "CX", "CG"]
colors = ["red", "black", "blue"]
for n, site in enumerate(["boa", "ccb", "cgg"]):

    df = load_HWM(infile = f"database/HWM/HWM93/{site}3502002.txt")
    
    
    
    
    df.index = df.index - dt.timedelta(hours = 3.5)
    
    df = df.loc[df.index.date == date.date()]
    
    df["mer"] = df["mer"] * (-1)
    
    U = effective_wind()
    d, i = run_igrf(date, 
                    site = site, 
                    alt = alt)
    d, i = round(d, 3), round(i, 3)
    print(site, i, d)

    plt.subplots_adjust(wspace = 0.15)
    
    ax[1].plot(df["zon"], label = names[n], color = colors[n])
    ax[0].plot(df["mer"] , label = names[n], color = colors[n])
    
    ax[1].legend()
    ax[0].legend()
    ax[1].grid()
    ax[0].grid()
    ax[1].set(ylim = [-240, 280])
    ax[0].set(ylim = [-60, 60])
    s.format_axes_date(
        ax[0], 
        time_scale = "hour", 
        interval = 4)
    
    
    #plot_zonal(ax[1], U, df, d, site)
    #plot_meridional(ax[0], U, df, d, i, site)