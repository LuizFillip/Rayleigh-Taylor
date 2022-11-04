import matplotlib.pyplot as plt

fontsize = 25
paths = {"latex" : 
         "G:\\My Drive\\Doutorado\\Modelos_Latex_INPE\\docs\\Proposal\\Figures\\methods\\"}
plt.rcParams.update({'font.size': fontsize, 
                     'axes.linewidth' : 0.5,
                     'grid.linewidth' : 0.5,
                     'lines.linewidth' : 1.,
                     'legend.frameon' : False,
                     'savefig.bbox' : 'tight',
                     'savefig.pad_inches' : 0.05,
                     'mathtext.fontset': 'dejavuserif', 
                     'font.family': 'serif', 
                     'ytick.direction': 'in',
                     'ytick.minor.visible' : True,
                     'ytick.right' : True,
                     'ytick.major.size' : 3,
                     'ytick.major.width' : 0.5,
                     'ytick.minor.size' : 1.5,
                     'ytick.minor.width' : 0.5,
                     'xtick.direction' : 'in',
                     'xtick.major.size' : 3,
                     'xtick.major.width': 0.5,
                     'xtick.minor.size' : 1.5,
                     'xtick.minor.width' : 0.5,
                     'xtick.minor.visible' : True,
                     'xtick.top' : True,
                     'axes.prop_cycle' : plt.cycler('color', ['#0C5DA5', '#00B945', '#FF9500', 
                                                              '#FF2C00', '#845B97', '#474747', '#9e9e9e'])
                         }) 


def text_painels(axs, x = 0.8, y = 0.8, 
                 fontsize = fontsize):
    """Plot text for enumerate painels by letter"""
    chars = list(map(chr, range(97, 123)))
    
    for num, ax in enumerate(axs.flat):
        char = chars[num]
        ax.text(x, y, f"({char})", 
                transform = ax.transAxes, 
                fontsize = fontsize)