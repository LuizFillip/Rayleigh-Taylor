import pandas as pd
import matplotlib.pyplot as plt
from plotConfig import *

df = pd.read_csv("database/growthRates/Gammas.txt", 
                 index_col = 0)

df.index = pd.to_datetime(df.index)

df = df.loc[df.index.year == 2014]

fig, ax = plt.subplots(figsize = (14, 6))

df["nowind"].plot()
df["noreco"].plot()
df["nowindReco"].plot()
df["local"].plot()
df["all"].plot()


ax.set(ylim = [-0.5e-3, 3e-3])


