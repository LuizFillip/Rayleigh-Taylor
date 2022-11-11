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

ax.plot(df["nowind"], label = "$U = 0$", **args)
ax.plot(df["noreco"], label = "$R = 0$", **args)
ax.plot(df["nowindReco"], label =  "$U = R = 0$", **args)
ax.plot(df["local"], label = "$U = V_z = R = 0$", **args)
ax.plot(df["all"],  label = "Todos parâmetros", **args)


ax.set(ylim = [-0.5e-3, 3e-3], 
       xlabel = "Meses", 
       title = f"Fortaleza, {year}",
       ylabel = "$\gamma_{RT}~ (\\times 10^{-3} s^{-1})$")


ax.legend(ncol = 3, fontsize = 30)

ax.xaxis.set_major_formatter(dates.DateFormatter('%b'))
ax.xaxis.set_major_locator(dates.MonthLocator(interval = 1))


ax.yaxis.set_major_formatter(
    ticker.FuncFormatter(lambda y, _: '{:g}'.format(y/10e-3)))