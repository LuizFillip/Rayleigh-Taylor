import base as b 
import aeronomy as ae 
import pandas as pd 
import datetime as dt
import digisonde as dg 
import GEO as gg
import pyIGRF 


def dec_dip(
        df, 
        site = "jic", alt = 300
        ):
    
    lat, lon = gg.sites[site]["coords"]
        
    for idx, row in df.iterrows():
        year = idx.year
        
        d, i, h, x, y, z, f = pyIGRF.igrf_value(
            lat, lon, alt=alt, year=year)
        
        # Assign the calculated values to new columns
        df.loc[idx, 'D'] = d
        df.loc[idx, 'I'] = i

    return df 


def winds(year, time = dt.time(1, 0)):
    
    infile = 'database/HWM/winds_jic'
    
    df = b.load(infile)
    df = df.loc[(df.index.time == time) &
                ( df.index.year == year)]
    wind = ae.effective_wind()
    
    df = dec_dip(df)
    df['UL'] = wind.meridional_perp(
        df['zon'], df['mer'], df['D'], df['I'])
    df.index = pd.to_datetime(df.index.date)
    return df 
    



def parameters(year, time = dt.time(1, 0)):
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
        'Tn.1', 'Ti', 'Te'])
    
    df = df.rename(columns = {'L': 'L1'})

    ds = df.loc[df.index.time == time]
    
    ds.index = ds.index.date
    return ds

def gradient(year, time, smooth = False):
    
    infile = f'digisonde/data/jic/profiles/{year}'
    
    df = dg.load_profilogram(infile)
        
    ds = df.loc[(df['alt'] == 300) & 
                (df.index.time == time)]
    
    ds = ds.drop(columns = ['alt', 'freq'])
    
    ds.index = ds.index.date
    ds = ds.loc[~ds.index.duplicated()]
    return ds

def vertical_drift(year):
    df = b.load('database/jic_freqs2')
    df = df.loc[df.index.year == year]
    df.index = pd.to_datetime(df['time']).dt.date
    df = df.loc[~df.index.duplicated()]
    df = df.loc[~(df['vp'] > 40)]
    return df


def another_pre(year):
    path = 'digisonde/data/PRE/jic/2013_2021.txt'
    ds = b.load(path)
    ds = ds.loc[ds.index.year == year]
    ds = ds.loc[~(ds['vz']> 100)]




def local_results(
        year, 
        col_grad = 'L1', 
        time = dt.time(0, 0)
        ):

    df = pd.concat(
        [vertical_drift(year), winds(year, time), 
        parameters(year, time)
        ], axis = 1)
   
    df['gamma'] = ((df['vp'] + df['ge']) * df[col_grad]) * 1e3
        
    df.index = pd.to_datetime(df.index)
    
    df['doy'] = df.index.day_of_year
    return df.dropna()

def concat_results():
    
    out = []
    for year in range(2013, 2022):
        
        out.append(
            local_results(
                year, 
                col_grad = 'L1', 
                time = dt.time(1, 0)
                )
        )
            
    df = pd.concat(out)

    df.to_csv('database/jic_local')
    


