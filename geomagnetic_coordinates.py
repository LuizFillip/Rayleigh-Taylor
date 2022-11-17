import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from iri2016 import IRI
from geomagnetic_parameters import mag2geo

def density_integrated(Ne, lat, h):
    Re = 6378.165
    L = apex_factor(lat, h)
    N = pow((1 - pow(np.sin(np.radians(lat)), 2)), 3)
    return 2 * Re * Ne * N

def apex_factor(lat, h):
    Re = 6378.165
    return ((h + Re) / (Re * (1 - np.sin(np.radians(lat))**2)))


def apex_height(lat, h):
    Re = 6378.165
    return ((h + Re) * np.cos(np.radians(lat))**2) - Re
    
def apex_latitude(ha):
    Re = 6378.165
    A = 1 + (ha / Re)
    return np.degrees(np.arccos(1 / pow(A, 0.5)))


def apex_range(h, num = 200):
    lat = apex_latitude(h)
    latitudes = np.linspace(-lat, lat, num)
    
    return latitudes, apex_height(latitudes, h)
    




import datetime
dz = 50
altkmrange = (200, 700, dz)
time = datetime.datetime(2014, 1, 1)
    
heights = np.arange(200, 700 + dz, dz)

out_heights = []
    
for h in heights:
    lats, apex = apex_range(h, num = 15)
    #ax.plot(lats, apex, color = "k")    
    
    #ax.contourf(df.columns, df.index, df.values, 40, cmap = "jet")
    #ax.set(ylim = [200, 700], xlim = [0, 15])
    
    lon = -80
    density_out = []
    for lat in lats:
        if lat > 0:
            geo_lat, geo_lon = mag2geo(lat, lon, time)
            iri = IRI(time, altkmrange, geo_lat, geo_lon)
            density_out.append(density_integrated(iri.ne.values, lat, h))
    
    sum_lats = np.vstack(density_out).sum(axis = 0)
    
    out_heights.append(sum_lats)
    
    
#out.append()
#fig, ax = plt.subplots()    

res = np.vstack(out_heights) #.T.sum(axis = 0)
        

print(res)


dat = np.vstack(out)


N = np.sum(dat, axis = 1)

#print(len(alts), len(N))
plt.plot(N, alts[:-2])

plt.xscale("log")
#plt.scale("log")


def iri_matrix(infile_iri = "database/iri/"):

    def read_iri(infile):
        iri = pd.read_csv(infile, 
                     delim_whitespace=True, 
                     header = None, index_col= 0)
        
        return iri
    
    out_iri = []
    for mlat in  np.arange(0, 32.5, 2.5): 
        filename = f"mlat_{float(mlat)}.txt"
        
        dat = read_iri(infile_iri + filename)
        
        dat.rename(columns = {1 : -mlat}, 
                   inplace = True)
        dat.index.name = "alts"
        dat.columns.name = "lats"
        out_iri.append(dat.loc[:, -mlat])
        
        
    return pd.concat(out_iri, axis = 1)