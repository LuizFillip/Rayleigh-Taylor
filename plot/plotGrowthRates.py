import pandas as pd
from common import runMSISE, getPyglow
from RTIparameters import PRE, neutrals, scale_gradient
from datetime import datetime
import matplotlib.pyplot as plt
from plotConfig import *
import matplotlib.ticker as ticker

infile = "database/PRE/FZ_PRE_2014_2015.txt"

pre = PRE(infile)
i = 0

date = pre.times[i]

vz = pre.pre[i]

pyglow = getPyglow(date)


ne = pyglow.density()
u = pyglow.winds()
dat = runMSISE(date)


neutral = neutrals(dat.Tn.values, 
                              dat.O.values, 
                              dat.O2.values, 
                              dat.N2.values)

nu = neutral.collision
r = neutral.recombination

l = scale_gradient(ne*1e6)

alts = dat.index.values

def growth_rate_RT(nu, L, R, Vp, U):
    """
    Generalized instability rate growth
    Paramaters:
    ---------- 
    Vp: Prereversal Enhancement (PRE)
    U: Neutral wind
    nu: ion-neutral collisional frequency
    L: gradient scale
    R: Recombination
    
    """
     
    return (Vp - U + (9.81 / nu))*L - R

gamma = growth_rate_RT(nu, l, r, vz, u)
no_wind = growth_rate_RT(nu, l, r, vz, 0)
no_r = growth_rate_RT(nu, l, 0, vz, u)
no_r_wind = growth_rate_RT(nu, l, 0, vz, 0)
local = growth_rate_RT(nu, l, 0, 0, 0)


fig, ax = plt.subplots(figsize = (8, 15))

args = dict(lw = 3)
ax.plot(gamma, alts, **args, label = r"$(V_{zp} - U + \frac{g}{\nu_{in}})\frac{1}{n_e} \frac{\partial n_e}{\partial y} - R$")
ax.plot(no_wind, alts, **args, label = r"$(V_{zp} + \frac{g}{\nu_{in}})\frac{1}{n_e} \frac{\partial n_e}{\partial y} - R$")
ax.plot(no_r, alts, **args, label = r"$(V_{zp} - U + \frac{g}{\nu_{in}})\frac{1}{n_e} \frac{\partial n_e}{\partial y}$")
ax.plot(no_r_wind, alts, **args, label = r"$(V_{zp} + \frac{g}{\nu_{in}})\frac{1}{n_e} \frac{\partial n_e}{\partial y}$")
ax.plot(local, alts, **args, label = r"$ (\frac{g}{\nu_{in}})\frac{1}{n_e} \frac{\partial n_e}{\partial y}$")

ax.legend(fontsize = 30)
ax.set(xlim = [-3e-3, 3e-3],
       ylabel = "Altitude (km)",
       xlabel = r"$\gamma_{RT}~(10^{-3} s^{-1})$")

ax.axvline(0, lw = 2, color = "k", linestyle = "--")
ax.xaxis.set_major_formatter(
    ticker.FuncFormatter(lambda y, _: '{:g}'.format(y/1e-3)))
infile = "G:\\Meu Drive\\Doutorado\\Modelos_Latex_INPE\\docs\\Proposal\\Figures\\methods\\"
#fig.savefig(infile + "\\growth_rates_profiles.png")
plt.show()