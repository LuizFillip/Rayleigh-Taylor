import matplotlib.pyplot as plt
from common import plot_roti, plot_terminators
import RayleighTaylor as rt
from utils import save_img
import pandas as pd
import datetime as dt

def plot_local_timeseries(df, alt = 250, station = "salu"):
        
    fig, ax = plt.subplots(
                figsize = (8, 10),
                sharex = True,
                nrows = 4,
                dpi = 300
                )

    plt.subplots_adjust(hspace = 0.3)
    
    eq = rt.EquationsRT()
    
    eqs = [eq.gravity(), eq.drift(), eq.complete()]
    
    for num, title in enumerate(eqs):
        
        ax[num].set(title = title, 
                    ylim = [-10, 45],
                    ylabel = eq.label)
    
    
    ax[0].text(0.9, 1.1, f"{alt} km", transform = ax[0].transAxes)
    gamma = (9.81 / df["nui"]) * df["L"] 
    ax[0].plot(gamma *1e4)
    
    gamma = (df["vz"] + (9.81 / df["nui"])) * df["L"] 
    ax[1].plot(gamma *1e4)
        
    gamma = (df["vz"] + df["U"] + (9.81 / df["nui"])) * df["L"] 
    ax[2].plot(gamma *1e4)
    
    plot_roti(ax[3], df, hour_locator = 1, station = station)
    
    for ax in ax.flat:
        plot_terminators(ax, df)
    return fig

# dn = dt.datetime(2013, 9, 19, 20)
alt = 250
times =  pd.date_range(dt.datetime(2013, 9, 17, 20), 
                        dt.datetime(2013, 9, 28, 20), freq = "1D")


#dn = dt.datetime(2013, 9, 20, 20)
save_in = "D:\\plots2\\Local\\"
for dn in times:
    
    df = pd.read_csv("gamma_parameters.txt", index_col = 0)
    df.index = pd.to_datetime(df.index)
    
    
    
    df = df.loc[(df["alt"] == alt) & 
                (df.index >= dn) &
                (df.index <= dn + dt.timedelta(seconds = 43200))]
    fig = plot_local_timeseries(df, alt = alt, station = "ceeu")
    
    FigureName = dn.strftime("%Y%m%d.png")
    print("saving...", dn)
    save_img(fig, save_in + FigureName)
    

#%%%

dt.datetime(2013, 9 , 24).timetuple().tm_yday