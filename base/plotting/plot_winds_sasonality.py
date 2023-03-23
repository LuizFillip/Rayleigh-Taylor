import datetime as dt
import matplotlib.pyplot as plt
from RayleighTaylor.src.common import load
import setup as s
from RayleighTaylor.base.winds import effective_wind
from GEO.core import run_igrf

def plot_winds_sasonality():

    ts = load()
    
    infile = "database/HWM/HWM14/SAA3002013.txt"
    
    times = [dt.time(21, 0), dt.time(0, 0), dt.time(3, 0)]
    
    df = ts.HWM(infile)
    
    d, i = run_igrf(2013, site = "saa", alt = 300)
    
    fig, ax = plt.subplots(
        nrows = 3, 
        sharex = True, 
        figsize = (10, 8)
        )
    
    for n, ax in enumerate(ax.flat):
    
        df1 = df.loc[df.index.time == times[n]]
        
        ax.plot(df1["mer"], label = "meridional")
        ax.plot(df1["zon"], label = "zonal")
        
        wind = effective_wind()
        
        ax.plot(wind.eff_meridional(
            df1["zon"], df1["mer"], d, i),
            label = "Efetivo meridional")
        
        ax.plot(wind.eff_zonal(
            df1["zon"], df1["mer"], d),
            label = "Efetivo zonal")
        
        ax.text(0.01, 1.05,
                f"{times[n]} (UT)", 
                transform = ax.transAxes)
        ax.set(ylabel = "Velocidade (m/s)")
        
        if n == 0:
            ax.legend(
                bbox_to_anchor=[0.5, 1.3], 
                loc = "center",  
                ncol = 4
                )