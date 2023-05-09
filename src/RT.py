import numpy as np


def generalized_rate_growth(nu, L, R, Vp, U):
    """
    Generalized instability rate growth
    local version
    Paramaters:
    ---------- 
    Vp: Prereversal Enhancement (PRE)
    U: Neutral wind (effective)
    nu: ion-neutral collisional frequency
    L: electron density gradient scale
    R: Recombination rate
    g: acceleration due gravity
    """
     
    return (Vp - U + (9.81 / nu))*L - R



class GrowthRate:
    
    def __init__(self, ne):
        
        self.ne = ne
        
    def wind():
        ...
    
    def vzp():
        ...
    
    def g():
        ...
    
    def nui():
        ...
        
        
class LabelsRT:
    
    @property
    def complete():
        return  r"$(V_{zp} - U + \frac{g}{\nu_{in}})\frac{1}{n_e} \frac{\partial n_e}{\partial y} - R$"
    
    @property
    def wind():
        return r"$(V_{zp} + \frac{g}{\nu_{in}})\frac{1}{n_e} \frac{\partial n_e}{\partial y}$"
    
    @property
    def vzp():
        return r"$(V_{zp} + \frac{g}{\nu_{in}})\frac{1}{n_e} \frac{\partial n_e}{\partial y} - R$"
    
    @property
    def recombination():
        return r"$(V_{zp} - U + \frac{g}{\nu_{in}})\frac{1}{n_e} \frac{\partial n_e}{\partial y}$"
    
    @property
    def gravity():
        return r"$ (\frac{g}{\nu_{in}})\frac{1}{n_e} \frac{\partial n_e}{\partial y}$"
        

 names = [r"$(V_{zp} - U + \frac{g}{\nu_{in}})\frac{1}{n_e} \frac{\partial n_e}{\partial y} - R$",
            r"$(V_{zp} + \frac{g}{\nu_{in}})\frac{1}{n_e} \frac{\partial n_e}{\partial y}$", 
            r"$(- U + \frac{g}{\nu_{in}})\frac{1}{n_e} \frac{\partial n_e}{\partial y}$ - R", 
            r"$(V_{zp} - U + \frac{g}{\nu_{in}})\frac{1}{n_e} \frac{\partial n_e}{\partial y}$", 
            r"$(V_{zp} + \frac{g}{\nu_{in}})\frac{1}{n_e} \frac{\partial n_e}{\partial y} - R$", ]
  