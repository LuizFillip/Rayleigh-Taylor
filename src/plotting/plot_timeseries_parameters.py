import matplotlib.pyplot as plt
import datetime as dt
import settings as s
from Results.utils import get_dusk
from RayleighTaylor.src.common import  load, SET
from RayleighTaylor.src.RT import growth_rate_RT
from RayleighTaylor.src.core import timerange_MSISE
#from base.plotting.plot_effective_winds import plot_meridional
import numpy as np

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
        D = np.deg2rad(D)
        # Ueff_y (positiva para leste)
        return (zon * np.cos(D) + mer * np.sin(D))
    
    @staticmethod
    def eff_meridional(zon, mer, D, I):
        D = np.deg2rad(D)
        I = np.deg2rad(I)
        # Ueff_x (positiva para sul)
        return (
            mer * np.cos(D) + zon * np.sin(D)
                ) * np.cos(I)


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

def plot_terminators(ax, dn):

    ax[0].text(0.03, 1.03, "0 km", 
               transform = ax[0].transAxes)
    ax[0].text(0.13, 1.03, "300 km", 
               transform = ax[0].transAxes)
    
    for ax in ax.flat:
        
        sunset, dusk = get_dusk(dn.date())
        args = dict(lw = 2,  color = "k")
        ax.axvline(sunset, **args)
        ax.axvline(dusk, linestyle = "--", **args)
        
        ax.grid()

def plot_gamma_part(
        ax,
        gamma
        ):
    eq = (r"$\gamma_{RT} = (V_{zp} - U_y^{ef} + " + 
          r"\frac{g}{\nu_{in}})\frac{1}{n_e}" +
          r"\frac{\partial n_e}{\partial y} - R$")
    
    ax.text(0.65, 0.8, eq, transform = ax.transAxes)
        
    ax.plot(gamma * 1e3, 
            color = "k",
            marker = "o",
            linestyle = "-")
    ax.set(ylim = [-1.5, 1.5], 
           ylabel = "$\gamma_{RT} ~ (10^{-3}s^{-1})$")

    ax.axhline(0, 
               color = "r", 
               linestyle = "--")



def plot_roti_part(ax, ROTI):
    y = ROTI.iloc[:, 0].values
    x = ROTI.index.values 
    ax.bar(x, y, width = 0.001, color = "k")   
    
    ax.axhline(1, 
               linestyle = "-", 
               color = "r", 
               lw = 1, 
               label = "1 TECU/min"
               )
    ax.legend(loc = "upper right")
    
    s.format_axes_date(
        ax, 
        time_scale = "hour", 
        interval = 1
        )
        
    ax.set(ylabel = "ROTI (TECU/min)", 
              xlabel = "Hora universal", 
              ylim = [0, 6], 
              xlim = [ROTI.index[0], 
                      ROTI.index[-1]])

def plot_timeseries_parameters(dn, iri_file):
    
    ts = load()
    
    df = ts.pre(infile = "database/Drift/PRE/SAA/2013.txt")
    
    df = df.loc[df.index.date == dn.date(), "vp"]
    
    vpre = df.item()
    wd = SET(dn, ts.HWM())
    
    msis = timerange_MSISE(dn, fixed_alt = 300)
    
    fig, ax = plt.subplots(
        figsize = (10, 8), 
        sharex = True, 
        nrows = 3
        )
    
    plt.subplots_adjust(hspace = 0.1)
    
    U = plot_meridional(ax[0], wd)

    
    gamma =  growth_rate_RT(
          msis["nu"], 
          ts.IRI(infile = iri_file)["L"], 
          msis["R"], 
          vpre, 
          U
          )
    
    ax[1].text(
        0.8, 0.2, 
        f"Vzp = {vpre} m/s", 
        transform = ax[1].transAxes
        )
    
    plot_gamma_part(ax[1], gamma)
    
    plot_roti_part(ax[2], SET(dn, ts.roti()))
    
    plot_terminators(ax, dn)

    fig.suptitle( 
        "São Luis - " + 
        dn.strftime("%d/%m/%Y"), 
        y = 0.92
        )
    
    return fig


dn = dt.datetime(2013, 1, 1, 20, 0)
iri_file = "database/IRI/SAA/20130101.txt"
plot_timeseries_parameters(dn, iri_file)
