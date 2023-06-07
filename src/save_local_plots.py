import datetime as dt
import pandas as pd
import RayleighTaylor as rt
from utils import  save_but_not_show

def save_plots():

    save_in = "RayleighTaylor/figures/"
    
    for dn in [dt.datetime(2013, 3, 16, 20), 
               dt.datetime(2013, 3, 17, 20), 
               dt.datetime(2013, 3, 18, 20)]:
        
        for sign in [1, -1]:
            
            for site in ["car", "caj"]:
                infile = f"database/RayleighTaylor/parameters_{site}.txt"
                
                fig = rt.plot_local_winds_effects(
                    infile, dn, sign = sign)
                
                if "car" in infile:
                    fig.suptitle("Ventos observados em Cariri", y = 1.)
                else:
                    fig.suptitle("Ventos observados em Cajazeiras", y = 1.)
                
                if sign == 1:
                    s = "positive"
                else:
                    s = "negative"
                    
                FigureName = f"{dn.strftime('%Y%m%d')}_{s}_{site}.png"
                
                print("saving...", dn)
                
                save_but_not_show(
                       fig, 
                       save_in + FigureName,
                       dpi = 300
                       )
                
save_plots()