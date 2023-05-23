import matplotlib.pyplot as plt
from common import plot_roti, plot_terminators
import RayleighTaylor as rt


def plot_local_timeseries(df):
    
    fig, ax = plt.subplots(
        figsize = (8, 6),
        sharex = True,
        nrows = 2, dpi = 300)
    
    # df = df.dropna()
    # ax[0].plot(df * 1e4)
    

    ax[0].set(ylabel = eq.label, 
              title = title
              )
    
    plot_roti(ax[1], df, station = "salu")
    
    
    for ax in ax.flat:
        plot_terminators(ax, df)
        
fig, ax = plt.subplots(
    figsize = (8, 10),
    sharex = True,
    nrows = 4
    )

plt.subplots_adjust(hspace = 0.4)

eq = rt.EquationsRT()

eqs = [eq.gravity(), eq.drift(), eq.complete()]

for num, title in enumerate(eqs):
    
    ax[num].set(title = title, ylabel = eq.label)
    
    
    
    

