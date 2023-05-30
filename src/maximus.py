import pandas as pd

def gamma_max_from_filter(df, date, alts = (250, 350)):
   
    cond_alt = ((df.index >= alts[0]) &
                (df.index <= alts[1]))
    
    cond_time = (df["date"] == date)
    
    return df.loc[cond_alt & cond_time, "g"].max()

def gamma_maximus(infile = "02_11_north.txt"):
    
    df = pd.read_csv(infile, index_col=0)
    dat = {
           "gamma_zon" : [], 
           "gamma_zon_ef" : [], 
           "gamma_g" : [], 
           "z_gamma_zon": [], 
           "z_gamma_zon_ef" : [], 
           "z_gamma_g" : [], 
           }
    times  = df["dn"].unique()
    for time in times:
    
        ds = df.loc[df["dn"] == time]
        
        for col in ['gamma_g', 'gamma_zon', 'gamma_zon_ef']:
            dat[col].append(ds[col].max())
            dat[f"z_{col}"].append(ds[col].idxmax())
            
    
    ts = pd.DataFrame(dat, index = times)
    
    ts.index = pd.to_datetime(ts.index)
    ts = ts.loc[ts.index.month == 2]
   
infile = "parameters_car.txt"
df = pd.read_csv(infile, index_col=0)

df