import numpy as np
import matplotlib.pyplot as plt

def colatitude(latitude):
    return (np.pi / 2) - latitude

def dip(inclination):
   """Latitude inlicação magnética (dip) """
   return np.degrees(np.arctan(0.5*np.tan(np.radians(inclination)) / 2))

def dipole_magnetic_field(colatitude, h = 1):
    Re = 6.371009e6
    return ((h + Re)) * (np.cos(np.radians(colatitude)))**2


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
    

def main():
    dz = 50
        
    heights = np.arange(200, 700 + dz, dz)
    
    
    fig, ax = plt.subplots()   
        
    for h in heights:
        lats, apex = apex_range(h, num = 15)
        ax.plot(lats, apex, color = "k")    
       


   
  
