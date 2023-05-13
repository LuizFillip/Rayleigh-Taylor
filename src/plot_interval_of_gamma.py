import pandas as pd
from results import plot_roti_maximus
import matplotlib.pyplot as plt
import datetime as dt
import settings as s
import astral 
from astral.sun import sun

fig, ax = plt.subplots(
    sharey = True,
    dpi = 300)


infile = "database/Results/maximus/2013.txt"
dn = dt.datetime(2013, 11, 1, 20)
plot_roti_maximus(
    ax, infile, 
    start = dn, 
    delta_hours = 4
    )

s.format_axes_date(
     ax, time_scale = "hour", interval = 1
     )


lat = -2.53
lon = -44.296 
twilightAngle = 18


observer = astral.Observer(latitude = lat, longitude = lon)
out = []
alts = [0, 125, 300]
for i, angle in enumerate([0, 12, 18]):
    phase = sun(observer, dn, dawn_dusk_depression = angle)
    ax.axvline(phase["dusk"])
    if angle == 12:
        minutes = 20
    else:
        minutes = 10
    ax.text(phase["dusk"] - dt.timedelta(minutes = minutes), 
            5.1, f"{alts[i]} km",
            transform = ax.transData
            )
    
ax.legend(["1 TEC/min", "Pôr do Sol"])
# plt.fill_between(x, y3, y4, color='grey', alpha='0.5')
