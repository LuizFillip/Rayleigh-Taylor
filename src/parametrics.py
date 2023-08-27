import RayleighTaylor as rt
from base import sel_times, load
import datetime as dt


infile = 'FluxTube/data/reduced/saa/2019.txt'
dn = dt.datetime(2019, 1, 1, 20)

df = rt.gammas_integrated(sel_times(load(infile), dn))

df['gravity'] = df['gravity']*1e4

df['gravity'].plot()