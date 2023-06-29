import RayleighTaylor as rt
import os
from utils import save_but_not_show, fname_to_save
import matplotlib.pyplot as plt
import datetime as dt

def save(
        fig, 
        fname, 
        save_in, 
        root = "D:\\plots\\"
        ):
    
    save_but_not_show(fig, os.path.join(root, save_in, fname))
    
    return None

plt.ioff()
    
def save_3():
          
    infile = "database/RayleighTaylor/reduced/300.txt"
    
    df = rt.load_process(infile, apex = 300)
    
    
    for ds in rt.split_by_freq(df, freq_per_split = "10D"):
        
        dn = ds.index[0]
        
        fname = fname_to_save(ds)
        
        
        if ((dn > dt.datetime(2013, 3, 1)) and 
            (dn < dt.datetime(2013, 4, 1))):
            
            station = "ceft"
                    
        elif ((dn >= dt.datetime(2013, 5, 1)) and 
            (dn < dt.datetime(2013, 5, 20))):
            
            station = "salu"
            
        else:
            station = "ceeu"
        
     
        
        print("saving...", dn)
        
        # save(
        #     rt.plot_gravity_effect(ds, station = station), 
        #     fname, "gravity"
        #     )
        
        
        # save(
        #     rt.plot_drift_effect(ds, station = station), 
        #     fname, "vertical_drift"
        #     )
        
    
        # save(rt.plot_total_gravity_drift_effect(ds, station = station), 
        #       fname, "total_gravity_drift", root = "D:\\plots3\\")
        
        for recom in [False]:
            
            if recom: 
                w = "with" 
            else: 
                w = "without"
                            
            # save(
            #     rt.plot_winds_effect(
            #         ds, recom = recom, station = station), 
            #         fname, f"winds_{w}_rec"
            #         )
            
        
            # save(rt.plot_total_winds_effect(
            #     ds, rc = recom, station = station),  
            #     fname, f"total_winds_{w}_rec", root = "D:\\plots3\\")
            
            for drift in ["vz", "vzp"]:
                
                # save(rt.plot_all_effects(
                #     ds, recom, drift = drift, station = station,
                #     ), fname, f"winds_and_{drift}_{w}_rec")
                    
               
                save(rt.plot_total_all_effects(
                        ds, drift = drift, rc = recom, station = station,
                        ), fname, f"total_effects_{drift}_{w}_rec", 
                    root = "D:\\plots3\\")

save_3()

plt.clf()   
plt.close()