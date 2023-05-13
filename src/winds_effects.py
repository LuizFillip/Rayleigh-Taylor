import FluxTube as ft
import ionosphere as io
import matplotlib.pyplot as plt
import pandas as pd
from models import altrange_msis
from GEO import sites


infile = "database/HWM/profiles.txt"

df = pd.read_csv(infile, index_col= 0)
df["dn"] = pd.to_datetime(df["dn"])

dates = df["dn"].unique()

dn = dates[0]
df = df.loc[df["dn"] == dn, ["zon"]]

plt.plot(df, df.index)

glat, glon = sites["saa"]["coords"]

nu = io.collision_frequencies()

msis = altrange_msis(
    pd.to_datetime(dn), glat, glon, 
    hmin = df.index[0], 
    hmax = df.index[-1]
    )

nui = nu.ion_neutrals(
    msis["Tn"], msis["O"], 
    msis["O2"], msis["N2"]
    )

omega = io.conductivity().ion_cyclotron

plt.plot((nui / omega) * df["zon"], nui.index)

res = (nui / omega) * df["zon"]

res[res.index == 300]