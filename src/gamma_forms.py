import ionosphere as io
import datetime as dt
import pandas as pd
import atmosphere as atm


df = pd.read_csv("perp_winds.txt", index_col = 0)
df.index = pd.to_datetime(df.index)





def compute_nu_like_timeseries():
    dn = dt.datetime(2013, 3, 17, 0)     
    glat, glon = sites["saa"]["coords"]   
    model = point_msis(dn, 300, glat, glon)
    
    temp = pd.read_csv("fp_temp.txt")
    temp.index = pd.to_datetime(temp.index)
    mag = mm.load_mag(freq = "5min")
    B = mag[mag.index == dn]["F"].item()
    
    nu = io.collision_frequencies()
    
    out = []
    
    for dn in temp.index:
        tn = temp[temp.index == dn]["avg"].item()
        df = point_msis(dn, 300, glat, glon)
        
        out.append(nu.ion_neutrals(
            tn, df["O"], 
            df["O2"], df["N2"]
            ))
        
        
    temp["nui"] = out
    
    temp.to_csv('nui_temp.txt')    