import matplotlib.pyplot as plt
import settings as s
import matplotlib.ticker as ticker
import pandas as pd


### COLOCAR OS DOIS PLOTS LADO A LADO (3 x 2)


def get_max(df, times, alts = (200, 350)):
   
    cond_alt = ((df.alt >= alts[0]) &
                (df.alt <= alts[1]))
    
    return [df.loc[(df.index == t) & 
            cond_alt, "g"].max() 
            for t in times]
    
def get_winds(df, heigth = 300):
    return df.loc[df.alt == heigth, "u"]
        

def plot_winds(ax, df, n):
    
    na = [r"$(U_\phi \cos D + U_\theta \sin D)\cos I$", 
          r"$(U_\theta \cos D + U_\phi \sin D)\sin I$",
          r"$U_\theta \cos D + U_\phi \sin D$"]
    
    ws = get_winds(df)

    ax.plot(ws, color = "k", label = na[n])
    
    ax.set(ylabel = "$U_{eff} ~(m/s)$", 
           xlabel = "Meses")
    
    ax.legend()
    
    if n == 0:
        ax.set(title = "Vento efetivo (300 km)")
        

def load(infile):

    df = pd.read_csv(infile, index_col = 0)
    
    df.index = pd.to_datetime(df.index)
    
    df["date"] = df.index.date
    
    return df

def plot_gammas(ax, df, times, n):
    gs = get_max(df, times)
    ax.plot(times, gs, color = "k")


    ax.yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda y, _: '{:g}'.format(y/1e-3)))

    ax.set(ylabel = "$\gamma_{RT} \\times 10^{-3} ~ s^{-1}$")
    
    if n == 0:
        ax.set(title = r"$(V_{zp} - U_{eff} + \frac{g}{\nu_{in}})" +
           "\frac{1}{n_e} \frac{\partial n_e}{\partial y} - R$")

def plot_gammas_end_eff_winds():
    
    fig, ax = plt.subplots(nrows = 3, 
                           figsize = (8, 6),
                           sharey = True,
                           sharex = True)    
    
    plt.subplots_adjust(hspace = 0.05)
    
    s.config_labels()
    
    for n, ax in enumerate(ax.flat):
        
        infile = f"database/data/2014_U{n + 1}.txt"
    
        df = load(infile)
        
        ax.axhline(0, color = "r", linestyle = "--")
        
        plot_winds(ax, df, n)
    
        s.format_axes_date(ax)
        