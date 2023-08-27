import pandas as pd

def gammas_locals(df):
    
    """
    local Generalized instability rate growth
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
    
    

    ds = pd.DataFrame()
    
    ds['vz'] = df["L"] * df['vp'] - df['R']
    ds['g'] =  df["L"] * (9.81 / df['nui']) - df['R']
    ds['u_perp'] = df["L"] * df['mer_perp'] - df['R']
    ds['u_parl'] = df["L"] * df['mer_parl'] - df['R']
    ds['all_perp'] = df["L"] * (df['vp'] - df['mer_perp'] +
                           (9.81 / df['nui'])) - df['R']
    
    ds['all_parl'] = df["L"] * (df['vp'] - df['mer_parl'] +
                           (9.81 / df['nui'])) - df['R']
    
    return ds * 1e4




def gammas_integrated(
        df, 
        factor = True,
        ):
    
    """
    Generalized instability rate growth
    Magnetic field Integrated version
    Paramaters:
    ---------- 
    Vp: Prereversal Enhancement (PRE)
    mer_perp: Neutral wind (effective)
    nui: ion-neutral collisional frequency
    K: electron density gradient scale for regionF
    R: Recombination rate
    ge: acceleration due gravity
    """

    ds = pd.DataFrame()
  
    ds['parl_mer'] = df['mer_parl'].copy()
    ds['R'] = df['R'].copy()
    
    
    ds['drift'] = df['ratio'] * df['K'] * df['vp'] 
    
    ds['gravity'] = df['ratio'] * df['K'] * (df['ge'] / df["nui"]) 
        
    ds['winds'] = df['ratio'] * df['K'] * (-df['mer_perp']) 
    
    ds['all'] =  df['ratio'] * df['K'] * (
        df['vp'] - df['mer_perp'] + (df['ge'] / df["nui"])
        ) 

    return ds
        
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
        recom = False
        ):
    
    gamma = ds["ratio"] * (
        - ds[wind] + (ds["ge"] / ds["nui"])) * ds["K"] 
    
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
        


