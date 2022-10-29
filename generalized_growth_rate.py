import datetime
import pandas as pd
import matplotlib.pyplot as plt
from nrlmsise00 import msise_flat
import numpy as np 
from iri2016 import IRI
import scipy.constants as sc
import pyIGRF
from nrlmsise00.dataset import msise_4d
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





def get_winds(glat, glon, date):
    
    df = pd.read_csv("database/pyglow/winds2014.txt", 
                 index_col = 0)
    df["date"] = pd.to_datetime(df["date"])

    
    
    d, i, h, x, y, z, f = pyIGRF.igrf_value(glat, glon, 
                                            year = toYearFraction(date))

    
    df["U"] = (df.zon * np.cos(np.radians(d)) + 
               df.mer * np.sin(np.radians(d)))
    
   
    return df.loc[(df["date"] == date), :]


def get_density(date):

    df = pd.read_csv("database/pyglow/density2014.txt", index_col = 2)
    df.index = pd.to_datetime(df.index)
    
    df = df.rename(columns = {"Unnamed: 0": "alts"})
    
    return df.loc[(df.index == date), :]


def get_PRE():
    df = pd.read_csv("database/pyglow/PRE2014.txt", 
                     delimiter = ";")
    def float_to_time(time):
         args = str(time).split(".")
         hour = int(args[0])
         minute = int(float("0." + args[1])*60)
         return f"{hour}:{minute}"
   
    df["time2"] = df["time"].apply(lambda x: float_to_time(x))
    
    df.index = pd.to_datetime(df.Date + " " + df.time2)
    
    del df["time2"], df["Date"]
    return df

def collision_and_recombination(hmin, hmax, 
                                step, glat, glon):
    alts = np.arange(hmin, 
                     hmax + step, 
                     step)   
    msi = msise_4d(date, alts, glat, glon)
    
    ref_alt = 300.0 

    point = msi.sel(alt = ref_alt)
    o_point = point["O"].values.ravel()[0]
    o2_point = point["O2"].values.ravel()[0]
    n2_point = point["N2"].values.ravel()[0]
    TN = msi.Talt.values.ravel()    

    JMAX = len(TN)                       # height step [km]
    
    CO = np.zeros(JMAX)                 # creating 1d array
    CO2 = np.zeros(JMAX)                # creating 1d array
    CN2 = np.zeros(JMAX)                # creating 1d array
    BETA = np.zeros(JMAX)               # creating 1d array
    CFO = np.zeros(JMAX)                # creating 1d array
    
    HB = 200.0                          # F region base  height [km]
    RK1 = 4.0E-11                       # recombination of O+ with O2
    RK2 = 1.3E-12                       # recombination of O+ with N2
    
    for J in range(0, JMAX):
        Z1 = HB + step * J
        GR = 1.0 / (1.0 + Z1 / 6370.0) ** 2.0
        HO = 0.0528 * TN[J] / GR                               # scale height of O [km]
        HO2 = 0.0264 * TN[J] / GR                              # scale height of O2 [km]
        HN2 = 0.0302 * TN[J] / GR                              # scale height of N2 [km]

        p_co = np.float64(o_point / 5.33 * 8.55)
        p_co2 = np.float64(o2_point / 1.67 * 4.44)
        p_cn2 = np.float64(n2_point / 9.67 * 2.26)

        CO[J] = p_co * np.exp(-(Z1 - ref_alt) / HO)           # atomic oxygen [cm-3]
        CO2[J] = p_co2 * np.exp(-(Z1 - ref_alt) / HO2)        # molecular oxygen [cm-3]
        CN2[J] = p_cn2 * np.exp(-(Z1 - ref_alt) / HN2)        # atomic oxygen[cm-3]
        BETA[J] = (RK1 * CO2[J]) + (RK2 * CN2[J])           # recombination [s-1]

        # COLLISION
        CFO[J] = (4.45E-11 * CO[J] * np.sqrt(TN[J]) * 
                  (1.04 - 0.067 * np.log10(TN[J])) ** 2.0 + 
                  6.64E-10 * CO2[J] + 6.82E-10 * CN2[J])
        
        
    return BETA, CFO


def growth_rate_RT(nu, L, R, Vp, U):
    """Generalized instability rate growth"""
    return (Vp - U + sc.g / nu)*L - R

hmin = 100
hmax = 600
step = 1
glat = -3.73 
glon = -38.522
df = get_PRE()

date = df.index[0]
     
R, nu = collision_and_recombination(hmin, hmax, 
                                    step, glat, glon)
U = get_winds(glat, glon, date).U.values
Vp = df.loc[df.index == date, "peak"].values[0]
Ne = get_density(date).Ne.values

L = length_scale_gradient(Ne*1e6, step)
gamma = growth_rate_RT(nu, L, R, Vp, U)

print(max(gamma))
alts = np.arange(hmin, 
                 hmax + step, 
                 step)   

fig, ax = plt.subplots()
ax.plot(gamma, alts)

ax.set(xlim = [-2e-3, 2e-3])

result = [gamma[alts == 200][0], 
          gamma[alts == 250][0],
          gamma[alts == 300][0], 
          gamma[alts == 350][0], 
          gamma[alts == 400][0]]


print(result)
def main():
    
    
    
    
            
    
    
    Nn = msis_data(glat, glon, date, hmin, hmax, step)
    nu  = collision_frequency(Nn.Tn, Nn.O, Nn.O2, Nn.N2).values
    R = recombination(Nn.O2, Nn.N2, Nn.Tn).values
    L = length_scale_gradient(Ne*1e6, step)
    gamma = growth_rate_RT(nu, L, R, Vp, 0)
    
    print(max(gamma))
    alts = Nn.index.values
    fig, ax = plt.subplots()
    ax.plot(gamma, alts)
    
    ax.set(xlim = [-2e-3, 2e-2])
            
    
