import pandas as pd
import numpy as np
from nrlmsise00 import msise_flat
from PlanetaryIndices.core import get_indices
import datetime as dt
from RayleighTaylor.base.neutral import R, nui_1, eff_wind
from RayleighTaylor.base.iono import scale_gradient
from build import paths as p


def growth_rate_RT(nu, L, R, Vp, U):
    """
    Generalized instability rate growth
    local version
    Paramaters:
    ---------- s
    Vp: Prereversal Enhancement (PRE)
    U: Neutral wind (effective)
    nu: ion-neutral collisional frequency
    L: electron density gradient scale
    R: Recombination rate
    g: acceleration due gravity
    """
     
    return (Vp - U + (9.81 / nu))*L - R

coords = {"car": (-7.38, -36.528), 
          "for": (-3.73, -38.522), 
          "saa": (-2.53, -44.296)}

def load_iri(date):
    infile = p("IRI").files
    
    df = pd.read_csv(infile, index_col = 0)
    
    df.index = pd.to_datetime(df.index)
    
    return df.loc[df.index == date]


def load_fpi(date):
    fpi = p("FabryPerot").get_files_in_dir("processed")
    
    df = pd.read_csv(fpi, index_col = 0)
    
    df.index = pd.to_datetime(df.index)
    
    df["u"] = eff_wind(df.zon, 
                       df.mer, 
                       year = 2013, 
                       site = "saa").Nogueira
    
    df["u"].plot()
    
    return df.loc[df.index == date, "u"].item()
    
def run_msise(datetime, 
          hmin = 200, 
          hmax = 500, 
          step = 1, 
          site = "saa"):
    
    glat, glon = coords[site]
    
    """Running models MSISE00"""
    
    alts = np.arange(hmin, hmax + step, step)
     
    t = get_indices(datetime.date())
    
    res = msise_flat(datetime, alts[None, :], 
                     glat, glon, 
                     t.get("F10.7a"), 
                     t.get("F10.7obs"), 
                     t.get("Ap"))
    
    columns = ["He", "O", "N2", "O2", "Ar", 
              "mass", "H", "N", "AnO", "Tex", "Tn"]
    
    df = pd.DataFrame(res[0], index = alts, 
                      columns = columns)
    
    df.drop(["He", "Ar", 
             "mass", "H", "N", "AnO", "Tex"], 
            axis = 1, 
            inplace = True)
    
    return df


date = dt.datetime(2013, 1, 1, 21)

n = run_msise(date) 

n["R"] = R(n.O2, n.N2)
 
n["nu"] = nui_1(n.Tn, n.O, 
                n.O2, n.N2)

iri = load_iri(date)

n["L"] = scale_gradient(iri["Ne"], dz = 1)

n.drop(columns = [ "O", "N2", "O2"], 
       inplace = True) 


u = load_fpi(date)

print(u)
