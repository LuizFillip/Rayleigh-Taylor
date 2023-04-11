import pandas as pd
import numpy as np
import datetime as dt
from build import paths as p

 


def load_IRI(date):
    infile = p("IRI").files
    
    df = pd.read_csv(infile, index_col = 0)
    
    df.index = pd.to_datetime(df.index)
    
    return df.loc[df.index == date]


def load_FPI(date):
    fpi = p("FabryPerot").get_files_in_dir("processed")
    
    df = pd.read_csv(fpi, index_col = 0)
    
    df.index = pd.to_datetime(df.index)
      
    return df.loc[df.index == date, "u"].item()




    




