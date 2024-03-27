import base as b
import os
import FluxTube as ft
import pandas as pd 
from tqdm import tqdm 
import datetime as dt 

PATH_PRE = "digisonde/data/drift/PRE/"
PATH_FLUXTUBE = "FluxTube/data/reduced/"
PATH_GAMMA = 'database/gamma/'


def add_gammas(df):

    df["drift"] = df["ratio"] * df["K"] * df["vp"]
    
    df["gravity"] = df["ratio"] * df["K"] * (df["ge"] / df["nui"])
        
    df["gamma"] = (
        df["ratio"] * df["K"] * (df["vp"] - df['mer_perp'] + (df["ge"] /df["nui"])))
    return df

def PRE(year, site = 'saa', alt = 300):
    """
    Adding PRE value
    """
    # infile = 'database/pre_2013_2023'
    infile = os.path.join(PATH_PRE, site, f'R{year}.txt')
    ds = b.load(infile)

    ds.rename(
        columns = {"vzp": "vp"}, 
        inplace = True
        )

    f_apex = ft.factor_height(alt) ** 3

    ds["vp"] = ds["vp"] * f_apex
    return ds


def GammaData(
        year = 2013, 
        site = "saa",
        ):
    
    infile = os.path.join(
         PATH_FLUXTUBE, 
         site, 
         f"{year}.txt"
         )
    
    ds = b.load(infile)
    
    try:
        ds = ds.drop(columns = ['alt', 'vzp', 'vp'])
    except:
        pass 
    
    ds = ds.join(PRE(year, site))
    

    return add_gammas(ds)




def concat_years( 
        site = "saa"
        ):
    '''
    Concat all processed files of gamma 
    parameters and save-it
    
    '''
    if site == 'saa':
        end_yr = 2024
    else:
        end_yr = 2022
        
        
    year_list = [GammaData(year, site) for year 
                 in tqdm(range(2013, end_yr), 
                         'join_results')]
    
    df = pd.concat(year_list)
    
    del df['alt']
    
    
    df.to_csv(
        os.path.join(
        PATH_GAMMA, 
        f'p1_{site}.txt')
        )
    
    return df



def load_gamma(site):
    
    infile = os.path.join(
        PATH_GAMMA, 
        f'{site}.txt'
        )
    
    return b.load(infile)

year = 2014
site = 'saa'


# # concat_years(site = "saa")
# infile = os.path.join(
# PATH_GAMMA, 
# f'p1_{site}.txt')


# df = b.load(infile)

# df['gamma'].plot()

