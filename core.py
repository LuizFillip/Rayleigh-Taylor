import datetime as dt
from common import get_wind, get_pre, get_ne, run_msise
from base.neutral import eff_wind, recombination, nui_1
from base.iono import scale_gradient

def growth_rate_RT(nu, L, R, Vp, U):
    """
    Generalized instability rate growth
    Paramaters:
    ---------- 
    Vp: Prereversal Enhancement (PRE)
    U: Neutral wind
    nu: ion-neutral collisional frequency
    L: gradient scale
    R: Recombination rate
    
    """
     
    return (Vp - U + (9.81 / nu))*L - R


def compute(date_time, func_wind = "Nogueira"):
    
    U = get_wind(date_time, 
                 func_wind=func_wind).U
    
    vzp = get_pre(date_time.date())  
    n = run_msise(date_time, hmin = 200, hmax = 500)
    R = recombination(n.O2, n.N2)

    nu = nui_1(n.Tn, n.O, n.O2, n.N2)

    ne = get_ne(date_time)
    
    l = scale_gradient(ne, dz = 1)
        
    return growth_rate_RT(nu.values, l, 
                          R.values, vzp, 
                          U.values)


date_time = dt.datetime(2014, 1, 1, 21, 10)
gamma = compute(date_time)

print(gamma)
