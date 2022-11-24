import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib.ticker as ticker

from plotConfig import *
infile = "database/growthRates/gammas250_350km.txt"


def plotAnnualVariation(infile, year = 2014):
    
    
    df = pd.read_csv(infile, index_col = 0)
    
    df.index = pd.to_datetime(df.index)
    
    df = df.loc[df.index.year == year]
    
    fig, ax = plt.subplots(figsize = (25, 12))
    
    args = dict(lw = 3)
    
    
    ax.plot(df["all"], **args, label = "Todos os termos")
    ax.plot(df["nowind"], **args, label = "$U = 0$")
    ax.plot(df["noreco"], **args, label = "$R = 0$")
    ax.plot(df["nowindReco"], **args, label = "$R = U = 0$")
    ax.plot(df["local"], **args, label = "$R = U = V_z = 0$")
    
    
    ax.set(ylim = [-0.5e-3, 2e-3], 
           xlabel = "Meses", 
           ylabel = "$\gamma_{RT}~ (10^{-3} s^{-1})$")
    
    
    ax.legend(bbox_to_anchor=[1.02, 1.15], ncol = 5, fontsize = 30)
    
    ax.axhline(0, linestyle = "--", color = "k", lw = 3)
    
    ax.xaxis.set_major_formatter(dates.DateFormatter('%b'))
    ax.xaxis.set_major_locator(dates.MonthLocator(interval = 1))
    
    ax.text(0.01, 0.9, year, transform = ax.transAxes)
    
    ax.yaxis.set_major_formatter(
                    ticker.FuncFormatter(lambda y, _: '{:g}'.format(y/1e-3)))
    plt.show()
    
    return fig
    
year = 2014
df = pd.read_csv(infile, index_col = 0)

df.index = pd.to_datetime(df.index)

df = df.loc[df.index.year == year]

fig, axs = plt.subplots(nrows = 5, figsize = (20, 25), 
                       sharex = True)

plt.subplots_adjust(hspace = 0.1)

col = df.columns
names = ["Todos os termos", "$U = 0$", "$R = 0$", 
         "$R = U = 0$", "$V_p = R = U = 0$"]

for num, ax in enumerate(axs.flat):

    ax.plot(df[col[num]], 
            lw = 3, 
            color = "k", 
            label = names[num])
    
    ax.set(ylim = [-0.3e-3, 3e-3], 
           ylabel ='$\gamma_{RT}~(s^{-1})$')
    
    ax.legend(loc = "upper left")    
    
    if num == 4:
        ax.set_xlabel("Meses")

ax.xaxis.set_major_formatter(dates.DateFormatter('%b'))
ax.xaxis.set_major_locator(dates.MonthLocator(interval = 1))

#fig = plotAnnualVariation(infile)


#fig.savefig(path_tex("results") + "\\annual_growth_rates.png", dpi = 300)