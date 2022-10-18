import pyIGRF
import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as const
import datetime
import time
import spacepy.coordinates as coord
from spacepy.time import Ticktock
import pandas as pd

def toYearFraction(date):
    
    "Return years in fraction (like julian date) "

   # returns seconds since epoch
    def sinceEpoch(date): # returns seconds since epoch
        return time.mktime(date.timetuple())
    
    s = sinceEpoch
    
    year = date.year
    startOfThisYear = datetime.datetime(year = year, 
                                        month = 1, day = 1)
    startOfNextYear = datetime.datetime(year = year + 1, 
                                        month = 1, 
                                        day = 1)
    
    yearElapsed = s(date) - s(startOfThisYear)
    yearDuration = s(startOfNextYear) - s(startOfThisYear)
    fraction = yearElapsed/yearDuration
    
    return date.year + fraction

def dipole_magnetic_field(colatitude, h = 1):
    Re = 6.371009e6
    return ((h + Re)) * (np.cos(np.radians(colatitude)))**2

def colatitude(latitude):
    return (np.pi / 2) - latitude



def dip(inclination):
   """Latitude inlicação magnética (dip) """
   return np.degrees(np.arctan(0.5*np.tan(np.radians(inclination)) / 2))

def geo2mag(geo_lat, geo_lon, date):
    """
    return the magnetic coords in the 
    same units as the geographic"""
    
    Re = 6378.0 #mean Earth radius in kilometers
     
    cvals = coord.Coords([float(300 + Re), 
                          float(geo_lat), 
                          float(geo_lon)], 
                         'GEO', 'sph', 
                         ['Re','deg','deg'])
    
    date = date.strftime("%Y-%m-%dT%H:%M")
    cvals.ticks = Ticktock([date], 'UTC')
    
    dat_coords =  cvals.convert('MAG','sph').data[0]
    
    mag_lat = dat_coords[1]
    mag_lon = dat_coords[2]
    
    return (mag_lat, mag_lon)





def mag2geo(mag_lat, mag_lon, date):
    
    """
    Convert the results from 'geo_to_mag' functions
    from numeric tuple
    
    """
    
    r = 6378.0
    
    date = date.strftime("%Y-%m-%dT%H:%M")
    
    cvals = coord.Coords([float(300 + r), 
                          float(mag_lat), 
                          float(mag_lon)], 
                         'MAG', 'sph', 
                         ['Re','deg','deg'])
    
    
    cvals.ticks = Ticktock([date], 'UTC')
    
    dat_coords = cvals.convert('GEO','sph').data[0]
    
    geo_lat = dat_coords[1]
    geo_lon = dat_coords[2]
    
    
    return (geo_lat, geo_lon)

def main():

    mag_lat = 0
    mag_lon = -40
    
    date = datetime.datetime(2014, 1, 1)
    geo_lat, geo_lon = mag2geo(mag_lat, mag_lon, date)
    
    
    print(geo2mag(geo_lat, geo_lon, date))