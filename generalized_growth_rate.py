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
    alts = np.arange(hmin, hmax + step, step)
    
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
    infile = "G://My Drive//Python//data-analysis//Rayleigh-Taylor//database//density//"
    filename = "20140101.txt"
    df = pd.read_csv(infile + filename, index_col = 2)
    df.index = pd.to_datetime(df.index)
    
    df = df.rename(columns = {"Unnamed: 0": "alts"})
    
    return df.loc[(df.index == date), :]


def get_winds(glat, glon, date):
    d, i, h, x, y, z, f = pyIGRF.igrf_value(glat, glon, 
                                            year = toYearFraction(date))

    df = pd.read_csv("G://My Drive//Python//data-analysis//Rayleigh-Taylor//database//winds//" + "20140101.txt", 
                 index_col = 1)
    df.index = pd.to_datetime(df.index)
    df = df.rename(columns = {"Unnamed: 0": "alts"})
    
    df["U"] = (df.zon * np.cos(np.radians(d)) + 
               df.mer * np.sin(np.radians(d)))
    
    # & (df.alts <= 600)
    return df.loc[(df.index == date), :]



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
    L = np.gradient(np.log(Ne), dz)*factor #(1 / Ne) *
    return L

def growth_rate_RT(nu, L, R, Vp, U):
    """Generalized instability rate growth"""
    return (Vp - U + sc.g / nu)*L - R







hmin = 100
hmax = 800
step = 5
glat = -3.73 
glon = -38.522
date = datetime.datetime(2014, 1, 1, 21, 10)



Nn = msis_data(glat, glon, date, hmin, hmax, step)


Ne = get_density(date)

U = get_winds(glat, glon, date).U.values 

Vp = np.mean([24.649, 22.402, 19.696])
nu  = collision_frequency(Nn.Tn, Nn.O, Nn.O2, Nn.N2).values
R = recombination(Nn.O2, Nn.N2, Nn.Tn).values
L = length_scale_gradient(Ne.Ne.values*1e6, 5)
gamma = growth_rate_RT(nu, L, R, Vp, U)


alts = Nn.index.values


def main():
    fig, ax = plt.subplots()
    ax.plot(gamma, alts)
    
    ax.set(xlim = [-2e-4, 2e-4])
    
main()