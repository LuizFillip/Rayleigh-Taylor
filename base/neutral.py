import numpy as np
from astropy import units as u
from astropy import constants as c
import pandas as pd
from geo.core import run_igrf
from datetime import datetime, timedelta

def nui_1(Tn, O, O2, N2):
    """
    The ion-neutral collisionfrequency
    by Bailey and Balan (1996)
    """
    term_O = (4.45e-11 * O * np.sqrt(Tn * u.K) * 
              (1.04 - 0.067 * np.log10(Tn* u.K))**2)
    
    term_O2 = 6.64e-10 * O2
    term_N2 = 6.82e-10 * N2
        
    return term_O + term_O2 + term_N2

def nui_2(O, O2, N2):
    """
    The ion-neutral collisionfrequency
    by Davies et al. (1997)
    """
    
    u_coeficient = pow(u.m, 3) * pow(u.s, -1)
    u_densities = pow(u.cm, 3)
    
    term_O = 2.44e-16 * u_coeficient * O * u_densities
    term_O2 = 4.28e-16 * u_coeficient * O2 * u_densities
    term_N2 = 4.34e-16 * u_coeficient * N2 * u_densities
    
    return term_N2 + term_O2 + term_O

def effective_wind(zon, 
                   mer, 
                   frac_year,
                   site):
    """
    Effective wind along magnetic field
    """
    d, i = run_igrf(frac_year, site = site)
    D = np.radians(d)
    I = np.radians(i)
    
    return (zon *  np.cos(D) + 
            mer *  np.sin(D)) * np.sin(I) 

def plasma_diffusion(nui):
    """
    Vertical plasma drift due to diffusion 
    """
    u_nu = pow(u.s, -1)
    return c.g0 / nui * u_nu


def recombination(O2, N2):
    """Recombination coefficient"""
    return (4.0e-11 * O2) + (1.3e-12 * N2)    

  
def density(date, df):
    
    return df.loc[(df["date"] == date), "Ne"].values  
    

def rangetime_winds(infile):

    df = pd.read_csv(infile, index_col = "time")
    df.index = pd.to_datetime(df.index)
    
    try:
        del df["Unnamed: 0"]
    except:
        pass
    
    return df
    
def get_wind(date, 
             year = 2014, 
             site = "for"):    
    
    infile = f"database/pyglow/{site}_winds_{year}.txt"


    df = rangetime_winds(infile)
    
    u_wind = u.m / u.s
    
    df = df.loc[(df.index.date == date.date())]
    
    U = effective_wind(df.zon, df.mer, 
                       year, site = "for")
   # U = U.to_frame()
    return U.values * u_wind


date = datetime(2014, 1, 1)

u = get_wind(date)


print(u)

  