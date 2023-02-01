import datetime
import pandas as pd
#import matplotlib.pyplot as plt
import numpy as np 
from RTIparameters import PRE, neutrals, scale_gradient
from common import loadNe, runMSISE, growth_rate_RT
#import os
from tqdm import tqdm


def run_for_all_times(vz, 
                      date, 
                      neInfile):
    """Running for all electron density (range 200 to 500 km)
    in whole day for each 10 minutes"""

    end =  date + datetime.timedelta(hours = 23, minutes = 50)
    
    times = pd.date_range(date,  end, freq = "10min")
    
    out = {"g300_reco": [], 
           "g300_Vp": [], 
           "gVp_max": [], 
           "gR_max": []}
    
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
        
        # Without winds effects 
        gammaR = growth_rate_RT(nu, l, r, vz, 0)
        # Without Recombination and winds effects
        gammaVp = growth_rate_RT(nu, l, 0, vz, 0)
        
        # Get from range altitude
        gVp_max = np.nanmax(gammaVp[(alts > 250) & (alts < 350)])
        gR_max = np.nanmax(gammaR[(alts > 250) & (alts < 350)])
        
        # Get from fixed altitude
        gamma300R = gammaR[alts == 300]
        gamma300Vp = gammaVp[alts == 300]
        
        out["g300_reco"].append(gamma300R[0])
        out["g300_Vp"].append(gamma300Vp[0])
        out["gVp_max"].append(gVp_max)
        out["gR_max"].append(gR_max)
        
    return pd.DataFrame(out, index = times)





def run_for_all_days2(preInfile, densityInfile):
    gammas = []
    
    pre = PRE(preInfile).df
    
    for num in tqdm(pre.index):
        
        try:
            
            filename = num.strftime("%Y%m%d") + ".txt"
            
            vz = pre.loc[num, "vz"]
            
            date = pd.to_datetime(num.date())
            gammas.append(run_for_all_times(vz, date, 
                                            densityInfile + filename))
    
        except:
            continue
        
    return pd.concat(gammas)

def main():
    preInfile = "database/PRE/FZ_PRE_2014_2015.txt"
    densityInfile = "D:\\ne\\"
    
    df = run_for_all_days2(preInfile, densityInfile)
    
    
    df.to_csv("database/growthRates/reco_and_vp_alltimes2.txt",
              sep = ",", index = True)
