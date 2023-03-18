import numpy as np
from astropy import units as u
from GEO.core import run_igrf

def nui_1(Tn, O, O2, N2):
    """
    The ion-neutral collision frequency
    by Bailey and Balan (1996)
    """
    term_O = (4.45e-11 * O * np.sqrt(Tn) * 
              (1.04 - 0.067 * np.log10(Tn))**2)
    
    term_O2 = 6.64e-10 * O2
    term_N2 = 6.82e-10 * N2
        
    return term_O + term_O2 + term_N2

def nui_2(O, O2, N2):
    """
    The ion-neutral collision frequency
    by Davies et al. (1997)
    """
    
    u_coeficient = pow(u.m, 3) * pow(u.s, -1)
    u_densities = pow(u.cm, 3)
    
    term_O = 2.44e-16 * u_coeficient * O * u_densities
    term_O2 = 4.28e-16 * u_coeficient * O2 * u_densities
    term_N2 = 4.34e-16 * u_coeficient * N2 * u_densities
    
    return term_N2 + term_O2 + term_O

def nu_3(O, Tn, Ti):
    """
    The ion-neutral collision frequency
    by Schunk and Nagy, 2000

    Parameters
    ----------
    O :  float array
        Molecular oxygen concentration
    Tn : float array
        neutral temperature
    Ti : float array
        ion temperature
    """
    Tr = (Ti + Tn) / 2
    return 3.7e-11 * O * np.sqrt(Tr) * (1 - 0.064 * np.log10(Tr))**2


def plasma_diffusion(nui):
    """
    Vertical plasma drift due to diffusion 
    """
    return 9.80 / nui


def R(O2, N2):
    """Recombination coefficient"""
    return (4.0e-11 * O2) + (1.3e-12 * N2)    

    

def neutral_constituintes(
        tn, 
        o_point, 
        o2_point, 
        n2_point, 
        step,  
        base_height = 200.0 
        ):
    

    CO = np.zeros(len(tn))
    CO2 = np.zeros(len(tn))                
    CN2 = np.zeros(len(tn))                

    
    for i in range(0, len(tn)):
        
        Z1 = base_height + step * i
        
        GR = 1.0 / pow(1.0 + Z1 / 6370.0, 2)
        
        HO = 0.0528 * tn[i] / GR                               # scale height of O [km]
        HO2 = 0.0264 * tn[i] / GR                              # scale height of O2 [km]
        HN2 = 0.0302 * tn[i] / GR                              # scale height of N2 [km]

        p_co = o_point / 5.33 * 8.55
        p_co2 = o2_point / 1.67 * 4.44
        p_cn2 = n2_point / 9.67 * 2.26

        CO[i] = p_co * np.exp(-(Z1 - 335.0) / HO)           # atomic oxygen [cm-3]
        CO2[i] = p_co2 * np.exp(-(Z1 - 335.0) / HO2)        # molecular oxygen [cm-3]
        CN2[i] = p_cn2 * np.exp(-(Z1 - 335.0) / HN2) 
    
    return CO, CO2, CN2


  