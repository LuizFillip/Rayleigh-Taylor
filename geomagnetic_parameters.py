import pyIGRF
import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as const
import datetime
import time

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

date = datetime.datetime(2019, 1, 1)

def dip(latitude, longitude, date, altitude = 1):

    date_fraction = toYearFraction(date)
    
    D, I, H, X, Y, Z, F = pyIGRF.igrf_value(latitude, 
                                longitude, 
                                altitude, 
                                date_fraction)
    
    # Latitude inlicação magnética (dip)
    return np.degrees(np.arctan(np.tan(np.radians(I)) / 2))




    
import spacepy.coordinates as coord
from spacepy.time import Ticktock

def string_to_list(alt, lat, lon, date):
    
    """
    Convert the results from 'geo_to_mag' functions
    from numeric tuple
    
    """

    first = str(geo_to_mag(alt, lat, lon, date))
    
    start = first.find('[[')
    end = first.find(']]')
    last = first[start + 2:end].split(', ')
    
    list_as_numeric = [float(num) for num in last]
    
    lat_mag = list_as_numeric[1]
    lon_mag = list_as_numeric[2]
    return round(lat_mag, 2), round(lon_mag, 2)


def geo_to_mag(alt, lat, lon, date):
    #call with altitude in kilometers and lat/lon in degrees 
    
    Re = 6378.0 #mean Earth radius in kilometers
    
    #setup the geographic coordinate object with altitude in earth radii 
    cvals = coord.Coords([float(alt + Re), 
                          float(lat), float(lon)], 
                         'GEO', 'sph', ['Re','deg','deg'])
    
    date = str(date).replace(' ', 'T')
    #set time epoch for coordinates:
    cvals.ticks = Ticktock([date], 'UTC')
    
    #return the magnetic coords in the same units as the geographic:
    return cvals.convert('MAG','sph')

latitude = np.arange(-30, 30, 1)

#:
mag_lats = [string_to_list(700, lat, 0, date)[0] 
            for lat in latitude]

for alt in range(0, 1000, 100):
    plt.plot(mag_lats, dipole_magnetic_field(mag_lats, h = alt))