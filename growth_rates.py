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
from generic import float_to_time

def runMSISE(date, 
              hmin = 100, 
              hmax = 600, 
              step = 1, 
              glat = -3.73, 
              glon = -38.522):
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


class neutral_parameters(object):
    
    def __init__(self, TN, O, O2, N2):
        self.tn = TN
        self.o = O
        self.o2 = O2
        self.n2 = N2

    @property
    def collision(self):
        """Collision frequency from Bailey and Balan 1992"""
        nu_o = (4.45e-11 * self.o * np.sqrt(self.tn) * 
               (1.04 - 0.067 * np.log10(self.tn)) ** 2.0)
        
        nu_o2 = (6.64e-10 * self.o2)
        
        nu_n2 = 6.82e-10 * self.n2
        
        return  nu_o + nu_o2 + nu_n2
    
    @property
    def recombination(self):
        
        return (4.0e-11  * self.o2) + (1.3e-12   * self.n2)    
  
def length_scale_gradient(Ne, dz = 1):
    """Vertical variation of """
    factor = 1e-3 #convert km to meters
    L = np.gradient(np.log(Ne), dz)*factor
    return L



class PRE(object):
    
    def __init__(self, infile):
    
        df = pd.read_csv(infile, index_col = 0)
    
        df = df.dropna()
    
        time = df["time"].apply(lambda x: float_to_time(x))
        df.index = pd.to_datetime(df.index + " " + time)
        
        self.df = df
        self.pre = self.df["vz"].values
        self.times = self.df.index



class getPyglow(object):
    
    def __init__(self, 
                 date, 
                 infile =  "database/pyglow/" ):
        self.infile = infile
        self.date = date

    @staticmethod
    def read(infile):
        
        df = pd.read_csv(infile,index_col = 0)
        df["date"] = pd.to_datetime(df["date"])
        return df
    
    def winds(self, 
              filename = "winds2014_2015.txt", 
              glat = -3.73, 
              glon = -38.522, 
              component = "U"):
        
        df = self.read(self.infile + filename)
        
        d, i, h, x, y, z, f = pyIGRF.igrf_value(glat, glon, 
                                                year = toYearFraction(date))

        df["U"] = (df.zon * np.cos(np.radians(d)) + 
                   df.mer * np.sin(np.radians(d)))
        return df.loc[(df["date"] == self.date), component].values
        
    
    def density(self,
                filename = "density2014_2015.txt"):
        
        df = self.read(self.infile + filename)
        
        return df.loc[(df["date"] == self.date), "Ne"].values
    

def growth_rate_RT(nu, L, R, Vp, U):
    """
    Generalized instability rate growth
    Paramaters:
    ---------- 
    Vp: Prereversal Enhancement (PRE)
    U: Neutral wind
    nu: ion-neutral collisional frequency
    L: gradient scale
    R: Recombination
    
    """
     
    return (Vp - U + (9.81 / nu))*L - R
    
infile = "database/PRE/FZ_PRE_2014_2015.txt"

pre = PRE(infile)

out_res = []

for i in range(len(pre.times)):
   
    date = pre.times[i]
    
    vz = pre.pre[i]
    
    pyglow = getPyglow(date)
    
    
    ne = pyglow.density()
    u = pyglow.winds()
    dat = runMSISE(date)
    
    
    neutral = neutral_parameters(dat.Tn.values, 
                                  dat.O.values, 
                                  dat.O2.values, 
                                  dat.N2.values)
    
    nu = neutral.collision
    r = neutral.recombination
    
    l = length_scale_gradient(ne*1e6)
    
    alts = dat.index.values
    
    gamma = growth_rate_RT(nu, l, r, vz, u)
    no_wind = growth_rate_RT(nu, l, r, vz, 0)
    no_r = growth_rate_RT(nu, l, 0, vz, u)
    no_r_wind = growth_rate_RT(nu, l, 0, vz, 0)
    local = growth_rate_RT(nu, l, 0, 0, 0)
    out_gammas = []
    out_res.append(out_gammas)
    
    for elem in [gamma, no_wind, no_r, 
                 no_r_wind, local]:
        
    
        max_gamma = elem[(alts > 200) & (alts < 400)]
    
    
        out_gammas.append(np.max(max_gamma))
        
df = pd.DataFrame(out_res, 
                  index = pre.times, 
                  columns = ["all", "nowind", 
                             "noreco", "nowindReco", 
                             "local"])

df.to_csv("database/growthRates/gammas.txt", 
          sep = ",", 
          index = True)
#%%
def collision_and_recombination(hmin, hmax, 
                                step, glat, glon, date):
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



    
