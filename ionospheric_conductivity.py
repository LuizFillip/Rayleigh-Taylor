import numpy as np
import scipy.constants as const


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

def electron_mobility(nu_e):
    """Electric mobility for electrons (mass transport)"""
    return (-const.elementary_charge) / (const.electron_mass * nu_e)

def ion_mobility(nu_i):
    """Electric mobility for ions (mass transport)"""
    return (const.elementary_charge) / (const.proton_mass * nu_i)


def electron_ratio(nu_e, B = 0.285e-04):
    """Electron ratio cyclotron frequency and collision"""
    return electron_cyclotron(B) / nu_e

def ion_ratio(nu_i, B = 0.285e-04):
    """Ion ratio cyclotron frequency and collision"""
    return ion_cyclotron(B) / nu_i

    
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

def dl(lat, dzeta, Re = 6.371009e6, L = 1):
    zeta = np.sin(np.radians(lat))
    return pow((1 + 3 * zeta**2), 0.5) * Re * L * dzeta
    
def pedersen(Ne, nui, B):
    return Ne * const.proton_mass * nui / B**2

   
def Hall_conductivity(Ne, nu_e, nu_i, B = 0.285e-04):
    """Conductivity perpendicular to both electric and magnetic field"""
    electron_term = electron_ratio(nu_e, B = B)**2 / (1 + electron_ratio(nu_e, B = B)**2)
    
    ion_term =  ion_ratio(nu_i, B = B)**2 / (1 + ion_ratio(nu_i, B = B)**2)
    
    return (Ne * const.elementary_charge / B) * (electron_term - ion_term)




