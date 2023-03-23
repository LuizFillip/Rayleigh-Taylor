import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import setup as s
from Results.utils import get_dusk
from RayleighTaylor.src.common import get_pre, load
from RayleighTaylor.src.RT import growth_rate_RT
from RayleighTaylor.base.winds import effective_wind
from GEO.core import run_igrf








dn = dt.datetime(2013, 1, 1, 20, 0)



def SET(dn, df):
    end = dn + dt.timedelta(hours = 11)

    return df.loc[(df.index >= dn ) & 
              (df.index <= end) , :]

def plot_gamma_part(
        ax,
        gamma
        ):


    
    eq = (r"$\gamma_{RT} = (V_{zp} - U_y^{ef} + " + 
          r"\frac{g}{\nu_{in}})\frac{1}{n_e}" +
          r"\frac{\partial n_e}{\partial y} - R$")
    
    ax.text(0.5, 0.8, eq, transform = ax.transAxes)
    
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


ts = load()

#df = ts.HWM()

df = ts.drift()

df = df.loc[df.index.date == dn.date()]

tpre, vpre = get_pre(dn.date(), df)


wd = SET(dn, ts.HWM())

wind = effective_wind()
d, i = run_igrf(2013, site = "saa", alt = 300)


gamma =  growth_rate_RT(
      SET(dn, ts.MSIS())["nu"], 
      ts.IRI()["L"], 
      SET(dn, ts.MSIS())["R"], 
      vpre, 
      wind.eff_zonal(
          wd["zon"], wd["mer"], d)
      )

fig, ax = plt.subplots(figsize = (8, 6), 
                       sharex = True, 
                       nrows = 3)

plt.subplots_adjust(hspace = 0.1)

fig.suptitle(dn.strftime("%d/%m/%Y"), y = 0.92)


dusk = get_dusk(dn.date())

ax[0].plot( wind.eff_zonal(
     wd["zon"], wd["mer"], d), color = "k")

ax[0].set(ylim = [0, 200], 
          ylabel = "$U_y^{ef}$ (m/s)")

plot_gamma_part(
        ax[1],
        gamma
        )

plot_roti_part(ax[2], SET(dn, ts.roti()))


#%%



def plot_winds_part(ax, FPI):
    #check esse sinal
    FPI["Uy"] = eff_wind(FPI.zon, FPI.mer).eff_zonal
    FPI["Ux"] = eff_wind(FPI.zon, FPI.mer).eff_meridional
    
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






    
def plot_timeseries_parameters():
    
    fig, ax = plt.subplots(nrows = 6, 
                           figsize = (12, 14), 
                           sharex = True)
    
    plt.subplots_adjust(hspace = 0.1)
    
    fig.suptitle(start.strftime("%d/%m/%Y"), y = 0.9)
    

    dusk = get_dusk(start.date())
    
    for ax in ax.flat:
        ax.axvline(dusk, color = "k", lw = 2, 
                   label = "Terminator")
    
    ax.legend()
    
