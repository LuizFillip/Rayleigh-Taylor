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




        
def effects_due_to_gravity(ds):
    
    return  ds["ratio"] * ((9.81 / ds["nui"])) * ds["K"]

def effects_due_to_winds(
        ds, 
        wind = "zon",
        sign = -1):
    
    return ds["ratio"] * (sign * ds[wind] + (9.81 / ds["nui"])
        ) * ds["K"] 


def effects_due_to_recombination(
        ds, 
        wind = "zon",
        sign = -1):
    
    return ds["ratio"] * (
        sign * ds[wind] + (9.81 / ds["nui"])
        ) * ds["K"] - ds["RT"]

def effects_due_to_drift(
        ds, 
        recom = False, 
        col = "vz"
        ):
    
    if recom:
        return ds["ratio"] * (ds[col] + (9.81 / ds["nui"])) * ds["K"] - ds["RT"]
    
    else:
        return ds["ratio"] * (ds[col] + (9.81 / ds["nui"])) * ds["K"] 
        


