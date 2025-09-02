import base as b 
import GEO as gg 
import datetime as dt
import pandas as pd 
import digisonde as dg 
import matplotlib.pyplot as plt
import aeronomy as ae 
import core as c
import FabryPerot as fp 
import numpy as np 
PATH_GAMMA = 'database/gamma/'
PATH_RESULT ='database/Results/concat/'


def get_drift(site = 'SAA0K'):
      
    start = dt.datetime(2015, 12, 19)
    
    cols = [5, 6]
    
    df1 = dg.join_iono_days(
            site, 
            start,
            cols = cols
            )
    
    df1.rename(
        columns = {site: 'vz'}, 
        inplace = True
        )
    
    df1 = df1.loc[~df1.index.duplicated(keep='first')]
    
    return df1.interpolate()

def get_models(site = 'SAA0K', 
               cols = ['vr', 'gr']):
    
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
    path =   'database/FabryPerot/car/'
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
    
    return df['L']


def get_gamma(site):
 

    ds = pd.concat(
          [get_drift(site), 
          get_scale(site), 
          get_models(site, cols = ['vr', 'gr', 'mer']), 
          # get_winds()
          ], axis = 1)
  

    ds = ds.replace(np.nan, 0)
    
    # ds['vr'] = 0
    
    ds['gamma'] =  (ds['L'] * (
        ds['vz'] - ds['mer'] + ds['gr']) - ds['vr']) * 1e3
    
    ds['gamma3'] =  (ds['L'] * (
        ds['vz'] + ds['gr']) - ds['vr']) * 1e3
    
    ds1 = c.quiettimeRTI()
    
    # ds1['vr'] = 0
    ds['gamma2'] =  (ds1['L'] * (
        ds1['vz'] - ds1['mer'] + ds1['gr']) - ds1['vr'])* 1e3
    
    ds['gamma4'] =  (ds1['L'] * (
        ds1['vz']  + ds1['gr']) - ds1['vr'] ) * 1e3
    
    ds = ds.resample('10min').mean()
    
    dn = dt.datetime(2015, 12, 21)
    
    delta = dt.timedelta(hours = 12)
    
    end = dn + delta
    
    ds.loc[dn: end] = ds.loc[dn: end].rolling(
        window = 5, 
        center = True
        ).mean()
    
  
    return ds.interpolate()

def plot_shade_around_terminator(ax, dn, site):
    
    
    dusk = gg.dusk_from_site(
            dn, 
            site[:3].lower(),
            twilight_angle = 18
            )
    
    ax.axvline(dusk, lw = 2, linestyle = '--')
    
    delta = dt.timedelta(minutes = 30)
    
    ax.axvspan(
         dn - delta, 
         dn + delta, 
         ymin = 0, 
         ymax = 1,
         alpha = 0.2, 
         color = 'red'
     )
    return None 
def plot_gamma_quiet_and_storm(ax, ds, gs, lim = 2, site = 'saa'):
        
    ax.plot(
        ds[gs[0]], 
        label = 'Storm-time', 
        lw = 2
        )
    ax.plot(
        ds[gs[1]], 
        label = 'Quiet-time', 
        lw = 2, 
        linestyle = '--'
        )
    
    ax.set(
        ylim = [-lim, lim],
        xlim = [ds.index[0], ds.index[-1]],
        ylabel = '$\\gamma_{RT}~ (\\times 10^{-3} ~s^{-1})$'
        )
    
    ax.axhline(0, lw = 0.5)
    
    dn = dt.datetime(2015, 12, 20, 21, 40)
    
    plot_shade_around_terminator(ax, dn, site)
    

    return None 

def plot_winds_effects_on_gamma(site = 'FZA0M'):
    
    fig, ax = plt.subplots(
        figsize = (16, 12), 
        dpi = 300, 
        nrows = 2, 
        sharex = True
        )
    
    plt.subplots_adjust(hspace = 0.05)
    ds = get_gamma(site)
        
    dn = dt.datetime(2015, 12, 20, 12)
    ds = b.sel_times(ds, dn, hours = 24)
    
    plot_gamma_quiet_and_storm(ax[0], ds, gs = ['gamma', 'gamma2'], site = site)
    plot_gamma_quiet_and_storm(ax[1], ds, gs = ['gamma3', 'gamma4'], site = site)
    
    b.format_time_axes(
         ax[-1], 
         hour_locator = 2, 
         translate = True, 
         pad = 85, 
         format_date = '%d/%m/%y'
         )
    
       
    ax[0].legend(
        ncol = 2, 
        loc = 'upper center', 
        bbox_to_anchor = (0.5, 1.2), 
    
        )
     
    ax[0].text(
        0.01, 0.85, 
        '(a) With meridional winds', 
        transform = ax[0].transAxes
        )
    
    ax[1].text(
        0.01, 0.85, 
        '(b) Without meridional winds', 
        transform = ax[1].transAxes
        )
    
    return fig 
    
def main():
    
    site = 'FZA0M'
    site = 'SAA0K'
    fig = plot_winds_effects_on_gamma(site)
    
    
    FigureName = 'winds_effects_on_gamma'
    
    path_to_save = 'G:\\My Drive\\Papers\\Paper 2\\Geomagnetic control on EPBs\\June-2024-latex-templates\\'
    
    
    # fig.savefig(path_to_save + FigureName, dpi = 400)



# main()