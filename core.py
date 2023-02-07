import datetime as dt
from common import get_wind, get_pre, get_ne, run_msise, pre_times
from base.neutral import recombination, nui_1
from base.iono import scale_gradient
import pandas as pd
import numpy as np


def growth_rate_RT(nu, L, R, Vp, U):
    """
    Generalized instability rate growth
    local version
    Paramaters:
    ---------- 
    Vp: Prereversal Enhancement (PRE)
    U: Neutral wind (effective)
    nu: ion-neutral collisional frequency
    L: electron density gradient scale
    R: Recombination rate
    g: acceleration due gravity
    """
     
    return (Vp - U + (9.81 / nu))*L - R



def make_df(date_time, func_wind = "Nogueira"):


    u = get_wind(date_time, func_wind = func_wind).U.values
    
    n = run_msise(date_time, 
                  hmin = 200, hmax = 500)
    
    r  = recombination(n.O2, n.N2).values
    
    nu = nui_1(n.Tn, n.O, n.O2, n.N2).values
    
    ne = get_ne(date_time, 
                hmin = 200, hmax = 500)
    
    vzp = np.array([get_pre(date_time.date())] * len(n))
    
    l = scale_gradient(ne, dz = 1)
  
    arr = np.vstack([u, r, nu, l, vzp,  n.index]).T
    
    return pd.DataFrame(arr, columns = ["u", "r", "nu", 
                                      "l", "vz", "alt"],
                      index = [date_time] * len(n))

def process_all_year(save = True):
    out = []
    for date_time in pre_times():
        out.append(make_df(date_time, 
                           func_wind = "Nogueira"))
    df = pd.concat(out)
    
    if save:
        df.to_csv("database/data/2014_U1_.txt", 
                  sep = ",", index = True)
    return df


df = process_all_year()