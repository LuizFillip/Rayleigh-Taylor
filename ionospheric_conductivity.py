import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as const
from datetime import datetime
import pandas as pd
from nrlmsise00 import msise_flat
from iri2016 import IRI

from sys import exit

def get_concentrations_profiles(TN, 
                                o_point, 
                                o2_point, 
                                n2_point, 
                                DZ):
    
    JMAX = len(TN)
    
    CO = np.zeros(JMAX)                 # creating 1d array
    CO2 = np.zeros(JMAX)                # creating 1d array
    CN2 = np.zeros(JMAX)                # creating 1d array

    
    HB = 200.0                          # F region base  height [km]

    
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
        CN2[J] = p_cn2 * np.exp(-(Z1 - 335.0) / HN2) 
    return CO, CO2, CN2


def ion_neutral_collision(Tn, O, O2, N2):
    """The ion-neutral collision rates (frequency)"""
    term_O = 4.45e-11 * O * np.sqrt(Tn) * (1.04 - 0.067 * np.log10(Tn))**2
    term_O2 = 6.64e-10 * O2
    term_N2 = 6.82e-10 * N2
        
    return term_O + term_O2 + term_N2


def electron_neutral_collision(Tn, Nn):
    """The electron-neutral collision rates (frequency)"""
    return (5.4e-10) * Nn * np.sqrt(Tn)

def electron_cyclotron(B = 0.285e-04):
    """Electron gyro frequency"""
    return - (const.elementary_charge * B / const.electron_mass)

def ion_cyclotron(B = 0.285e-04):
    """Ion gyro frequency"""
    return (const.elementary_charge * B / const.proton_mass)

def electron_ratio(nu_e, B = 0.285e-04):
    """Electron ratio cyclotron frequency and collision"""
    return (-const.elementary_charge * B) / (const.electron_mass * nu_e)

def ion_ratio(nu_i, B = 0.285e-04):
    """Ion ratio cyclotron frequency and collision"""
    return (const.elementary_charge * B) / (const.proton_mass * nu_i)

def electron_mobility(nu_e):
    """Electric mobility for electrons (mass transport)"""
    return (-const.elementary_charge) / (const.electron_mass * nu_e)

def ion_mobility(nu_i):
    """Electric mobility for ions (mass transport)"""
    return (const.elementary_charge) / (const.proton_mass * nu_i)
    
def parallel_conductivity(Ne, nu_e, nu_i):
    """conductivity along magnetic field"""
    ion_term = 1 / (const.proton_mass * nu_i)
    electron_term  = 1 / (const.electron_mass * nu_e)
    return (Ne * const.elementary_charge**2 * (electron_term + ion_term))


def Pedersen_conductivity(Ne, nu_e, nu_i, B = 0.285e-04):
    """Conductivity along the electric field and perpendicular to the magnetic field"""
    electron_term = electron_mobility(nu_e) / (1 + electron_ratio(nu_e, B = B)**2)
    
    ion_term = ion_mobility(nu_i) / (1 + ion_ratio(nu_i, B = B)**2)
    
    return Ne * const.elementary_charge * (ion_term - electron_term)



def Hall_conductivity(Ne, nu_e, nu_i, B = 0.285e-04):
    """Conductivity perpendicular to both electric and magnetic field"""
    electron_term = electron_ratio(nu_e, B = B)**2 / (1 + electron_ratio(nu_e, B = B)**2)
    
    ion_term =  ion_ratio(nu_i, B = B)**2 / (1 + ion_ratio(nu_i, B = B)**2)
    
    return (Ne * const.elementary_charge / B) * (electron_term - ion_term)


def main():
    
    
    
    
    def get_profiles(glat, glon, date, alts):
        
        res = msise_flat(date, alts[None, :], glat, glon, 100, 150, 4)
        
        
        columns= ["He", "O", "N2", "O2", "Ar", "mass", 
                  "H", "N", "AnO", "Tex", "Tn"]
        
        df = pd.DataFrame(res[0], 
                          index = alts, 
                          columns = columns)
        
        iri = IRI(date, (hmin, hmax - step, step), glat, glon)
        
        Ne = iri.ne.values
        Te = iri.Te.values

        df["nui"] = ion_neutral_collision(df.Tn, df.O, 
                                          df.O2, df.N2)
        
        df["Nn"] = df[["He", "O", "N2", 
                       "O2", "Ar", "H", "N"]].sum(axis = 1)
        
        df["nue"] = electron_neutral_collision(Te, df.Nn)
        
        return Pedersen_conductivity(Ne, df.nue, df.nui)
    

    
    
    
    step = 5
    hmax = 600
    hmin = 100
    alts = np.arange(hmin, hmax, step)
    date = datetime(2014, 1, 1, 23, 0, 0)
    
    glon = -40
    
    from geomagnetic_parameters import string_to_list
    
    
    
    def integrated_values(alts, date, glon = 0, lat_max = 30, delta = 5):
        
        
        
        out = []
        for glat in np.arange(-2, lat_max + delta, delta):
            mlat = string_to_list(0, glat, glon, date)[0]
        
            sigma_p = get_profiles(float(glat), glon, date, alts)
            
            sigma_1 = sigma_p.values * (1 + 3 * np.sin(np.radians(mlat))**2)
            
            out.append(sigma_1)
        
        Re = 6.371009e6
        L = 1
        
        integrated = 2*Re*L*(np.sum(np.vstack(out).T, axis = 1))*delta
       
        return sigma_p.index, integrated
    
    altitude, sigma = integrated_values(alts, date, glon = 0)
    
    #(sigma)
        
    plt.plot(sigma, altitude)
    
    plt.xscale("log")
    
    #plt.yscale("log")
main()