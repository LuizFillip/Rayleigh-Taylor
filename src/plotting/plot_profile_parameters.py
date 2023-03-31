import matplotlib.pyplot as plt
from RayleighTaylor.RT import growth_rate_RT
import locale
import numpy as np
import setttings as s

def plot_collision_freq(ax, nu, alts):
    
    name = "Frequência de colisão íon-neutro"
    symbol = "$\nu_{in}$"
    units = "$s^{-1}$"
    
    ax.plot(nu, alts, color = "k", lw = 2) 
    
    ax.set(
        title = name,
        xscale = "log", 
        yticks = np.arange(100, 650, 50),
        ylim = [100, 650],
        xlabel = (f"{symbol} ({units})"),
        ylabel = "Altitude (km)"
        )
    
def plot_recombination_freq(ax, r, alts):
    
    name = "Taxa de recombinação" 
    symbol = "$\nu_R$"
    units = "$s^{-1}$"
    
    
    ax.plot(r, alts, color = "k", lw = 2) 
    ax.set(
        title = name,
        xlabel = (f"{symbol} ({units})"),
        xscale = "log", 
        xlim = [1e-10, 1e3]
            )

def plot_winds(ax, u, alts):
    name = "Ventos termosféricos"
    units = "m/s"
    symbol = "U"
    
    ax.plot(u, alts, color = "k", lw = 2)
    ax.axvline(0, linestyle = "--", color = "r", lw = 2)
    
    ax.set(
        title = name,
        xlabel = (f"{symbol} ({units})"), 
        xlim = [-120, 120], 
        xticks = np.arange(-120, 140, 40)
        )
    ax.legend(loc = "upper right")
    
def plot_electron_density(ax, ne, l, alts):
    
    name = "Densidade eletrônica"
    symbol = "$n_0$"
    units = "$cm^{-3}$"
    
    ax.plot(ne, alts, color = "k", lw = 2)
    ax.set(
        title = name,
        xscale = "log", 
        xlabel = (f"{symbol} ({units})"), 
        ylabel = "Altitude (km)"
        )
    
    name = "Gradiente de escala"
    symbol = "$L^{-1}$"
    units = "$10^{-3} m^{-1}$"
    ax1 = ax.twiny()
    ax1.plot(l, alts, color = "k", lw = 2)
    ax1.set(
        title = name,
        xlabel = (f"{symbol} ({units})")
        )
    
    
def plot_growth_rate_RT(
        ax, 
        nu, l, r, vz, u, alts
        ):
    
    name = "Taxa de crescimento Rayleigh-Taylor"
    symbol = "$\gamma_{RT}$"
    units = "$10^{-3} s^{-1}$"
    
    ax.plot(growth_rate_RT(nu, l, r, vz, u), alts, 
               color = "k", lw = 2)
    
    ax.plot(growth_rate_RT(nu, l, 0, vz, u), alts, 
               label = r"$R = 0 $", lw = 2)
    
    ax.plot(growth_rate_RT(nu, l, r, vz, 0), alts, 
               label = r"$U = 0 $", lw = 2)
    
    ax.legend()
    ax.set(
        title = name,
        xlim = [-6e-3, 6e-3], 
        xlabel = (f"{symbol} ({units})")
        )
    
def plot_profiles_parameters(date):
    fig, ax = plt.subplots(figsize = (17, 20), 
                           ncols = 3,
                           nrows = 2,
                           sharey = True)
    
    #plt.rc('text', usetex = True)
    plt.subplots_adjust(wspace = 0.2)
    
    s.text_painels(ax, x = 0.05, y = 0.94)
    
  
    locale.setlocale(locale.LC_ALL, 'pt_pt.UTF-8')
    time_str = date.strftime("%d de %B de %Y, %H:%M UT")
    fig.suptitle(f"Parâmetros da taxa de crescimento Rayleigh-Taylor, \n {time_str}", y = 0.93)

plot_profiles_parameters(date)
