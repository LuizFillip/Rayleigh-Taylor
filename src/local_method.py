import base as b 
import aeronomy as ae 
import pandas as pd 
import datetime as dt
import digisonde as dg 


def input_specific_time(ss):
    if ((ss.date() < dt.date(year, 4, 1)) | 
        (ss.date() > dt.date(year, 10, 1))):
        
        time = dt.time(1, 0)
    else:
        time = dt.time(0, 0)
        
    return time


def sel_times(df, year):
    time = dt.time(1, 0)
    ss = dt.datetime(year, 1, 1, 3)
    ee = dt.datetime(year + 1, 1, 1, 3)
    dates = pd.date_range(ss, ee, freq = '1D')
    
    out = {'gamma': [], 'L': [], 'ge': []}
    
    for i in range(len(dates) - 1):
    
        ss = dates[i]
        ds = df.loc[(df.index > ss) & 
                    (df.index <= dates[i + 1]) ]
        
        
        for col in ['gamma', 'L', 'ge']:
            sel = ds.loc[ds.index.time == time]
            out[col].append(sel[col].max())
    
    index = pd.to_datetime(dates[:-1].date)
    
    return pd.DataFrame(out, index = index)
def parameters(year, time):
    infile = f'models/temp/local_{year}'
    df = b.load(infile)
        
    nu = ae.collision_frequencies()
    
    df["nui"] = nu.ion_neutrals(
        df["Tn"],
        df["O"], 
        df["O2"], 
        df["N2"]
        )
    
    df['ge'] = 9.81 / df['nui']
    
    df = df.drop(columns = [
        'He', 'O', 'N2', 'foF2',
        'O2', 'H', 'N', 'Tn',
        'Tn.1', 'Ti', 'Te', 'L'])
    time = dt.time(1, 0)
    ds = df.loc[df.index.time == time]
    
    ds.index = ds.index.date
    return ds

def gradient(year, time, smooth = False):
    
    infile = f'digisonde/data/jic/profiles/{year}'
    
    df = dg.load_profilogram(infile)

    ds = df.loc[(df['alt'] == 300) & 
                (df.index.time == time)]
    
    if smooth:
        ds['L'] = b.smooth(ds['L'], 10).copy()
        
    ds = ds.drop(columns = ['alt', 'freq'])
    
    ds.index = ds.index.date

    return ds

def PRE(year):
    df = b.load('jic_freqs2')
    df = df.loc[df.index.year == year]
    df.index = pd.to_datetime(df['time']).dt.date
    df = df.loc[~df.index.duplicated()]
    return df


year = 2019


time = dt.time(1, 0)
df = pd.concat([PRE(year), 
                gradient(year, time), 
                parameters(year, time)], axis = 1)



df['gamma'] = (df['ge'] * df['L']) * 1e3
df['gamma2'] = ((df['vp'] + df['ge']) * df['L']) * 1e3

df['L'] = df['L'] * 1e5


df['gamma2'].plot(ylim = [0, 3])