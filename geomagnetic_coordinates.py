import numpy as np
import matplotlib.pyplot as plt


def apex_factor(lat, h):
    Re = 6378.165
    return ((h + Re) / (Re * (1 - np.sin(np.radians(lat))**2)))


def apex_height(lat, L, h):
    Re = 6378.165
    return (h + Re) * np.cos(np.radians(lat))
    
def apex_latitude(ha):
    Re = 6378.165
    A = 1 + (ha / Re)
    return np.degrees(np.arccos(1 / pow(A, 0.5)))



    
h = 200 #km

heights = np.arange(0, 700, 10)

out = []


fig, ax = plt.subplots()    
for h in [200, 300, 500]:
    lat = apex_latitude(h)
    num = 100
    range_lat = np.linspace(-lat, lat, num)
    
    L = apex_factor(lat, h)
   
    ax.plot(range_lat, apex_height(range_lat, L, h))
    
    
    ax
    
