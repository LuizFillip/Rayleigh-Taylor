import numpy as np
import matplotlib.pyplot as plt


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
    
heights = np.arange(0, 700, 10)


fig, ax = plt.subplots()    

for h in [0, 200, 500, 1000, 1500]:
    lats, apex = apex_range(h)
    ax.plot(lats, apex, color = "k")    
    ax.axhline(150)
    ax.set(ylim = [50, 1500])
