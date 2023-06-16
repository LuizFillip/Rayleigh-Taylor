def generalized_rate_growth(nui, L, R, Vp, U):
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
     
    return (Vp - U + (9.81 / nui))*L - R


        
def effects_due_to_gravity(
        ds, 
        recom = False
        ):
    
    gamma = ds["ratio"] * (ds["ge"] / ds["nui"]) * ds["K"]
    
    if recom:
        return gamma - ds["R"]
    else:
        return gamma

def effects_due_to_winds(
        ds, 
        wind = "zon",
        sign_wd = -1, 
        recom = False
        ):
    
    gamma = ds["ratio"] * (
        sign_wd * ds[wind] + (ds["ge"] / ds["nui"])) * ds["K"] 
    
    if recom:
        return gamma - ds["R"]
    else:
        return gamma 


def all_effects(
        ds, 
        wind = "zon",
        sign_wd = -1, 
        drift = "vz", 
        recom = False
        ):
    
    gamma = ds["ratio"] * (ds[drift] +
        sign_wd * ds[wind] + (ds["ge"] / ds["nui"])
        ) * ds["K"]
    
    if recom:
        return gamma - ds["R"]
    else:
        return gamma
    
    
def effects_due_to_drift(
        ds, 
        col = "vz",
        recom = False
        ):
    
    gamma = ds["ratio"] * (
        ds[col] + (ds["ge"] / ds["nui"])
        ) * ds["K"]
    
    if recom:
        return gamma - ds["R"]
    else:
        return gamma 
        



