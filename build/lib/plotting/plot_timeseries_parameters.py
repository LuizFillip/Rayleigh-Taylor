import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import setup as s
from Results.utils import get_dusk
from Digisonde.drift import load_DRIFT
from FabryPerot.core import (load_FPI, 
                             load_HWM,
                             filter_times, 
                             load_ROTI)

from RayleighTaylor.core import (timerange_msise, 
                                 timerange_iri, 
                                 growth_rate_RT)

from RayleighTaylor.base.neutral import eff_wind







start = dt.datetime(2013, 1, 1, 20)

ROTI = filter_times(
    start, 
    load_ROTI()
    )

HWM = filter_times(
    start, 
    load_HWM()
    )

DRF = filter_times(
    start, 
    load_DRIFT(smoothed = True)
    )
FPI = filter_times(
    start, 
    load_FPI(resample = None)
    )




neu = timerange_msise(start)

ion = timerange_iri()

#%%



#----------

def plot_drift_part(ax, DRF):
    ax.plot(DRF["vz"], color = "k")
    vpre, tpre = get_pre(start, DRF)
    ax.axvline(tpre, color = "k", 
               linestyle = "--",
               label = f"Vzp = {vpre} m/s")
    ax.legend()
    ax.axhline(0, linestyle = "--", color = "r")
    ax.set(
        ylim = [-50, 50], 
        ylabel = r"$V_z ~ (ms^{-1})$"
        )


#----------

def plot_winds_part(ax, FPI):
    #check esse sinal
    FPI["Uy"] = eff_wind(FPI.zon, FPI.mer).eff_zonal
    FPI["Ux"] = eff_wind(FPI.zon, FPI.mer, ).eff_meridional
    
    ax.plot(
        FPI[["mer", "zon", "Uy", "Ux"]], 
        label = [r"$U_\theta$ (meridional)", 
                 r"$U_\phi$ (zonal)", 
                 r"$U_y = (U_\phi \cos D + U_\theta \sin D)$",
                 r"$U_x = (U_\theta \cos D - U_\phi \sin D)\cos I$"
                 ] #r"$U_y + U_x$"
            )
    
    
    ax.set(ylabel = r"Velocidade $~(ms^{-1})$", 
           ylim = [-100, 200])
    
    ax.axhline(0, 
               linestyle = "--", 
               color = "r")
    
    ax.legend(
        ncol = 2, 
        loc = "upper right"
        )

#----------

def plot_neutral_part(ax, neu):
    ax1 = ax.twinx()
    
    p, = ax.plot(9.81 / neu["nu"])
    ax1.plot(neu["R"] * 10e3, color = "k")
    
    s.change_axes_color(ax, p)
    
    ax1.set(ylabel = r"$R~(10^{-3} s^{-1})$")
    ax.set(ylabel = r"$g/\nu_{in} ~(ms^{-1})$")

#----------

def plot_gamma_part(ax, 
                    neutro, 
                    iono,
                    drift,
                    wind
                    ):
    
    if isinstance(drift, int):
        vz = 0
    else:
        vz = drift["vz"]        
    
    gamma = growth_rate_RT(
        neutro["nu"], 
        iono["L"], 
        neutro["R"], 
        vz, 
        wind["Ux"]
        ).interpolate()
    
    eq = (r"$\gamma_{RT} = (Vz - U_{eff} + " + 
          r"\frac{g}{\nu_{in}})\frac{1}{n_e}" +
          r"\frac{\partial n_e}{\partial y} - R$")
    
    ax.text(0.7, 0.8, eq, transform = ax.transAxes)
    
    ax.plot(gamma * 1e3, 
            color = "k",
            marker = "o",
            linestyle = "-")
    ax.set(ylim = [-1.5, 1.5], 
           ylabel = "$\gamma_{RT} ~ (10^{-3}s^{-1})$")

    ax.axhline(0, 
               color = "r", 
               linestyle = "--")

#----------

def plot_iono_part(ax, ion):
    ax1 = ax.twinx()
    
    p, = ax.plot(ion["Ne"] * 1e-6)
    ax.set(ylabel = "Ne ($10^{6}~cm^{-3}$)")
    s.change_axes_color(ax, p)
    
    ax1.plot(ion["L"] * 1e5, color = "k")
    ax1.set(ylabel = "$L^{-1}~(10^{-5}~m^{-1}$)")
    
    
#----------

def plot_roti_part(ax, ROTI):
    y = ROTI["roti"].values
    x = ROTI.index.values 
    ax.bar(x, y, width = 0.001, color = "k")   
    ax.axhline(1, 
               linestyle = "-", 
               color = "r", 
               lw = 2, 
               label = "1 TECU/min"
               )
    ax.legend(loc = "upper right")
    
    s.format_axes_date(
        ax, 
        time_scale = "hour", 
        interval = 2
        )
    
    ax.set(ylabel = "ROTI (TECU/min)", 
              xlabel = "Hora universal", 
              ylim = [0, 6], 
              xlim = [ROTI.index[0], 
                      ROTI.index[-1]])
    
def plot_timeseries_parameters():
    
    fig, ax = plt.subplots(nrows = 6, 
                           figsize = (12, 14), 
                           sharex = True)
    
    plt.subplots_adjust(hspace = 0.1)
    
    fig.suptitle(start.strftime("%d/%m/%Y"), y = 0.9)
    
    plot_drift_part(ax[0], DRF)
    plot_winds_part(ax[1], HWM)
    plot_neutral_part(ax[2], neu)
    plot_iono_part(ax[3], ion)
                        
    plot_gamma_part(ax[4], 
                    neu, 
                    ion,
                    DRF,
                    HWM)
    
    plot_roti_part(ax[5], ROTI)
    
    dusk = get_dusk(start.date())
    
    for ax in ax.flat:
        ax.axvline(dusk, color = "k", lw = 2, 
                   label = "Terminator")
    
    ax.legend()
    
plot_timeseries_parameters()