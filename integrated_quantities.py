import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as const
import pandas as pd
from generic import read_iri

def integrated_values(alts, date, glon = 0, 
                      lat_max = 30, 
                      delta = 5):
    

    out = []
    for glat in np.arange(0, lat_max + delta, delta):
        mlat = string_to_list(0, glat, glon, date)[0]
    
        sigma_p = get_profiles(float(glat), glon, date, alts)
        
        sigma_1 = sigma_p.values * (1 + 3 * np.sin(np.radians(mlat))**2)
        
        out.append(sigma_1)
    
   
    L = 1
    
    integrated = 2*Re*L*(np.sum(np.vstack(out).T, axis = 1))*delta
   
    return sigma_p.index, integrated
   


from mag_parameters import apex_latitude, apex_range

Ne = []

for i in range(0, 35, 5):
    
    df = read_iri(f"database/density_magnetic/{i}.txt")
    alts = df[0].values 
    Ne.append(df[1].values* 1e-6)
    

ne = np.vstack(Ne).T
mlats = np.arange(0, 35, 5)

def interpolate_data():
    from scipy import interpolate
    
    X = np.arange(0, 35, 5)
    Y = alts
    
    x,y = np.meshgrid(X,Y)
    
    
    f = interpolate.interp2d(x, y, ne, kind='cubic')
    
    Xnew = np.linspace(0, 35, 50)
    Ynew = np.linspace(100, 700, 1000)
    
    
    return f(Xnew,Ynew)



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
    
    
plotContourfMagLines(Ynew, Xnew, neI)