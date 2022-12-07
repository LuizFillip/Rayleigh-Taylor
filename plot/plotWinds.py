import pandas as pd
from common import getPyglow
from datetime import datetime
import matplotlib.pyplot as plt
from plotConfig import *
import numpy as np


date = datetime(2014, 1, 1, 21, 10)

pyglow = getPyglow(date)


ne = pyglow.density()
u = pyglow.winds(component = ["zon", "mer", "U"])


fig, ax = plt.subplots(ncols = 1, 
                       sharey = True, 
                       figsize = (15, 20))


alts = np.arange(100, 600 + 1, 1)

for i in range(3):
    
    ax.plot(u[:, i], alts, lw = 3)


ax.legend(["$U_\\theta$", "$U_\phi$", "U"])
ax.axvline(0, color = "k", lw = 0.5, linestyle = "--")
ax.set(xlim = [-140, 140], 
       xticks = np.arange(-140, 160, 40),
       ylabel = "Altitude (km)", 
       xlabel = "Velocidade (m/s)")


fig.savefig(path_tex("methods") + "\\winds.png")