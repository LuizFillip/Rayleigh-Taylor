# -*- coding: utf-8 -*-
"""
Created on Sun May  7 13:14:11 2023

@author: Luiz
"""

import ionosphere as io
from GEO import load_meridian
import datetime as dt
import matplotlib.pyplot as plt
dn = dt.datetime(2013, 1, 1, 21, 0) 

mlon, mlat, _, _, = load_meridian() 


kwargs = dict(
     dn = dt.datetime(2013, 1, 1, 21), 
     glat = mlat, 
     glon = mlon,
     hmin = 150 
     )
 

base = io.test_data(**kwargs)


g = 9.81

gamma = (g / base["nui"]) * io.scale_gradient(base["ne"])

fig, ax = plt.subplots(dpi = 300)

ax.plot(gamma, base.index)

lim = 1e-3
ax.axvline(0, linestyle = "--")

ax.set(xlim = [-lim, lim])
