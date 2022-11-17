import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as const
from datetime import datetime
import pandas as pd
from ionospheric_conductivity import *


def integrated_values(alts, date, glon = 0, 
                      lat_max = 30, 
                      delta = 5):
    

    out = []
    for glat in np.arange(0, lat_max + delta, delta):
        mlat = string_to_list(0, glat, glon, date)[0]
    
        sigma_p = get_profiles(float(glat), glon, date, alts)
        
        sigma_1 = sigma_p.values * (1 + 3 * np.sin(np.radians(mlat))**2)
        
        out.append(sigma_1)
    
    Re = 6.371009e6
    L = 1
    
    integrated = 2*Re*L*(np.sum(np.vstack(out).T, axis = 1))*delta
   
    return sigma_p.index, integrated
   
    
def read_iri(infile):
    iri = pd.read_csv(infile, 
                 delim_whitespace=True, 
                 header = None)
    
    return iri

def read_msise(infile):
    df = pd.read_csv(infile, 
                 delim_whitespace = True, 
                 header = 33, 
                 names = ["height", 
                          "O", 
                          "N2", 
                          "O2", 
                          "mass", 
                          "Tn", 
                          "Tex", 
                          "He", 
                          "Ar", 
                          "H", 
                          "N", 
                          "OAn"])
    
    
    df["nui"] = ion_neutral_collision(df.Tn, df.O, 
                                      df.O2, df.N2)
    
    df["Nn"] = df[[ "O", "N2", "O2"]].sum(axis = 1)
    
    df["nue"] = electron_neutral_collision(df.Tn, df.Nn)
    
    return df


def apex_factor(lat, h, Re = 6378):
    return ((h + Re) / 
            (Re * (1 - np.sin(np.radians(lat))**2)))


delta = 5


apex_heights = np.arange(100, 600, 5)
out_2 = []
for h in apex_heights:
    L = apex_factor(mlat, h, Re = 6378)
    out_1 = []
    for mlat in range(0, 35, 5):
        infile_msise = f"database/msis/mlat_{mlat}.txt"
        msi = read_msise(infile_msise)
        infile_iri = f"database/iri/mlat_{mlat}.txt"
        Ne = read_iri(infile_iri).iloc[:, 1]
    
        sp = Pedersen_conductivity(Ne, msi.nue, msi.nui)
    
        sigma_1 = sp*(1 + 3 * np.sin(np.radians(mlat))**2)

#

        integrated = 2*Re*L*(sigma_1)*delta
    
    out_2 = np.sum(np.vstack(out_1).T, axis = 1)
