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
            label = f"Efetivo ({hem})"
        else:
            label = f"Geográfico ({hem})"
        
        ax.plot(gamma * 1e4, label = label)
        
    
    ax.text(0.05, 0.85, coord, transform = ax.transAxes)
    
    ax.axhline(0, linestyle = "--")
        
    ax.set(ylim = [-20, 20], 
           xlim = [ds.index[0], 
                   ds.index[-1]]
           )
    return ax


def plot_all_effects(df, recom, drift = "vz"):


    fig, ax = plt.subplots(
           figsize = (14, 12), 
           sharex = True,
           sharey = "row",
           ncols = 2, 
           nrows = 3, 
           dpi = 300
        )
    
    plt.subplots_adjust(
        hspace= 0.1, 
        wspace = 0.1
        )
    
    eq = rt.EquationsFT()
    
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
                              drift = drift
                              )
                
                title = eq.complete(
                    wind_sign = sign, 
                    recom = recom
                    )
                
                ax[0, col].set(title = title)

    plot_roti(ax[2, 0], ds)
    plot_roti(ax[2, 1], ds)
    
    ax[0, 0].legend(
        ncol= 4, 
        bbox_to_anchor = (1., 1.35),
        loc = "upper center")
    
    ax[2, 1].set(ylabel = "")
    
    for ax in ax.flat:
        plot_terminators(ax, ds)
        
    if recom:
        r = "com"
    else:
        r = "sem"
        
    fig.suptitle(f"$V_P = ${drift} e {r} efeitos de recombinação")

    return fig



def save(
        drift = "vz", recom = False
        ):
    
    if recom:
        w = "with"
    else:
        w = "without"
    
    save_in = f"D:\\plots\\neutral_winds_and_{drift}_{w}_rec"
        
    infile = "database/RayleighTaylor/reduced/300km.txt"
    df = rt.load_process(infile, apex = 300)
    
    for ds in rt.separeting_times(df):
        
        name_to_save = fname_to_save(ds)
        
        print(name_to_save)
        fig = plot_all_effects(ds, recom, drift = drift)
        
        save_it = os.path.join(save_in, name_to_save )
        save_but_not_show(fig, save_it)
                
     
     
# for vz in ["vz", "vzp"]:
    # vz = "vz"
    # for rc in [True, False]:
    #     save(drift = vz, recom = rc)


infile = "database/RayleighTaylor/reduced/300km.txt"
df = rt.load_process(infile, apex = 300)
 
ds = rt.separeting_times(df)[0]
drift = "vz"
recom = True
fig = plot_all_effects(ds, recom, drift = drift)

plt.show()

"Efeitos dos ventos neutros e de Vz (variando no tempo)"