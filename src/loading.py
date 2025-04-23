import base as b 
import os
import datetime as dt
import pandas as pd 
import digisonde as dg 
import matplotlib.pyplot as plt
import aeronomy as ae 

PATH_GAMMA = 'database/gamma/'
PATH_RESULT ='database/Results/concat/'


def get_gamma2():
    
    path = os.path.join(PATH_GAMMA, 'p1_saa.txt')
    
    df = b.load(path)
    
    df['gr'] = df['ge'] /df['nui']
    
    start = dt.datetime(2015, 12, 19)
    end = dt.datetime(2015, 12, 23)
    
    return b.sel_dates(df, start, end)


def get_drift():
    
    site = 'SAA0K'
    
    start = dt.datetime(2015, 12, 19)
    
    cols = list(range(3, 10, 1))
    
    df1 = dg.join_iono_days(
            site, 
            start,
            cols = cols, 
            smooth = 3
            )
    
    df1.rename(columns = {site: 'vz'}, 
               inplace = True)
    return df1.interpolate()

def get_models(alt):
    
    df = b.load(f'RayleighTaylor/src/models_{alt}')
    
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
    
    return df[['vr', 'gr', 'ON2']]

def get_scale(alt = 250):
    infile = 'digisonde/data/SAO/pro_profiles/SAA0K_20151219(353).TXT'
    df = dg.load_profilogram(infile)
    
    return df.loc[df['alt'] == alt][['L']]

def get_gamma(alt = 300):
    
    ds = pd.concat(
        [get_models(alt), 
        get_scale(alt), 
        get_drift()], axis = 1)
    
    
    ds['gamma'] =  ds['L'] * (ds['vz'] + ds['gr']) * 1e3
    ds['gamma2'] =  (ds['L'] * (ds['vz'] + ds['gr']) - ds['vr']) * 1e3
    

    return ds

fig, ax = plt.subplots(
    figsize = (14, 6), 
    dpi = 300
    )

ds = get_gamma()

ax.plot(ds['gamma'])
ax.plot(ds['gamma2'])

ax.set(
    xlim = [ds.index[0], ds.index[-1]],
    ylabel = '$\\gamma_{RT}~ (\\times 10^{-3} ~s^{-1})$'
    )

ax.axhline(0, lw = 1)
b.format_time_axes(
    ax, 
    hour_locator = 12, 
    translate = True, 
    pad = 85, 
    format_date = '%d/%m/%y'
    )