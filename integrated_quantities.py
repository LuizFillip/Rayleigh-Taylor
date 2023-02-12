import numpy as np
import matplotlib.pyplot as plt
from RayleighTaylor.base.mag import apex_latitude, apex_range

def dl(lat, dzeta, Re = 6.371009e6, L = 1):
    zeta = np.sin(np.radians(lat))
    return pow((1 + 3 * zeta**2), 0.5) * Re * L * dzeta

def integrated_density(delta = 5):
    

    Ne = []

    for i in range(0, 35, delta):
        
        df = read_iri(f"database/density_magnetic/{i}.txt")
        alts = df[0].values 
        Ne.append(df[1].values* (1 - np.sin(np.radians(i))**2)**3)
        

    ne = np.vstack(Ne).T
    delta = 5
    L = 1
    Re = 6.31e6
    integrated = 2*Re*L*np.sum(ne, axis = 1)*delta

    plt.plot(integrated, alts)

    plt.xlabel("Densidade integradas")
    plt.ylabel("Altura de apex")
    return alts, integrated
   

fig, ax = plt.subplots()   

h = 400
    
#for h in heights:
lats, apex = apex_range(h, num = 10)

#print(apex[lats > 0])

ax.plot(lats, apex, marker = "o", color = "k")    
    
ax.set(xlim = [-20, 0], ylim = [100, 700])
    
for hh in apex:
    ax.axhline(h)
from geo.conversions import mag2geo
import datetime as dt

date = dt.datetime(2014, 1, 1)

mag_lon = 0

lats = lats[lats < 0]

import iri2016
out = []
x = []
for mag_lat in lats:

    glat, glon = mag2geo(mag_lat, mag_lon, date)
    #print(glat, glon, mag_lat)
    ax.axvline(mag_lat, color = "r") 
    ax.text(mag_lat, 600, round(glat, 2), transform = ax.transData)
    altkmrange = [100, 700, 50]
    x.append(glat)
        
    iono = iri2016.IRI(date, altkmrange, glat, glon)

    out.append(iono.ne.values)
    

#%%    
altkmrange = [100, 700, 50]
    
plt.contourf(x[::-1], 
             iono.alt_km.values, 
             np.array(out).T, 
             50)

print()
#%%
plt.plot(ne, alts, marker = "o", 
         label = f"glat: {round(glat, 2)},\n mlat: {round(mag_lat, 2)}")

#-52/-7.5, -51/4.68
plt.legend()

