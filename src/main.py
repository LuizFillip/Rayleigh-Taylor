import pandas as pd
import numpy as np 
from build import paths as p 
import os 
from AllSky.labeling import save_img
import datetime as dt

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
    

def save_timeseries_parameters(
        iri_infile = "D:\\ne\\2013\\",
        save_in = "D:\\plots\\"):
    
    
    files = os.listdir(iri_infile)
    
    for filename in files:
    
        date = dt.datetime.strptime(
            filename.replace(".txt", ""), "%Y%m%d"
            )
        
        dn = date + dt.timedelta(hours = 20)
        
        try:
            iri_file = os.path.join(iri_infile, filename)
            fig = plot_timeseries_parameters(
                    dn, iri_file)
            print("saving...", dn)
            fig_name = filename.replace(".txt", ".png")
            save_img(
                fig, 
                os.path.join(save_in, fig_name)
                     )
        except:
            continue