import pandas as pd
from generalized_growth_rate import getPyglow, length_scale_gradient
from datetime import datetime
import matplotlib.pyplot as plt
from plotConfig import *
import matplotlib.ticker as ticker

date = datetime(2014, 1, 1, 21, 10)

pyglow = getPyglow(date)


ne = pyglow.density()


fig, ax = plt.subplots(ncols = 2, 
                       sharey = True, 
                       figsize = (18, 18))


plt.subplots_adjust(wspace = 0.1)

alts = np.arange(100, 600 + 1, 1)


ax[0].plot(ne, alts, lw = 4, color = "k")

ax[1].plot(length_scale_gradient(ne), alts, lw = 4, color = "k")

ax[0].set(ylabel = "Altitude (km)", 
          xscale = "log", 
          xlabel = ("Densidade eletrônica,\n"+ 
                              r" $n_0~(cm^{-3}$)"),)


ax[1].xaxis.set_major_formatter(
    ticker.FuncFormatter(lambda y, _: '{:g}'.format(y/10e-3)))
ax[1].set(xlabel = ("Gradiente de escala (L) \n" + 
       r"$\frac{1}{n_0} \frac{\partial n_0}{\partial z} (10^{-3} m^{-1})$"))

text_painels(ax, x = 0.05, y = 0.95, 
                 fontsize = 45)
fig.savefig(path_tex["latex"] + "electron_density.png", 
            dpi = 500)