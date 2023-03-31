import matplotlib.pyplot as plt
import datetime as dt
import settings as s
from Results.utils import get_dusk
from RayleighTaylor.src.common import get_pre, load
from RayleighTaylor.src.RT import growth_rate_RT
from RayleighTaylor.base.plotting.plot_effective_winds import plot_meridional

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
    
    ax.text(0.55, 0.8, eq, transform = ax.transAxes)
    
    ax.grid()
    
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
    
    ax.grid()
    
    ax.set(ylabel = "ROTI (TECU/min)", 
              xlabel = "Hora universal", 
              ylim = [0, 6], 
              xlim = [ROTI.index[0], 
                      ROTI.index[-1]])

def plot_timeseries_parameters(
        dn = dt.datetime(2013, 1, 1, 20, 0)
        ):
    
    ts = load()
    
    label = [r"$U_\theta$ (meridional)", 
             r"$U_\phi$ (zonal)", 
             r"$U_y = (U_\phi \cos D + U_\theta \sin D)$",
             r"$U_x = (U_\theta \cos D - U_\phi \sin D)\cos I$"
             ]
    
    df = ts.drift()
    
    df = df.loc[df.index.date == dn.date()]
    
    tpre, vpre = get_pre(dn.date(), df)
    
    
    wd = SET(dn, ts.HWM())
    
    
    fig, ax = plt.subplots(figsize = (12, 8), 
                           sharex = True, 
                           nrows = 3)
    
    plt.subplots_adjust(hspace = 0.1)
    
    U = plot_meridional(ax[0], wd)
    
    gamma =  growth_rate_RT(
          SET(dn, ts.MSIS())["nu"], 
          ts.IRI()["L"], 
          SET(dn, ts.MSIS())["R"], 
          vpre, 
          U
          )
    
    plot_gamma_part(
            ax[1],
            
            gamma
            )
    
    plot_roti_part(ax[2], SET(dn, ts.roti()))
    
    for ax in ax.flat:
        
        sunset, dusk = get_dusk(dn.date())
        args = dict(lw = 2,  color = "k")
        ax.axvline(sunset, **args)
        ax.axvline(dusk, linestyle = "--", **args)
        
        
    fig.suptitle(
        dn.strftime("%d/%m/%Y"), y = 0.92
        )
        
plot_timeseries_parameters(
        dn = dt.datetime(2013, 1, 1, 20, 0)
        )