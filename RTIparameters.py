import numpy as np 
import pandas as pd
from common import float_to_time



class PRE(object):
    
    def __init__(self, infile):
    
        df = pd.read_csv(infile, index_col = 0)
    
        df = df.dropna()
    
        time = df["time"].apply(lambda x: float_to_time(x))
        df.index = pd.to_datetime(df.index + " " + time)
        
        self.df = df
        self.pre = self.df["vz"].values
        self.times = self.df.index
        

class neutrals(object):
    
    def __init__(self, TN, O, O2, N2):
        self.tn = TN
        self.o = O
        self.o2 = O2
        self.n2 = N2

    @property
    def collision(self):
        """Collision frequency from Bailey and Balan 1992"""
        nu_o = (4.45e-11 * self.o * np.sqrt(self.tn) * 
               (1.04 - 0.067 * np.log10(self.tn)) ** 2.0)
        
        nu_o2 = (6.64e-10 * self.o2)
        
        nu_n2 = 6.82e-10 * self.n2
        
        return  nu_o + nu_o2 + nu_n2
    
    @property
    def recombination(self):
        
        return (4.0e-11  * self.o2) + (1.3e-12   * self.n2)    
  
def scale_gradient(Ne, dz = 1):
    """length scale gradiendt : Vertical variation of density"""
    factor = 1e-3 #convert km to meters
    return np.gradient(np.log(Ne), dz)*factor





