from utils import translate
import matplotlib.pyplot as plt
import RayleighTaylor as rt
from utils import save_but_not_show, fname_to_save, make_dir
import os
from common import plot_roti, plot_terminators


def plot_gravity_effect(df):
    
    fig, ax = plt.subplots(
        figsize = (15, 6), 
        sharex = True,
        sharey = "row",
        ncols = 2, 
        nrows = 2, 
        dpi = 300
        )
    
    plt.subplots_adjust(
        hspace = 0.1, 
        wspace = 0.1
        )
    
    eq = rt.EquationsFT()
    
    for col, hem in enumerate(["north", "south"]):
        
        ds = df.loc[df["hem"] == hem]

        plot_roti(ax[1, col], ds)
        
       
        for recom in [True, False]:
            
            gamma = rt.effects_due_to_gravity(
                ds, recom = recom)
            
            ax[0, col].plot(
                gamma * 1e4, 
                label = eq.gravity(recom = recom) 
                        )
        
        ax[0, col].axhline(0, linestyle = "--")
    
        ax[0, col].set(ylim = [-20, 20], 
                     ylabel = eq.label, 
                     title = translate(hem).title()) 
           
    ax[0, 0].legend(
        loc = "upper center",
        ncols = 2, 
        bbox_to_anchor = (1., 1.4)
        )
    
    ax[1, 1].set(ylabel = '')
    ax[0, 1].set(ylabel = '')
    
    for ax in ax.flat:
        plot_terminators(ax, ds)
        
    return fig
    

def save():
    save_in =  "D:\\plots\\gravity\\"
    
    infile = "database/RayleighTaylor/reduced/300km.txt"
    
    df = rt.load_process(infile, apex = 300)
    
    for ds in rt.separeting_times(df):
            
        fig = plot_gravity_effect(ds)
        

        dn = ds.index[0]
        print("saving...", dn)
        month_name = dn.strftime("%m")
        
        save_it = os.path.join(
            save_in, 
            month_name, 
            fname_to_save(ds)
            )
        save_but_not_show(fig, save_it)
                
# infile = "database/RayleighTaylor/reduced/300km.txt"
# df = rt.load_process(infile, apex = 300)
# ds = rt.separeting_times(df)[0]
# fig = plot_gravity_effect(ds)
# plt.show()



def create_months_folders():
    import pandas as pd
    
    ts = pd.date_range("2013-1-1", "2013-12-31", freq = "1M")
    infile = "D:\\plots\\total"
    #for folder in os.listdir(infile):
      
    for dn in ts:
        month_name = dn.strftime("%m")
        
        make_dir(
            os.path.join(infile, month_name)
            )
    
#"Efeito da deriva vertical na taxa crescimento"


# save()

# create_months_folders()