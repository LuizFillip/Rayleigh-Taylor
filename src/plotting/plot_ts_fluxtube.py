import matplotlib.pyplot as plt
import datetime as dt
import settings as s
from settings import axes_hour_format, secondary_axis, axes_date_format
from results import plot_roti_maximus
from GEO import dawn_dusk






def plot_timeseries_parameters(df, alt, hemisphere):
    fig, ax = plt.subplots(
        figsize = (8, 8), 
        sharex = True,
        nrows = 4, 
        dpi = 300
        )
    
    plt.subplots_adjust(hspace= 0.1)
    
    infile = "database/Results/maximus/2013.txt"
    
    
    ax[1].plot(df['gamma_g'] * 1e4)
    
    ax[1].set(ylim = [-5, 5], 
              ylabel = "$\gamma_{FT} ~(\\times 10^{-4}~s^{-1})$"
              )
    
    name = "$\gamma_{FT} = \\frac{\Sigma_P^F}{\Sigma_P^E + \Sigma_P^F}(\\frac{g_e}{\\nu_{eff}^{F}})K^F$"
    
    ax[1].text(0.05, 0.8, name, transform = ax[1].transAxes)
    
    
    ax[2].plot(df[['gamma_zon', 'gamma_zon_ef']] * 1e4)
    
    ax[2].legend(["Geográfico", "Efetivo"], 
                 loc = "upper right",
                 ncol = 2)
    
    name = "$\gamma_{FT} = \\frac{\Sigma_P^F}{\Sigma_P^E + \Sigma_P^F}(-U_L^P + \\frac{g_e}{\\nu_{eff}^{F}})K^F$"
    
    ax[2].text(0.05, 0.8, name, transform = ax[2].transAxes)
    
    ax[2].set(ylim = [-17, 17], 
              ylabel = "$\gamma_{FT} ~(\\times 10^{-4}~s^{-1})$"
              )
    
    
    plot_roti_maximus(
        ax[3], "database/Results/maximus/2013.txt", 
        start = df.index[0], 
        delta_hours = df.index[-1]
        )
     



import RayleighTaylor as rt

eq = rt.EquationsFT(wind_sign = "positive")

eqs_gamma = [eq.gravity, eq.winds, eq.drift]
col_gamma = ["gamma_g", "gamma_zon_ef", "gamma_vp"]

infile = "database/RayleighTaylor/winds_positive/02_north.txt"

df = rt.set_data(infile, alt = 300)

df = df.loc[(df.index >= df.index[0]) & 
       (df.index <= df.index[0] + dt.timedelta(days = 5))]

    
fig, ax = plt.subplots(
    figsize = (12, 8), 
    sharex = True,
    nrows = 4, 
    dpi = 300 
    )

plt.subplots_adjust(hspace= 0.1)

plot_roti_maximus(
    ax[3], "database/Results/maximus/2013.txt", 
    start = df.index[0], 
    delta_hours = df.index[-1]
    )


        
        
axes_hour_format(ax[3], hour_locator = 6)

ax1 = secondary_axis(ax[3])

axes_date_format(ax1)

for num, ax in enumerate(ax.flat):


     if num < 3:
         ax.text(
             0.03, 0.8, eqs_gamma[num], 
             transform = ax.transAxes
             )
        
         ax.plot(df[col_gamma[num]] * 1e4)
         
         ax.set(ylabel = eq.label, ylim = [-5, 20])
         
         
         


