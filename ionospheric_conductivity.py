import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as const
from datetime import datetime
import pandas as pd
from nrlmsise00 import msise_flat
from iri2016 import IRI

from sys import exit



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
    
    step = 5
    hmax = 600
    hmin = 100
    alts = np.arange(hmin, hmax, step)
    date = datetime(2014, 1, 1, 23, 0, 0)
    
    glat = 0
    glon = 0
    res = msise_flat(date, alts[None, :], glat, glon, 100, 150, 4)
    
    
    columns= ["He", "O", "N2", 
              "O2", "Ar", "mass", 
              "H", "N", "AnO", 
              "Tex", "Tn"]
    
    df = pd.DataFrame(res[0], 
                      index = alts, 
                      columns = columns)
    
    iri = IRI(date, (hmin, hmax - step, step), glat, glon)
    
    Ne = iri.ne.values
    
    
    df["nui"] = ion_neutral_collision(df.Tn, df.O, 
                                      df.O2, df.N2)
    
    df["Nn"] = df[["He", "O", "N2", 
                   "O2", "Ar", "H", "N"]].sum(axis = 1)
    
    df["nue"] = electron_neutral_collision(df.Tn, df.Nn)
    
    sigma_P = Pedersen_conductivity(Ne, df.nue, df.nui)
    
    Re = 6.371009e6
    L = 1
    mlat = 2.93
    
    from scipy.integrate import cumtrapz
    
    
    def f1(sigma_P, x):
        Re = 6.371009e6
        L = 1
        return 2*Re*L*sigma_P*(1 + 3 * np.sin(np.radians(x))**2)
    
    
    integrated_P =  cumtrapz(f1(3, mlat), df.index)

    #integrated_P = 2*Re*L*sigma_P*(1 + 3 * np.sin(np.radians(mlat))**2)
    
    plt.plot(integrated_P, df.index)
    
    plt.xscale("log")    

main()