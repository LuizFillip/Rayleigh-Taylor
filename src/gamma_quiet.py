import datetime as dt 
import pandas as pd 
import core as c
import digisonde as dg 
import base as b
import aeronomy as ae 
import numpy as np 

def fl2dn(df, ref_date):
    
    df = df.copy()
    
    out = []
    for num in df.index:
        
        if num >= 24:
            num -= 24 
            days = 1
        else:
            days = 0
            
        out.append(
            ref_date + dt.timedelta(
                hours = num, 
                days = days
                )
            )
    df.index = out
    
    return df


def float_index_to_datetime(date):

    out = []
        
    for day in [19, 20, 21, 22]:
        ref_date = dt.datetime(2015, 12, day)
    
        out.append(fl2dn(date, ref_date))
            
        
    df = pd.concat(out)
    
    df = df.loc[~df.index.duplicated()]
    
    return df 



def get_models(site = 'FZA0M'):
    
    path = 'RayleighTaylor/data/'
    
    df = b.load(path + f'{site}_models_quiet')
    
    nu = ae.collision_frequencies()
    
    df["nui"] = nu.ion_neutrals(
        df["Tn"],
        df["O"], 
        df["O2"], 
        df["N2"]
        )
    
    df['vr'] = (5.15e-13 * df['N2']) + (1.2e-11 * df['O2'])
    
    df['gr'] = 9.8 / df['nui']
    
    df = df.loc[~df.index.duplicated()]
    
    return df #[['vr', 'gr', 'mer']]

def quiettime_models(site, cols = ['gr', 'vr']):
    
    df = get_models(site)
    
    df['time'] = b.time2float(
        df.index, sum_from = None)
    
    df['day'] = df.index.day
    
    out = []
    for par in cols:
    
        ds = pd.pivot_table(
            df, 
            values = par, 
            index = 'time', 
            columns = 'day'
            )
        out.append( ds.mean(axis = 1).to_frame(par))
        
    return pd.concat(out, axis = 1)


def quiettime_gamma(site = 'FZA0M'):
    
    datas = [
            c.quiettime_winds(),
            dg.quiettime_gradient_scale(site), 
            dg.quiettime_drift(site, cols = [5, 6, 7], window = None),
            quiettime_models(site, ['gr', 'vr']), 
            ]
    
    out = []
    for data in datas:
        out.append(float_index_to_datetime(data.dropna()))
        
    ds = pd.concat(out, axis = 1)
    
    ds = ds.replace(np.nan, 0)
    
    ds['wind'] =  (ds['L'] * (ds['vz'] - ds['mer'] + ds['gr']) - ds['vr'])* 1e3

    ds['no_wind'] =  (ds['L'] * (ds['vz']  + ds['gr']) - ds['vr'] ) * 1e3

    return ds 

