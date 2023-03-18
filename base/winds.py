import numpy as np 
from GEO.core import run_igrf
import pandas as pd

d, i = run_igrf(year = 2013, site = "saa")

class effective_wind(object):
    
    """
    Effective wind along magnetic field
    
    Pag. 27 e 28 (Tese Ely, 2016)
    
    U_theta (mer) = meridional component (positiva para sul)
    U_phi (zon) = zonal component (positiva para leste)
    
    """
    
    @staticmethod
    def eff_zonal(zon, mer, d): 
        D = np.radians(d)
        # positiva para leste
        return (zon * np.cos(D) + mer * np.sin(D))
    
    @staticmethod
    def eff_meridional(zon, mer, d, i):
        D = np.radians(d)
        I = np.radians(i)
        # Ueff_x (positiva para sul)
        return (
            mer * np.cos(D) - zon * np.sin(D)
                ) * np.cos(I)

    
winds = effective_wind()



