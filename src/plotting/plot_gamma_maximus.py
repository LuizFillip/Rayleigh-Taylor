# -*- coding: utf-8 -*-
"""
Created on Fri May 12 00:04:41 2023

@author: Luiz
"""

def plot_maximus_altime(ts):
    
    fig, ax = plt.subplots(
        figsize = (12, 4), dpi = 300)
    
    g = "gamma_g"
    img = plt.scatter(ts.index, 
                      ts[f"z_{g}"], 
                      c = ts[g]*1e4)
    
    
    cb = plt.colorbar(img)
    cb.set_label("$\gamma_{FT} ~(\\times 10^{-4}~s^{-1})$")
    
    
    s.format_axes_date(
        ax, time_scale = "hour", interval = 4
        )
    
    
    ax.set(title = "gravidade", ylabel = "Altura de Apex (km)")
    
    
    ax.set_xlabel("Hora universal", 
                     rotation = 0, 
                     labelpad = 25)