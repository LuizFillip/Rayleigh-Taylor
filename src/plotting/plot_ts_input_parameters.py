import os
from common import plot_times_axes
import numpy as np
import matplotlib.pyplot as plt
import settings as s
from labels import Labels
from utils import save_but_not_show, translate
import pandas as pd
from matplotlib.colors import Normalize
import matplotlib.cm as cm


def separeting_times2(df, col = "dn", freq = "5D"):
    times = df[col].values

    ts = pd.date_range(
          min(times), 
          max(times), 
          freq = freq
          )
    def remove_lowers(ds):
        return [i for i in ds if len(i) > 10]
    
    sep_data = [df.loc[(df[col] >= ts[i]) & 
                       (df[col] <= ts[i + 1])]
                for i in range(len(ts) - 1)]
    
    return remove_lowers(sep_data)

def raw_data(infile):
    out = []
    for filename in os.listdir(infile):
        df = pd.read_csv(
            infile + filename, index_col = 0
            )
        df["dn"] = pd.to_datetime(df["dn"])
        month = filename.replace(".txt", "")
        
        if int(month) <= 6:
            out.append(df)
            
    return pd.concat(out)


def limits_wind(ds, cols):

    vmin = min([ds[col].min() for col in cols])
    vmax = max([ds[col].max() for col in cols])

    return vmin, vmax


def limits_iono(ds, cols):
    dic = {}
    
    for col in cols:
        dic[col] = (ds[col].min(), ds[col].max())
        
    return dic


def plot(ax, ts, vmin, vmax, parameter = "zon"):
    
    pt = pd.pivot_table(
         ts, 
         values = parameter, 
         columns = "dn", 
         index = ts.index
         )
    cmap = "rainbow"
    
    img = ax.contourf(
        pt.columns, pt.index, pt.values, 30,
        norm = plt.Normalize(vmin=vmin, vmax = vmax),
        cmap = cmap
       )
    
    cb = plt.colorbar(
        cm.ScalarMappable(
        norm = Normalize(vmin, vmax), 
        cmap = cmap), ax = ax)
    
    lbs  = Labels().infos[parameter]
    name = lbs["name"].replace("\n", " ")
    
    if parameter == "ratio":
        label = lbs["symbol"] 
    else:
        label = f"{lbs['symbol']} ({lbs['units']})"
    cb.set_label(label)
    
    ax.set(title = f"{name}")
    
    return img

def set_figure(ncols = 2, nrows = 2):
    fig, ax = plt.subplots(
        dpi = 300,
        figsize = (15, 8),
        ncols = ncols,
        nrows = nrows,
        sharex = True,
        sharey = True
        )
    
    plt.subplots_adjust(
        hspace = 0.1, 
        wspace = 0.1
        )
    
    return fig, ax
    
def plot_winds(
        ts, vmin, vmax, cols, cmap = "rainbow"
        ):
   
    fig, ax = set_figure()
    
    cols = ["zon", "zon_ef", "mer", "mer_ef"]
 
    for i in range(2):
        ax[i, 0].set(ylabel = "Altura de Apex (km)")
    
    for col, axs in zip(cols, ax.flat):
            
        pt = pd.pivot_table(
             ts, 
             values = col, 
             columns = "dn", 
             index = ts.index
             )
        
        ax.contourf(
            pt.columns, pt.index, pt.values, 30,
            norm = plt.Normalize(
                vmin = vmin, vmax = vmax),
            cmap = cmap
           )
        
        
        axs.axhline(300, linestyle = "--")
        
        if "mer" in col:
            plot_times_axes(axs)
            plot_times_axes(axs)
        
    im = cm.ScalarMappable(
        norm = Normalize(vmin, vmax), 
        cmap = cmap
        )
    cb = fig.colorbar(im, ax = ax.flat)
    
    cb.set_label("Velocidade (m/s)")
    
    return fig

def plot_iono(ds, ts, dix):

    cols = ["N", "K", "nui", "ratio"]
    
    fig, ax = set_figure()
    
    for i in range(2):
        
        ax[i, 0].set(
            xlim = [ts["dn"].values[0], 
                    ts["dn"].values[-1]],
            ylabel = "Altura de apex (km)")
        
        plot_times_axes(ax[1, i])
        
    for num, ax in enumerate(ax.flat):
        col = cols[num]
        vmin, vmax = dix[col]
        plot(ax, ts, vmin, vmax, 
             parameter = col
             )
        
    return fig
        


def save(infile, hem, save_in, cols):

    ds = raw_data(infile)
    
    if "zon" not in cols:
        dix = limits_iono(ds, cols)
    else:
        vmin, vmax =  limits_wind(ds, cols)
    
    ds = ds.loc[(ds.index <= 500) & 
                (ds["hem"] == hem)]
    
    for ts in separeting_times2(ds, col = "dn"):
            
        dn = pd.to_datetime(ts["dn"].values[0])
        
        print("saving...", dn)
        
        month_name = dn.strftime("%m")
        try:
            if "zon" in cols:
                fname = f"w{dn.strftime('%Y%m%d%H%M')}_{hem}.png"
                fig = plot_winds(
                    ts, vmin, vmax, cols
                    )
            else:
                fname = f"p{dn.strftime('%Y%m%d%H%M')}_{hem}.png"
            
                fig = plot_iono(ds, ts, dix )
            
            fig.suptitle(translate(hem).title())
            save_it = os.path.join(
                save_in, 
                month_name, 
                fname
                )
            save_but_not_show(fig, save_it)
        except:
            print(dn)
            continue
        
      
        

infile = "database/RayleighTaylor/process/"
save_in = "D:\\plots\\parameters\\"



hem = "south"
cols = ["N", "K", "nui", "ratio"]

save(infile, hem, save_in, cols)


