import pandas as pd
import digisonde as dg


def gamma_forms(df, dn, wind = "mer_perp"):
    
    vz = dg.add_vzp()
    vzp = vz[vz.index == dn.date()]["vzp"].item()
    
    try:
        gammas = [
            df["L"] * ( 9.81 / df["nui"]), 
            df["L"] * (-df[wind]), 
            df["L"] * (vzp),
            df['L'] * (vzp - df[wind] + 
                      (9.81 / df["nui"]))
                  ] 
    except:
        gammas = [
            df['ratio'] * df['K'] * (
                df['ge'] / df["nui"]), 
            df['ratio'] * df['K'] * (-df[wind]), 
            df['ratio'] * df['K'] * (vzp),
            df['ratio'] * df['K'] * (vzp - df[wind] + 
                      (df['ge'] / df["nui"]))
                  ] 
    
    gm = pd.concat(gammas, axis = 1).dropna()
        
    gm.columns = [
        'gravity', 
        'wind', 
        'drift', 
        'all']
    
    return gm * 1e4



