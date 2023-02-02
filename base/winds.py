import numpy as np 

    
def general_vz(vz, uy, wd, i):
    """
    A general expression for vertical plasma drift including
    the effect from meridional wind and plasma diffusion
    """
    I = np.radians(i)
    
    vz_term = vz * np.cos(I)
    uy_term = uy * np.cos(I)* np.sin(I)
    wd_term = wd * pow(np.sin(I), 2)
    
    return vz_term + uy_term - wd_term 


