import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
from RTIparameters import PRE, neutrals, scale_gradient
from common import loadNe, runMSISE

def growth_rate_RT(nu, L, R):
    """Local rate growth"""
    return (9.81 / nu) * L - R


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
    
infile = "database/PRE/FZ_PRE_2014_2015.txt"

pre = PRE(infile)
i = 0

vz = pre.pre[i]

out = []
times = pd.date_range("2014-01-01 00:00", 
                      "2014-01-01 23:50", 
                      freq = "10min")
for date in times:
    

    df = loadNe("20140101.txt").sel_time(date)
    
    hmin = df.index[0]
    hmax = df.index[-1]
    dat = runMSISE(date, hmin = hmin, 
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
    
    out.append(np.nanmax(gamma))
#%%
# Growth rate without winds and recombination
fig = plt.figure(figsize = (20, 5))
plt.plot(times, out)

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
        out_gammas = []
        out_res.append(out_gammas)
        
        for elem in [gamma, no_wind, no_r, 
                     no_r_wind, local]:
            
        
            max_gamma = elem[(alts > 200) & (alts < 400)]
        
        
            out_gammas.append(np.max(max_gamma))
            
    df = pd.DataFrame(out_res, 
                      index = pre.times, 
                      columns = ["all", "nowind", 
                                 "noreco", "nowindReco", 
                                 "local"])

    #df.to_csv("database/growthRates/gammas.txt", 
         # sep = ",", 
          #index = True)

    
