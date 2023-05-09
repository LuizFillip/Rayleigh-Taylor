import ionosphere as io
from GEO import load_meridian
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

dn = dt.datetime(2013, 1, 1, 21, 0) 

mlon, mlat, _, _, = load_meridian() 





def timeseries_local(start, end, alt):
    
    times = pd.date_range(start, end, freq = "10min")
    
    out = []
    
    for time in times:
        print(time)
        kwargs = dict(
             dn = time, 
             glat = mlat, 
             glon = mlon,
             hmin = 150 
             )
         
        base = io.test_data(**kwargs)
        
        gamma = ((9.81/ base["nui"]) * io.scale_gradient(base["ne"]))
        
        out.append(gamma[base.index == alt])
        
    return out, times

start = dt.datetime(2013, 1, 1, 0, 0)
end = dt.datetime(2013, 1, 2, 23, 50)
alt = 300
out, times = timeseries_local(start, end, alt)