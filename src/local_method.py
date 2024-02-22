import base as b 
import aeronomy as ae 
import pandas as pd 
import datetime as dt



b.config_labels()

def pre_dataset():
    
    df = b.load('jic_freqs')
    df['time'] = df.index
    df.index = df.index.date - dt.timedelta(days = 1)

    df= df.loc[~df.index.duplicated()]
    
    return df.dropna()


def local_gamma():
    
    infile = 'models/temp/local_parameters.txt'

    df = b.load(infile)
    
    nu = ae.collision_frequencies()
    
    df["nui"] = nu.ion_neutrals(
        df["Tn"],
        df["O"], 
        df["O2"], 
        df["N2"]
        )
    
    df['ge'] = 9.81 / df['nui']
    
    df['gamma'] = df['ge'] * df['L'] * 1e3

    df = pd.concat([df, pre_dataset()], axis =1)
    
    df['gamma2'] = (df['vzp'] + df['ge']) * df['L'] * 1e3
    return df









        
# year = 2019

# df = b.sel_time(pre_dataset(), year, hour = 0)

# ds = b.load(f'jic{year}1').dropna()

# df['vp'].plot()

# ds['vp'].plot(ylim = [-2, 20])


df = pre_dataset()

df['vp'].plot()