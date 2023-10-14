import base as b
import datetime as dt
import os
import FluxTube as ft

PATH_PRE = 'digisonde/data/PRE/'
PATH_FLUXTUBE =  'FluxTube/data/reduced/'

def PRE(year, site = 'saa', alt = 300):
    
    infile = os.path.join(
        PATH_PRE,
        site,
        f'R{year}.txt'
        )

    ds = b.load(infile)
    
    ds.rename(
        columns  = {'vzp': 'vp'}, 
        inplace = True
        )

    ds['vp'] = ds['vp'] * ft.factor_height(alt)**3

    return ds

def FluxTube_dataset(
        dn, 
        site = 'saa'
        ):
    
    infile = os.path.join(
        PATH_FLUXTUBE,
        site, 
        f'{dn.year}.txt'
        )
    ds = b.load(infile)
    
    try:
        joined = ds.join(PRE(dn.year))
    except:
        joined = ds.copy()
    
    return b.sel_times(joined, dn)


import datetime as dt 

dn = dt.datetime(2013, 1, 1, 21)
ds = FluxTube_dataset(dn, site = 'jic')
    
    
# df = rt.gammas_integrated(ds)


# ds['K'].plot()

ds.columns