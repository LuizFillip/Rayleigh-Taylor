import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.dates as dates


infile = "database/density/"
_, _, files = next(os.walk(infile))


filename = files[30]


df = pd.read_csv(infile + filename, 
                 index_col = 0)
df["date"] = pd.to_datetime(df["date"])
df["alts"] = df.index

df1 = pd.pivot_table(df, 
                     columns = "date", 
                     index = "alts", 
                     values = "Ne")


fig, ax = plt.subplots(figsize = (30, 12))

plt.contourf(df1.columns, 
             df1.index, 
             df1.values, 50, 
             cmap = "rainbow")


ax.xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
ax.xaxis.set_major_locator(dates.HourLocator(interval = 2))


ax.set(ylabel = "Altitude (km)", 
       xlabel = "Time (UT)")