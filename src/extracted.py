import os
import ionosphere as io
import datetime as dt
import pandas as pd
import atmosphere as atm


infile = "D:\\ne\\2013\\"

files = os.listdir(infile)

filename = files[0]

ds = pd.read_csv(infile + filename, index_col = 0)

times  = ds.index.unique()
out = []

for time in times:
    df = ds[ds.index == time]
    df["L"] = io.scale_gradient(df["Ne"]).copy()
    for alt in [250, 300, 350]:
        out.append(df.loc[df["alt"] == alt])

ts = pd.concat(out)

print(ts)