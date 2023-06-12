import matplotlib.pyplot as plt
from common import plot_roti, plot_terminators, load_by_alt_time
import RayleighTaylor as rt
import pandas as pd
import datetime as dt
import settings as s
import os

infile = "database/RayleighTaylor/parameters_car.txt"
dn = dt.datetime(2013, 3, 16, 20)
alt = 300
df = load_by_alt_time(infile, alt, dn)


fig, ax = plt.subplots()
vzp = 30

for wind in [0, 50, 100]:
    gamma = df["L"] * (vzp - wind + (9.81 / df["nui"]) )  - df["R"]
     
    ax.plot(gamma *1e4, label = f"{wind} m/s")
    
    ax.legend()