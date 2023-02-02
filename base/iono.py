import numpy as np
import scipy. cants as  c

def scale_gradient(Ne, dz = 1):
    """length scale gradiendt : Vertical variation of density"""
    factor = 1e-3 #convert km to meters
    return np.gradient(np.log(Ne), dz)*factor

def electron_neutral_collision(Tn, Nn):
    """The electron-neutral collision rates (frequency)"""
    return (5.4e-10) * Nn * np.sqrt(Tn)

def electron_cyclotron(B = 0.285e-04):
    """Electron gyro frequency"""
    return - ( c.elementary_charge * B /  c.electron_mass)

def ion_cyclotron(B = 0.285e-04):
    """Ion gyro frequency"""
    return ( c.elementary_charge * B /  c.proton_mass)

def electron_mobility(nu_e):
    """Electric mobility for electrons (mass transport)"""
    return (- c.elementary_charge) / ( c.electron_mass * nu_e)

def ion_mobility(nu_i):
    """Electric mobility for ions (mass transport)"""
    return ( c.elementary_charge) / ( c.proton_mass * nu_i)

def electron_ratio(nu_e, B = 0.285e-04):
    """Electron ratio cyclotron frequency and collision"""
    return electron_cyclotron(B) / nu_e

def ion_ratio(nu_i, B = 0.285e-04):
    """Ion ratio cyclotron frequency and collision"""
    return ion_cyclotron(B) / nu_i

    
def parallel_conductivity(Ne, nu_e, nu_i):
    """conductivity along magnetic field"""
    ion_term = 1 / ( c.proton_mass * nu_i)
    electron_term  = 1 / ( c.electron_mass * nu_e)
    return (Ne *  c.elementary_charge**2 * (electron_term + ion_term))


def Pedersen_conductivity(Ne, nu_e, nu_i, B = 0.285e-04):
    """Conductivity along the electric field and perpendicular to the magnetic field"""
    electron_term = electron_mobility(nu_e) / (1 + electron_ratio(nu_e, B = B)**2)
    
    ion_term = ion_mobility(nu_i) / (1 + ion_ratio(nu_i, B = B)**2)
    
    return Ne *  c.elementary_charge * (ion_term - electron_term)


    
def pedersen(Ne, nui, B):
    return Ne *  c.proton_mass * nui / B**2

   
def Hall_conductivity(Ne, nu_e, nu_i, B = 0.285e-04):
    """Conductivity perpendicular to both electric and magnetic field"""
    electron_term = (electron_ratio(nu_e, B = B)**2 / 
                     (1 + electron_ratio(nu_e, B = B)**2))
    
    ion_term =  ion_ratio(nu_i, B = B)**2 / (1 + ion_ratio(nu_i, B = B)**2)
    
    return (Ne *  c.elementary_charge / B) * (electron_term - ion_term)




