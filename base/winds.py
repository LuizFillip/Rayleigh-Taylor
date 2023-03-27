import numpy as np 

class effective_wind(object):
    
    """
    Effective wind along and perpendicular of 
    magnetic field
    
    Pag. 27 e 28 (Tese Ely, 2016)
    
    U_theta (mer) = meridional component (positiva para sul)
    U_phi (zon) = zonal component (positiva para leste)
    
    """
    
    @staticmethod
    def eff_zonal(zon, mer, D): 
        D = np.deg2rad(D)
        # Ueff_y (positiva para leste)
        return (zon * np.cos(D) + mer * np.sin(D))
    
    @staticmethod
    def eff_meridional(zon, mer, D, I):
        D = np.deg2rad(D)
        I = np.deg2rad(I)
        # Ueff_x (positiva para sul)
        return (
            mer * np.cos(D) + zon * np.sin(D)
                ) * np.cos(I)


