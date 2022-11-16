import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib.ticker as ticker

from plotConfig import *

df = pd.read_csv("database/growthRates/Gammas.txt", 
                 index_col = 0)

df.index = pd.to_datetime(df.index)

year = 2014

df = df.loc[df.index.year == year]

fig, ax = plt.subplots(figsize = (20, 10))

args = dict(lw = 2)


ax.plot(df["all"], **args, label = "Todos os termos")
ax.plot(df["nowind"], **args, label = "$U = 0$")
ax.plot(df["noreco"], **args, label = "$R = 0$")
ax.plot(df["nowindReco"], **args, label = "$R = U = 0$")
ax.plot(df["local"], **args, label = "$R = U = V_z = 0$")


ax.set(ylim = [-0.5e-3, 3e-3], 
       xlabel = "Meses", 
       title = f"Fortaleza, {year}",
       ylabel = "$\gamma_{RT}~ (\\times 10^{-3} s^{-1})$")


ax.legend(ncol = 3, fontsize = 30)

ax.xaxis.set_major_formatter(dates.DateFormatter('%b'))
ax.xaxis.set_major_locator(dates.MonthLocator(interval = 1))


ax.yaxis.set_major_formatter(
    ticker.FuncFormatter(lambda y, _: '{:g}'.format(y/1e-3)))



fig.savefig(path_tex["latex"] + "annual_growth_rates.png", 
            dpi = 500)


plt.show()