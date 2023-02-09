import pandas as pd
import numpy as np 
from core import growth_rate_RT
from common import get_wind, get_pre, get_ne, run_msise, pre_times
from base.neutral import recombination, nui_1
from base.iono import scale_gradient

    
    
    

def make_df(date_time, func_wind = "U1"):


    u = get_wind(date_time, func_wind =
                 func_wind).U.values
    
    n = run_msise(date_time, 
                  hmin = 200, hmax = 500)
    
    r  = recombination(n.O2, n.N2).values
    
    nu = nui_1(n.Tn, n.O, n.O2, n.N2).values
    
    ne = get_ne(date_time, 
                hmin = 200, hmax = 500)
    
    vzp = np.array([get_pre(date_time.date())] * len(n))
    
    l = scale_gradient(ne, dz = 1)
    
    g = growth_rate_RT(nu, l, r, vzp, u)
  
    arr = np.vstack([u, r, nu, l, vzp, g, n.index]).T
    
    return pd.DataFrame(arr, columns = ["u", "r", "nu", 
                                       "l", "vz", "g", "alt"],
                      index = [date_time] * len(n))

def process_all_year(func_wind = "U1", 
                     save = True):
    
    out = []
    
    for date_time in pre_times():
        print(func_wind, "...", date_time)
        try:
            out.append(make_df(date_time, 
                           func_wind = func_wind))
        except:
            continue
    
    df = pd.concat(out)
    
    if save:
        df.to_csv(f"database/data/2014_{func_wind}.txt", 
                  sep = ",", 
                  index = True)
    return df

def main():
    
    for func_wind in ["U1", "U2", "U3"]:

        df = process_all_year(func_wind)
    
main()



