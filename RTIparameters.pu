from nrlmsise00.dataset import msise_4d
from nrlmsise00 import msise_model
import numpy as np 
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, date, time
from config_plotting import *
from iri2016 import IRI
import matplotlib.ticker as ticker
import locale
import scipy.constants as sc
import pandas as pd








def collision_and_recombination(o_point, o2_point, n2_point, 
                                TN, JMAX, DZ = 5.0):
    
                                # height step [km]
    
    CO = np.zeros(JMAX)                 # creating 1d array
    CO2 = np.zeros(JMAX)                # creating 1d array
    CN2 = np.zeros(JMAX)                # creating 1d array
    BETA = np.zeros(JMAX)               # creating 1d array
    CFO = np.zeros(JMAX)                # creating 1d array
    
    HB = 200.0                          # F region base  height [km]
    RK1 = 4.0E-11                       # recombination of O+ with O2
    RK2 = 1.3E-12                       # recombination of O+ with N2
    
    for J in range(0, JMAX):
        Z1 = HB + DZ * J
        GR = 1.0 / (1.0 + Z1 / 6370.0) ** 2.0
        HO = 0.0528 * TN[J] / GR                               # scale height of O [km]
        HO2 = 0.0264 * TN[J] / GR                              # scale height of O2 [km]
        HN2 = 0.0302 * TN[J] / GR                              # scale height of N2 [km]

        p_co = np.float64(o_point / 5.33 * 8.55)
        p_co2 = np.float64(o2_point / 1.67 * 4.44)
        p_cn2 = np.float64(n2_point / 9.67 * 2.26)

        CO[J] = p_co * np.exp(-(Z1 - 335.0) / HO)           # atomic oxygen [cm-3]
        CO2[J] = p_co2 * np.exp(-(Z1 - 335.0) / HO2)        # molecular oxygen [cm-3]
        CN2[J] = p_cn2 * np.exp(-(Z1 - 335.0) / HN2)        # atomic oxygen[cm-3]
        BETA[J] = (RK1 * CO2[J]) + (RK2 * CN2[J])           # recombination [s-1]

        # COLLISION
        CFO[J] = (4.45E-11 * CO[J] * np.sqrt(TN[J]) * 
                  (1.04 - 0.067 * np.log10(TN[J])) ** 2.0 + 
                  6.64E-10 * CO2[J] + 6.82E-10 * CN2[J])
        
        
    return BETA, CFO



def collision_frequency(TN, O, O2, N2):
    
    return (4.45e-11 * O * np.sqrt(TN) * 
            (1.04 - 0.067 * np.log10(TN)) ** 2.0 + 
            6.64e-10 * O2 + 6.82e-10 * N2)

def recombination(O2, N2, T):
    
    RK1 = 4.0E-11                       # recombination of O+ with O2
    RK2 = 1.3E-12                       # recombination of O+ with N2
    return (RK1 * O2) + (RK2 * N2)    
  
def length_scale_gradient(Ne, dz):
    factor = 1e-3
    L = ((1 / Ne) * (np.gradient(Ne, dz)))*factor
    return L[1:]

def growth_rate_RT(nu, L, R):
    """Local rate growth"""
    return ((sc.g / nu) * (L)) - R


df = pd.read_csv("iri2014.txt", 
                 header = None, 
                 delim_whitespace=(True))

dz = 0.5

altkmrange = (100, 599.5, dz)

glat = -3.9
glon = -38.45

alts = np.arange(altkmrange[0], 
                 altkmrange[1], 
                 dz)

out_gamma = []
out_time = []
year = 2014
import datetime

for doy in range(1, 366, 3):
    
    date_day = datetime.date(year, 1, 1) + datetime.timedelta(doy - 1)
    
    print("running...", date_day)
    for hour in range(0, 24, 1):
        
        time = datetime.datetime.combine(date_day, 
                                         datetime.time(hour, 0, 0))
        
        msi = msise_4d(time, alts, glat, glon)
        iri = IRI(time, altkmrange, glat, glon)

        point = msi.sel(alt = 335)
        o_point = point["O"].values.ravel()[0]
        o2_point = point["O2"].values.ravel()[0]
        n2_point = point["N2"].values.ravel()[0]
        T = msi.Talt.values.ravel()
        O = msi.O.values.ravel()



        O2 = msi.O2.values.ravel()
        N2 = msi.N2.values.ravel()


        R, nu = collision_and_recombination(o_point, o2_point, 
                                            n2_point, T, len(T), 
                                            DZ = dz)

        Ne = iri.ne.values
        alt_iri = iri.alt_km.values

        L = length_scale_gradient(Ne, dz)

        gamma = growth_rate_RT(nu, L, 0)

        result = [gamma[alts == 200][0], 
                  gamma[alts == 250][0],
                  gamma[alts == 300][0], 
                  gamma[alts == 350][0], 
                  gamma[alts == 400][0]]
        
        out_time.append(time)
        
        out_gamma.append(result)
        
        

df = pd.DataFrame(out_gamma,
                  index = out_time, 
                  columns = [200, 250, 300, 350, 400])


df.to_csv("gamms.txt", sep = ",", index = True)

'''


out_gamma.append(max(gamma))
out_time.append(time)

x = pd.to_datetime(np.array(out_time))
y = np.array(out_gamma)
import matplotlib.dates as dates
fig, ax = plt.subplots()

ax.plot(x, y)

ax.xaxis.set_major_formatter(dates.DateFormatter('%H'))
ax.xaxis.set_major_locator(dates.HourLocator(interval = 3))

'''
