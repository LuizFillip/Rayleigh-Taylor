import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import setup as s
from Results.utils import get_dusk
from Digisonde.drift import load_DRIFT
from FabryPerot.core import load_FPI
from RayleighTaylor.core import timerange_msise, timerange_iri, growth_rate_RT
from RayleighTaylor.base.neutral import eff_wind

def load_ROTI():
    infile = "database/Results/maximus/salu_2013.txt"
    df = pd.read_csv(infile, index_col = 0)
    df.index = pd.to_datetime(df.index)
    return df


def filter_times(start, df):
    
    end = start + dt.timedelta(hours = 11)
    return df.loc[(df.index >= start) & 
                 (df.index <= end), :]

def load_HWM():
    infile = "database/HWM/saa_250_2013.txt"
    
    df = pd.read_csv(infile, index_col = "time")
    df.index = pd.to_datetime(df.index)
    del df["Unnamed: 0"]
    
    df["U"] = eff_wind(df["zon"], 
             df["mer"], 
             year = 2013, 
             site = "saa").Nogueira
    return df


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

FPI["U"] = eff_wind(FPI.zon, 
         FPI.mer, 
         year = 2013, 
         site = "saa").Nogueira



neu = timerange_msise(start)

ion = timerange_iri()

#%%
print(HWM.plot())

#%%
def get_pre(dn, df):
    
    b = dt.time(21, 0, 0)
    e = dt.time(22, 30, 0)
    
    df = df.loc[(df.index.time >= b) & 
                (df.index.time <= e) & 
                (df.index.date == dn.date()), ["vz"]]
        
    return round(df.max().item(), 2), df.idxmax().item()

#----------

def plot_drift_part(ax, DRF):
    ax.plot(DRF["vz"], color = "k")
    vpre, tpre = get_pre(start, DRF)
    ax.axvline(tpre, color = "k", 
               linestyle = "--",
               label = f"Vzp = {vpre} m/s")
    ax.legend()
    ax.axhline(0, linestyle = "--", color = "r")
    ax.set(ylim = [-50, 50], 
           ylabel = r"$V_z ~ (ms^{-1})$")
    
#----------

def plot_winds_part(ax, FPI):
    ax.plot(FPI[["zon", "mer", "U"]], 
            label = [r"$U_\theta$ (zonal)", 
                     r"$U_\phi$ (meridional)", 
                     r"$(U_\phi \cos D + U_\theta \sin D)\cos I$"]
            )
    
    ax.set(ylabel = r"Velocidade $~(ms^{-1})$", 
           ylim = [-100, 200])
    ax.axhline(0, linestyle = "--", color = "r")
    ax.legend(loc = "upper right")

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
        wind["U"]
        ).interpolate()
    
    eq = (r"$\gamma_{RT} = (- U_{eff} + " + 
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
              ylim = [0, 6])
    
    
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
                0,
                HWM)

plot_roti_part(ax[5], ROTI)

dusk = get_dusk(start.date())

for ax in ax.flat:
    ax.axvline(dusk, color = "k", lw = 2, 
               label = "Terminator")

ax.legend()