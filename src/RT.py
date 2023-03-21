from RayleighTaylor.core import (run_msise, 
                                 load_iri)
from RayleighTaylor.base.neutral import R, nui_1
from RayleighTaylor.base.iono import scale_gradient



def growth_rate_RT(nu, L, R, Vp, U):
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


def df_parameters(date):
    
    n = run_msise(date) 
    
    n["R"] = R(n.O2, n.N2)
     
    n["nu"] = nui_1(n.Tn, n.O, 
                    n.O2, n.N2)
    
    iri = load_iri(date)
    
    n["L"] = scale_gradient(iri["Ne"], dz = 1)
    
    n.drop(columns = 
           ["O", "N2", "Tn", "O2"], 
           inplace = True) 
    
    n["u"] = load_fpi(date)
    #n["vz"] = load_drift(date)
    
    n["g"] = growth_rate_RT(n.nu, n.L, n.R, 
                            n.vz, n.u)
    
    n["date"] = date.date()
    return n