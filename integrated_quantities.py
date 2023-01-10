import numpy as np
import matplotlib.pyplot as plt
from generic import read_iri

from mag_parameters import apex_latitude, apex_range



def integrated_density(alts, date, glon = 0, 
                      lat_max = 30, 
                      delta = 5):
    

    Ne = []

    for i in range(0, 35, 5):
        
        df = read_iri(f"database/density_magnetic/{i}.txt")
        alts = df[0].values 
        Ne.append(df[1].values* (1 - np.sin(np.radians(i))**2)**3)
        

    ne = np.vstack(Ne).T
    delta = 5
    L = 1
    Re = 6.31e6
    integrated = 2*Re*L*np.sum(ne, axis = 1)*delta

    #plt.plot(integrated, alts)

    #plt.xscale("log")
    mlats = np.arange(0, 35, 5)
   
    return alts, integrated
   




def plotContourfMagLines(alts, mlats, ne):
    

    fig, ax = plt.subplots()   
    
    ax.contourf(mlats, alts, ne, 50)
    
    dz = 50
    hmin = min(alts)
    hmax = max(alts)
    
    heights = np.arange(hmin, hmax + dz, dz)
        
    for h in heights:
        lats, apex = apex_range(h, num = 10)
        
        ax.plot(lats, apex, color = "k")    
        
    ax.set(xlim = [0, 20], ylim = [100, 700])
    
    
