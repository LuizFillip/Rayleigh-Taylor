import matplotlib.pyplot as plt
from utils import translate
import RayleighTaylor as rt
import os
from common import plot_roti, plot_terminators
from utils import save_but_not_show, fname_to_save



def plot_gamma(
        ax, 
        ds, 
        cols, 
        sign = -1, 
        recom = False,
        hem = "north",
        drift = "vz"
        ):
    
    hem = translate(hem)
    
    if "zon" in cols:
        coord =  "Zonal"
    else:
        coord = "Meridional"

    for wd in cols:
                    
        gamma = rt.all_effects(
                ds, 
                wind = wd,
                drift = drift, 
                sign_wd = sign, 
                recom = recom)
      
        if "ef" in wd:
            label = f"efetivo ({hem})"
        else:
            label = f"Geográfico ({hem})"
        
        ax.plot(gamma * 1e4, label = label)
        
    ax.legend(ncol= 2, loc = "lower left")
    ax.text(0.05, 0.85, coord, transform = ax.transAxes)
    
    ax.axhline(0, linestyle = "--")
        
    ax.set(ylim = [-20, 20], 
           xlim = [ds.index[0], 
                   ds.index[-1]]
           )
    return ax


def plot_all_effects(infile, alt, recom, drift = "vz"):


    fig, ax = plt.subplots(
           figsize = (20, 12), 
           sharex = True,
           sharey = "row",
           ncols = 2, 
           nrows = 3, 
        )
    
    plt.subplots_adjust(
        hspace= 0.1, 
        wspace = 0.1)
    

    eq = rt.EquationsFT()
    
    df = rt.set_data(infile, alt = alt)
    
    for hem in ["north", "south"]:
        
        ds = df.loc[df["hem"] == hem]
        
        for row, wd in enumerate(["zon", "mer"]):
        
            cols = [wd, f"{wd}_ef"]
            
            ax[row, 0].set_ylabel(eq.label)
            
            for col, sign in enumerate([1, -1]):
                
                plot_gamma(ax[row, col], ds, cols, 
                              sign = sign, 
                              recom = recom, 
                              hem = hem, 
                              drift=drift)
                
                title = eq.complete(
                    wind_sign = sign, 
                    recom = recom
                    )
                
                ax[0, col].set(title = title)
    
    
    
    plot_roti(ax[2, 0], ds)
    plot_roti(ax[2, 1], ds)
    
    ax[2, 1].set(ylabel = "")
    
    for ax in ax.flat:
        plot_terminators(ax, ds)
        
    if drift == "vz":
        fig.suptitle("Assumindo $V_P = V_z$ (variando no tempo)")
    else:
        fig.suptitle("Assumindo $V_P = V_{zp}$ (Pico pré reversão)")

    return fig, fname_to_save(ds)



def save(
        drift = "vz", recom = False, alt = 300
        ):
    
    if recom:
        w = "with_recombination"
    else:
        w = "without_recombination"
    
    save_in = f"D:\\plots\\all_effect_{w}\\{drift}\\"
    
    path = "database/RayleighTaylor/process3/"
    
    for filename in os.listdir(path):
    
        infile = os.path.join(path, filename) 
        
        recom = True
        
        print("saving...", filename)
        
        fig, fname = plot_all_effects(infile, alt, recom, drift = drift)
    
        save_but_not_show(
                fig, 
                os.path.join(save_in, fname)
                )
     
for vz in ["vz", "vzp"]:
    for rc in [True, False]:
        save(drift = vz, recom  = rc)