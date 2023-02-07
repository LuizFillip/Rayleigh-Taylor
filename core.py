import pandas as pd
import numpy as np
import datetime as dt
from common import get_wind, get_pre, runMSISE
from base.neutral import eff_wind, recombination, nui_1


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


date_time = dt.datetime(2014, 1, 1, 21, 20)

w = get_wind(date_time.date())

vzp = get_pre(date_time.date())

u = eff_wind(w.zon, w.mer)
n = runMSISE(date_time)
R = recombination(n.O2, n.N2)

nu = nui_1(n.Tn, n.O, n.O2, n.N2)


print(nu)
    


class loadNe(object):
    
    def __init__(self, filename):
        df = pd.read_csv(filename, index_col = 0)
        
        df["date"] = pd.to_datetime(df["date"])
        
        self.times = np.unique(df.date)
        self.df  = df
      
    @property
    def pivot(self):
        self.df["alts"] = self.df.index
        return pd.pivot_table(self.df, 
                              columns = "date", 
                              index = "alts", 
                              values = "Ne")
    
    def sel_time(self, date):
        return self.df.loc[self.df["date"] == date, "Ne"]
                              



