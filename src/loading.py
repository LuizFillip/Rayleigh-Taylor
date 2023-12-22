# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 09:19:13 2023

@author: Luiz
"""

import base as b 
import os
import GEO as gg 
import datetime as dt
import pandas as pd 


PATH_GAMMA = 'database/Results/gamma/'
PATH_RESULT ='database/Results/concat/'

def load_grt(
        site = 'saa', 
        hour = 22, 
        minute = 0
        ):

    path = os.path.join(
       PATH_RESULT,
       f'{site}.txt'
       )
    df = b.load(path)
    
    sel_time = dt.time(hour, minute)
    
    df = df.loc[df.index.time == sel_time]
    
    df.columns.name = gg.sites[site]['name']
    
    df.index = pd.to_datetime(df.index.date)
    
    return df.interpolate()


def parameters(
        site = 'saa',
        col = 'e_f'
        ):
    
    path = os.path.join(
       PATH_GAMMA,
       f'p_{site}.txt'
       )
    
    df = b.load(path)
    df = df.loc[df['period'] == col]
    
    df.columns.name = gg.sites[site]['name']
    
    return df.interpolate()