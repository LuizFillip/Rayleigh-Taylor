import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
from RTIparameters import PRE, neutrals, scale_gradient
from common import loadNe, runMSISE, getPyglow
import os
from tqdm import tqdm

def growth_rate_RT(nu, L, R, Vp, U):
    """
    Generalized instability rate growth
    Paramaters:
    ---------- 
    Vp: Prereversal Enhancement (PRE)
    U: Neutral wind
    nu: ion-neutral collisional frequency
    L: gradient scale
    R: Recombination rate
    
    """
     
    return (Vp - U + (9.81 / nu))*L - R
    



def run_for_all_times(vz, 
                      date, 
                      neInfile = "20140101.txt"):
    """Running for all electron density (range 200 to 500 km)
    in whole day for each 10 minutes"""

    end =  date + datetime.timedelta(hours = 23, minutes = 50)
    
    times = pd.date_range(date, 
                          end, 
                          freq = "10min")
    
    out = []
    
    for date in times:
        
        df = loadNe(neInfile).sel_time(date)
        
        hmin = df.index[0]
        hmax = df.index[-1]
        dat = runMSISE(date, 
                       hmin = hmin, 
                       hmax = hmax)
        neutral = neutrals(dat.Tn.values, 
                            dat.O.values, 
                            dat.O2.values, 
                            dat.N2.values)
        
        nu = neutral.collision
        r = neutral.recombination
        ne = df.values
        
        l = scale_gradient(ne)
        
        alts = dat.index.values
        
        gamma = growth_rate_RT(nu, l, r, vz, 0)
    
        max_gamma = gamma[alts == 300 ]
        out.append(np.nanmax(max_gamma))
        
    return out

def run_for_all_days2():
    gammas = []
    dates = []
    
    pre = PRE("database/PRE/FZ_PRE_2014_2015.txt").df
    
    
    for num in tqdm(pre.index):
        
        try:
            filename = num.strftime("%Y%m%d") + ".txt"
            vz = pre.loc[num, "vz"]
            
            date = pd.to_datetime(num.date())
            
            gammas.append(run_for_all_times(vz, date, 
                          neInfile = "database/density/" + filename))
        
            dates.append(date)
        except:
            continue
        
    return gammas, dates


gammas, dates = run_for_all_days2()
#%%
import plotConfig

x = np.linspace(0, 24, 144)
z = np.array(gammas).T
y = dates

fig, ax = plt.subplots(figsize = (30, 15))
cs = ax.contourf(y, x, z, 30)

import matplotlib.dates as md
ax.xaxis.set_major_formatter(md.DateFormatter('%d-%m'))
ax.xaxis.set_major_locator(md.DayLocator(interval = 10))

cb = plt.colorbar(cs)

cb.set_label(r'$\gamma_{RT}~(s^{-1})$')
ax.set(yticks = np.arange(0, 25, 2),
       ylabel = "Tempo (UT)", 
        xlabel = "Meses")
#%%

def run_for_all_days(pre):
    out_res = []
    for i in range(len(pre.times)):
       
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
        
        GRT = growth_rate_RT(nu, l, r, vz, u)
        wind_zero = growth_rate_RT(nu, l, r, vz, 0)
        reco_zero = growth_rate_RT(nu, l, 0, vz, u)
        reco_wind_zero = growth_rate_RT(nu, l, 0, vz, 0)
        LRT = growth_rate_RT(nu, l, 0, 0, 0)
        out_gammas = []
        out_res.append(out_gammas)
        
        for elem in [GRT, wind_zero, reco_zero, 
                     reco_wind_zero, LRT]:
            
        
            max_gamma = elem[(alts > 250) & (alts < 350)]
            #max_gamma = elem[alts == 300 ]
        
            out_gammas.append(np.max(max_gamma))
            
    df = pd.DataFrame(out_res, 
                      index = pre.times, 
                      columns = ["all", "nowind", 
                                 "noreco", "nowindReco", 
                                 "local"])

    df.to_csv("database/growthRates/gammas250_350km.txt", 
              sep = ",", 
              index = True)
infile = "database/PRE/FZ_PRE_2014_2015.txt"

pre = PRE(infile)
run_for_all_days(pre)
