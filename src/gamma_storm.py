import base as b 
import datetime as dt
import pandas as pd 
import digisonde as dg 
import aeronomy as ae 
import FabryPerot as fp 
import numpy as np 
PATH_GAMMA = 'database/gamma/'
PATH_RESULT ='database/Results/concat/'


def get_drift(site = 'SAA0K'):
      
    start = dt.datetime(2015, 12, 19)
    
    cols = [5, 6, 7]
    
    df = dg.join_iono_days(
            site, 
            start,
            cols = cols
            )
            
    # idx = df.index.indexer_between_time(
    #     '00:00', '20:00', include_end=False)

    # df.iloc[idx] = df.iloc[idx].apply(lambda s: b.smooth2(s, 5))
    
    return df.interpolate().rename(columns = {site:'vz'})

def get_models(
        site = 'SAA0K', 
        cols = ['vr', 'gr']
        ):
    
    path = 'RayleighTaylor/data/'
    
    df = b.load(path + f'{site}_models_storm')
    
    nu = ae.collision_frequencies()
    
    df["nui"] = nu.ion_neutrals(
        df["Tn"],
        df["O"], 
        df["O2"], 
        df["N2"]
        )
    
    df['vr'] = (5.15e-13 * df['N2']) + (1.2e-11 * df['O2'])
    
    df['gr'] = 9.8 / df['nui']
    
    df['ON2'] = df['O'] / df['N2']
    
    return df[cols]



def get_winds():
    
    days = [19, 20, 21, 22]
    out = []
    path =  'database/FabryPerot/car/'
    
    for day in days:
        fn = f'minime01_car_201512{day}.cedar.003.txt'
        df = fp.process_directions(
                path + fn, 
                freq = "10min", 
                parameter = "vnu"
                )
        
        out.append(df)
        
    return pd.concat(out)

def get_scale(site, alt = 250):
    

    df = dg.storm_profiles(site = site)
    
    df = df.loc[df['alt'] == alt]
    
    df = df.loc[~df.index.duplicated(keep='first')]
    
    return df

def concat_by_map(ds, md):
    for col in md.columns:
        ds[col] = ds.index.map(md[col])
        
    return ds 

def stormtime_gamma(site):
    
    ds = get_drift(site)
    
    frames = [get_scale(site), get_models(site), get_winds() ]
    
    for frame in frames:
        ds = concat_by_map(ds, frame)
    
    ds = ds.replace(np.nan, 0)
    
    ds['wind'] =  (ds['L'] * (ds['vz'] - ds['mer'] + ds['gr']) - ds['vr']) * 1e3
    
    ds['no_wind'] =  (ds['L'] * (ds['vz'] + ds['gr']) - ds['vr']) * 1e3
     
    t0  = pd.Timestamp('2015-12-20 20:40')   
    t1 = pd.Timestamp('2015-12-20 21:20')
    ds.loc[(ds.index > t0) & (ds.index < t1), ['wind']  ] /= 4
    return ds 