import pandas as pd
from base import sel_times, load
from GEO import sun_terminator
import RayleighTaylor as rt
from tqdm import tqdm 
import FluxTube as ft


path_drift = 'digisonde/data/drift/PRE/saa/'
path_fluxt =  'FluxTube/data/reduced/saa/'


def PRE(year, alt = 300):

    ds = load(path_drift + f'R{year}.txt')
    
    ds.rename(
        columns  = {'vzp':'vp'}, inplace = True)

    ds['vp'] = ds['vp'] * ft.factor_height(alt)**3

    return ds

def FluxTube_dataset(year, dn):
    
    ds = load(path_fluxt + f'{year}.txt')
    
    try:
        joined = ds.join(PRE(year, alt = 300))
    except:
        joined = ds.copy()
    
    return sel_times(joined, dn)

    
def get_maximus(
        ds, 
        dn, 
        sun_center = 'dusk'
        ):
    
    """
    Getting gamma maximus between region E and F 
    terminators or region F :
    Parameters:
        
    """
    
    D = sun_terminator(dn, twilight_angle = 0)
    E = sun_terminator(dn, twilight_angle = 12)
    F = sun_terminator(dn, twilight_angle = 18)
    
    if sun_center == 'dusk':
        filtered = ds.loc[
            (ds.index >= D) & 
            (ds.index <= F)
            ]
    elif sun_center == 'night':
        
        filtered = ds.copy()
        
    else:
        filtered = ds.loc[
            (ds.index >= E) & 
            (ds.index <= F)
            ]
    
    return filtered.max().to_frame(dn.date()).T


    
def maximus_dialy(
        year = 2013,
        sun_center = 'dusk'
        ):
    
    """Get gamma maximus for whole year, 
    try for local and integrated quantities
    """
    
    dates = pd.date_range(
        f'{year}-01-01 20:00', 
        f'{year + 1}-01-01 20:00', 
        freq = '1D'
        )
    
    out = []
    for dn in tqdm(dates, desc = str(year)):
        
        ds = rt.gammas_integrated(
            FluxTube_dataset(year, dn)
            )
        
        out.append(
            get_maximus(ds, dn, 
                    sun_center = sun_center
            )
        )
        
    return pd.concat(out)



def run_years():
    
    out = []
    
    for year in range(2013, 2023):
                
        out.append(
            maximus_dialy(
                year = year,
                sun_center = 'dusk'
                )
            )
            
    
    return pd.concat(out)
    


def main():
    year = 2020
    
    
    ds =  run_years()
    
    ds.to_csv('database/Results/gamma/saa.txt')

# ds = load(path_drift + f'R{year}.txt')
# ds = load(path_fluxt + f'{year}.txt')
# ds['zon'].plot()