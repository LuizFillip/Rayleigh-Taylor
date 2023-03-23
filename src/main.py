import pandas as pd
import numpy as np 
from build import paths as p 
from RayleighTaylor.core import df_parameters



def get_max(df, date, alts = (250, 350)):
   
    cond_alt = ((df.index >= alts[0]) &
                (df.index <= alts[1]))
    
    cond_time = (df["date"] == date)
    
    return df.loc[cond_alt & cond_time, "g"].max()


def run(df):
    infile = p('RayleighTaylor').files

    df = pd.read_csv(infile, index_col = 0)
    dates = np.unique(df.date)
    
    out = []
    for date in dates:
        out.append(get_max(df, date))
        
    return (pd.to_datetime(dates), 
            np.array(out, dtype = np.float64))
    

