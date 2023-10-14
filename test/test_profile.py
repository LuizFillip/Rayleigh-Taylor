import base as b
import matplotlib.pyplot as plt


infile = "database/Results/gamma/saa.txt"
ds = b.load(infile)
ds = ds[~ds.index.duplicated(keep="first")]

ds = ds * 1e3

# col = 'night'
# ds = ds.loc[~(ds[col] > 4)]
ds = ds.loc[ds.index.year == 2015]
# ds[col].plot()

#

ds["drift"].plot()
plt.show()
