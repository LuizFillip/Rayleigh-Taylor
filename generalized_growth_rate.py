import datetime
import pandas as pd
import matplotlib.pyplot as plt
from nrlmsise00 import msise_flat
import numpy as np 
from iri2016 import IRI
import scipy.constants as sc
import pyIGRF

from geomagnetic_parameters import toYearFraction


def msis_data(glat, glon, date, hmin, hmax, step):
    alts = np.arange(hmin, hmax, step)
    
    iri = IRI(date, (hmin, hmax - step, step), glat, glon)
    
    attrs = iri.attrs
    
    
    res = msise_flat(date, alts[None, :], glat, glon, 100, 
                     attrs["f107"], attrs["ap"])
    
    
    columns= ["He", "O", "N2", "O2", "Ar", 
              "mass", "H", "N", "AnO", "Tex", "Tn"]
    
    df = pd.DataFrame(res[0], 
                      index = alts, 
                      columns = columns)
    
    df.drop(["He", "Ar", 
             "mass", "H", "N", "AnO", "Tex"], 
            axis = 1, 
            inplace = True)
    
    return df

def get_density(date):
    infile = "database/density/"
    filename = "20140101.txt"
    df = pd.read_csv(infile + filename, index_col = 2)
    df.index = pd.to_datetime(df.index)
    
    df = df.rename(columns = {"Unnamed: 0": "alts"})
    
    return df.loc[df.index == date, :]



hmin = 100
hmax = 800
step = 5
glat = -3.73 
glon = -38.522
date = datetime.datetime(2014, 1, 1, 18, 0)



Nn = msis_data(glat, glon, date, hmin, hmax, step)


Ne = get_density(date)


def collision_frequency(TN, O, O2, N2):
    
    return (4.45e-11 * O * np.sqrt(TN) * 
            (1.04 - 0.067 * np.log10(TN)) ** 2.0 + 
            6.64e-10 * O2 + 6.82e-10 * N2)

def recombination(O2, N2, T):
    
    RK1 = 4.0e-11   # recombination of O+ with O2
    RK2 = 1.3e-12   # recombination of O+ with N2
    return (RK1 * O2) + (RK2 * N2)    
  
def length_scale_gradient(Ne, dz):
    factor = 1e-3
    L = ((1 / Ne) * (np.gradient(Ne, dz)))*factor
    return L[1:]

def growth_rate_RT(nu, L, R, Vp, U):
    """Generalized instability rate growth"""
    return (Vp - U - (sc.g / nu) )*L - R



def get_winds(glat, glon, date):
    d, i, h, x, y, z, f = pyIGRF.igrf_value(glat, glon, 
                                            year = toYearFraction(date))

    df = pd.read_csv("database/winds/" + "20140101.txt", 
                 index_col = 1)
    df.index = pd.to_datetime(df.index)
    df = df.rename(columns = {"Unnamed: 0": "alts"})
    
    df["U"] = (df.zon * np.cos(np.radians(d)) + 
               df.mer * np.sin(np.radians(d)))
    return df.loc[df.index == date, :]

win = get_winds(glat, glon, date)
print(win)