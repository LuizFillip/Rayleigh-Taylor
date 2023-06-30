import pandas as pd
import models as mm

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

def gammas_locals(df):

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

def gammas_integrated(df, rc = False):

    ds = pd.DataFrame()
    
    ds['vz'] =  df['ratio'] * df['K'] * df['vzp'] 
    
    ds['g'] =  df['ratio'] * df['K'] * (df['ge'] / df["nui"]) 
    
    ds['u_parl'] =  df['ratio'] * df['K'] * (-df['mer_parl']) 
    
    ds['u_perp'] =  df['ratio'] * df['K'] * (-df['mer_perp']) 
    
    ds['all_parl'] = df['ratio'] * df['K'] * (
        df['vzp'] - df['mer_parl'] + (df['ge'] / df["nui"])
        ) 
    
    ds['all_perp'] = df['ratio'] * df['K'] * (
        df['vzp'] - df['mer_perp'] + (df['ge'] / df["nui"])
        ) 
    
    if rc:
        for col in ds.columns:
            ds[col] = ds[col] - df['R']
            
    for col in ds.columns:
        
        ds[col] = mm.correct_and_smooth(
            ds[col], threshold = 0.5
            )

    return ds * 1e4
        
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
        



