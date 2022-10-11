import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as const
from datetime import datetime
import pandas as pd
from ionospheric_conductivity import *

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
    
    df["Nn"] = df[["He", "O", "N2", 
                   "O2", "Ar", "H", "N"]].sum(axis = 1)
    
    df["nue"] = electron_neutral_collision(df.Tn, df.Nn)
    
    return df


mlat = 0

out = []
for mlat in range(0, 35, 5):
    infile_msise = f"database/msis/mlat_{mlat}.txt"
    msi = read_msise(infile_msise)
    
    
    infile_iri = f"database/iri/mlat_{mlat}.txt"
    Ne = read_iri(infile_iri).iloc[:, 1]
    
    sp = Pedersen_conductivity(Ne, msi.nue, msi.nui)
    
    sigma_1 = sp*(1 + 3 * np.sin(mlat)**2)
    
    out.append(sigma_1)

Re = 6.371009e3
L = 1
delta = 5
integrated = 2*Re*L*(np.sum(np.vstack(out).T, 
                            axis = 1))*delta
plt.plot(integrated, msi.height)
plt.xscale("log")
plt.ylim([150, 600])