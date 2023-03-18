import numpy as np 
from GEO.core import run_igrf
import pandas as pd
import setup as s


d, i = run_igrf(2013, site = "saa")

class effective_wind(object):
    
    """
    Effective wind along magnetic field
    
    Pag. 27 e 28 (Tese Ely, 2016)
    
    U_theta (mer) = meridional component (positiva para sul)
    U_phi (zon) = zonal component (positiva para leste)
    
    """
    
    @staticmethod
    def eff_zonal(zon, mer, d): 
        D = np.radians(d)
        # positiva para leste
        return (zon * np.cos(D) + mer * np.sin(D))
    
    @staticmethod
    def eff_meridional(zon, mer, d, i):
        D = np.radians(d)
        I = np.radians(i)
        # Ueff_x (positiva para sul)
        return (
            mer * np.cos(D) - zon * np.sin(D)
                ) * np.cos(I)

    

from RayleighTaylor.core import load_HWM
import datetime as dt
import matplotlib.pyplot as plt


df = load_HWM()

date = dt.date(2013, 6, 3)
df = df.loc[df.index.date == date]


U = effective_wind()



def plot_zonal(ax, U, df):

    for d in [-30, 0, 30]:
        Ux = U.eff_zonal(df.zon, df.mer, d)
        ax.plot(Ux, label = f"D = {d}°")
        ax.legend()
        
    ax.axhline(0, color = "r", linestyle = "--")
    
    ax.set(ylabel = "Velocidade (m/s)")
    ax.set(xlabel = "Hora universal (UT)", 
           title = "Zonal")
    s.format_axes_date(
        ax, 
        time_scale = "hour", 
        interval = 4)
    
def plot_meridional(ax, U, df):
    
    for d in [-30, 0, 30]:
        i = -20
        Ux = U.eff_meridional(df.zon, df.mer, d, i)
        ax.plot(Ux, label = f"D = {d}°, I = {i}°")
        ax.legend()
        
    ax.axhline(0, color = "r", linestyle = "--")
    
    ax.set(xlabel = "Hora universal (UT)", 
           title = "Meridional")
    s.format_axes_date(
        ax, 
        time_scale = "hour", 
        interval = 4)
    
    
fig, ax = plt.subplots(figsize = (12, 5), 
                       ncols = 2, 
                       sharey = True, 
                       sharex = True)    
plt.subplots_adjust(wspace = 0.05)
plot_zonal(ax[0], U, df)
plot_meridional(ax[1], U, df)