import ionosphere as io
import datetime as dt
import pandas as pd
import atmosphere as atm
import digisonde as dg
from models import altrange_models, altrange_msis
from GEO import sites
import FabryPerot as fp





def compute_parameters(dn, alt = 300):
    
    lat, lon = sites["saa"]["coords"]

    
    kwargs = dict(
         dn = dn, 
         glat = lat, 
         glon = lon,
         hmin = 200,
         hmax = 400
         )

    df = altrange_models(**kwargs)
    
    nu = io.collision_frequencies()
    
    nui = nu.ion_neutrals(
        df["Tn"], df["O"], 
        df["O2"], df["N2"]
        )
    
    ds = pd.DataFrame()
    
    ds["nui"] = nui
    ds["ne"] = df["ne"]
    ds["K"] = io.scale_gradient(ds["ne"])
    
    ds["R"] = atm.recombination2(df["O2"], df["N2"])
    
    ds = ds[ds.index == alt].reset_index()

    ds.index = [dn]
    
    return ds



def vertical_drift(
        drift_file = "database/Drift/SSA/PRO_2013.txt"
        ):

    drift = dg.load_drift(drift_file)
    return drift.resample("10min").asfreq().bfill()["vz"]


def join_hwm_fpi():

    wd = fp.load_FPI("database/FabryPerot/PRO/2013.txt")
    
    df = pd.read_csv("database/HWM/saa_250_2013.txt", index_col="time")
    df.index = pd.to_datetime(df.index)
    
    wd.drop_duplicates(inplace = True)
    wd = wd.reindex(df.index)
        
    filled_df = wd.copy()
    filled_df["zon"] = filled_df["zon"].fillna(df["zon"])
    filled_df["mer"] = filled_df["mer"].fillna(df["mer"])

    return filled_df

def gamma_parameters(ds, dn):
    wd = join_hwm_fpi()
    
    vp = vertical_drift("database/Drift/SSA/PRO_2013.txt")
    
    ds["U"] = wd[wd.index == dn]["zon"]
    
    ds["vz"] = vp[vp.index == dn]
    
    return ds





def timeseries_local(start, end):
    
    times = pd.date_range(start, end, freq = "10min")
    
    out = []
    
    for dn in times:
        ds = compute_parameters(dn, alt = 300)

        base = gamma_parameters(ds, dn)

        gamma = ((base["vz"] + base["U"] + 
                  (9.81/ base["nui"])) * base["K"])
        
        out.append(gamma)
        
    return pd.concat(out)


start = dt.datetime(2013, 1, 1, 20, 0) 
end = dt.datetime(2013, 1, 5, 0, 0)
#df = timeseries_local(start, end)



    

def compute_parameters2(ne, start):
    
    ds = ne.loc[ne.index == start
                ].set_index("alt").copy()
    
    nu = io.collision_frequencies()
    
    lat, lon = sites["saa"]["coords"]

    kwargs = dict(
         dn = start, 
         glat = lat, 
         glon = lon,
         hmin = 250,
         hmax = 350, 
         step = 50
         )

    
    msis = altrange_msis(**kwargs)


    ds["nui"] = nu.ion_neutrals(msis["Tn"], msis["O"], 
                          msis["O2"], msis["N2"]
                          ).to_frame("nui")
    
    ds["R"] = atm.recombination2(msis["O2"], msis["N2"])
    
    wd = join_hwm_fpi()
    
    ds["alt"] = ds.index
    ds.index = [start] * len(ds)
    
    ds["U"] = wd[wd.index == start]["zon"] 
    ds["V"] = wd[wd.index == start]["mer"] 
    
    vp = vertical_drift("database/Drift/SSA/PRO_2013.txt")
    ds["vz"] = vp[vp.index == start]
    
    return ds


def run_from_pyglow():

    ne = pd.read_csv("scale_plasma.txt", index_col = 0)
    ne.index = pd.to_datetime(ne.index)
    
    out = []
    
    for time in ne.index.unique():
    
        out.append(compute_parameters2(ne, time))
        
    
    df = pd.concat(out)
    
    df.to_csv("gamma_parameters.txt")
    return df


wd = join_hwm_fpi()
import matplotlib.pyplot as plt
import settings as s
from common import plot_terminators


fig, ax = plt.subplots(
    sharey = True, sharex = True,
    nrows = 2, dpi = 300, 
    figsize = (10, 8)
    )

ds = wd[wd.index < dt.datetime(2013, 1, 10)].copy()

ax[0].plot(ds["mer"])
ax[1].plot(ds["zon"])

ax[0].set(ylabel = "Vento meridional (m/s)")
ax[1].set(ylabel = "Vento zonal (m/s)")

s.format_time_axes(
        ax[1], 
        hour_locator = 12, 
        day_locator = 1, 
        tz = "UTC"
        )

for ax in ax.flat:
    plot_terminators(ax, ds)