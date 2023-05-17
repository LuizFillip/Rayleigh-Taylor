import pandas as pd
import RayleighTaylor as rt
import matplotlib.pyplot as plt

infile = "database/RayleighTaylor/reduced/300km.txt"
df = rt.load_process(infile)

df = rt.separeting_times(df)[0]


def sum_gammas(df, recom = False):
    res = []
    for hem in ["south", "north"]:
        ds = df.loc[df["hem"] == hem]
        
        res.append(rt.effects_due_to_gravity(
            ds, recom = recom))
    
    return pd.concat(res, axis = 1).sum(axis = 1)

ds = sum_gammas(df)
ds.plot()

ds1 = sum_gammas(df, recom  = True)

ds1.plot()

plt.show()

