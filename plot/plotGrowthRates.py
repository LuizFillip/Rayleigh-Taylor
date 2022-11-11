import pandas as pd
from generalized_growth_rate import *
from datetime import datetime
import matplotlib.pyplot as plt
from plotConfig import *


infile = "database/PRE/FZ_PRE_2014_2015.txt"

pre = PRE(infile)
i = 0

date = pre.times[i]

vz = pre.pre[i]

pyglow = getPyglow(date)


ne = pyglow.density()
u = pyglow.winds()
dat = runMSISE(date)


neutral = neutral_parameters(dat.Tn.values, 
                              dat.O.values, 
                              dat.O2.values, 
                              dat.N2.values)

nu = neutral.collision
r = neutral.recombination

l = length_scale_gradient(ne*1e6)

alts = dat.index.values

gamma = growth_rate_RT(nu, l, r, vz, u)
no_wind = growth_rate_RT(nu, l, r, vz, 0)
no_r = growth_rate_RT(nu, l, 0, vz, u)
no_r_wind = growth_rate_RT(nu, l, 0, vz, 0)
local = growth_rate_RT(nu, l, 0, 0, 0)


fig, ax = plt.subplots(figsize = (12, 18))

args = dict(lw = 4)
ax.plot(gamma, alts, **args, label = "todos os termos")
ax.plot(no_wind, alts, **args, label = "$U = 0$")
ax.plot(no_r, alts, **args, label = "$R = 0$")
ax.plot(no_r_wind, alts, **args, label = "$R = U = 0$")
ax.plot(local, alts, **args, label = "$R = U = V_z = 0$")

ax.legend()
ax.set(xlim = [-6e-3, 6e-3], 
          xlabel = ("Taxa de crescimento,\n" + 
                    r"$\gamma_{RT}~(10^{-3} s^{-1})$"))


ax.xaxis.set_major_formatter(
    ticker.FuncFormatter(lambda y, _: '{:g}'.format(y/10e-3)))


plt.show()