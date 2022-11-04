import matplotlib.ticker as ticker
from generalized_growth_rate import *
import locale
from plotConfig import *

fig, ax = plt.subplots(figsize = (15, 20), 
                       ncols = 3,
                       nrows = 2,
                       sharey = True)

plt.rc('text', usetex = True)
plt.subplots_adjust(wspace = 0.2)

text_painels(ax, x = 0.1, y = 0.93)

ax[0, 0].plot(nu, alts, color = "k", lw = 2) 

ax[0, 0].set(xscale = "log", 
       xlabel = ("Frequência de colisão \n íon-neutro" + 
                 r" $\nu_{in}~(s^{-1})$"),
       ylabel = "Altitude (km)")


ax[0, 1].plot(R, alts, color = "k", lw = 2) 
ax[0, 1].set(xscale = "log", 
          xlim = [1e-10, 1e3],
          xlabel = ("Taxa de recombinação,\n " + 
                  r"$\nu_R~(s^{-1})$")
        )

ax[0, 2].plot(U, alts, color = "k", 
              label = "Vento neutro", lw = 2)
ax[0, 2].axvline(Vp, label = r"$V_z$", lw = 2)
ax[0, 2].set(xlabel = "Velocidade~(m/s)", 
             xlim = [-120, 120], 
             xticks = np.arange(-120, 140, 40))
ax[0, 2].legend(loc = "upper right")


ax[1, 0].plot(Ne, alts, color = "k", lw = 2)
ax[1, 0].set(xscale = "log", 
          xlabel = ("Densidade eletrônica,\n"+ 
                    r" $n_0~(cm^{-3}$)"), 
          ylabel = "Altitude (km)")


ax[1, 1].plot(L, alts, color = "k", lw = 2)
ax[1, 1].set(
             xlabel = ("Gradiente de escala (L) \n" + 
                    r"$\frac{1}{n_0} \frac{\partial n_0}{\partial z} (10^{-3} m^{-1})$"))


ax[1, 2].plot(growth_rate_RT(nu, L, R, Vp, U), alts, 
           color = "k", lw = 2)

ax[1, 2].plot(growth_rate_RT(nu, L, 0, Vp, U), alts, 
           label = r"$R = 0 $", lw = 2)

ax[1, 2].plot(growth_rate_RT(nu, L, R, Vp, 0), alts, 
           label = r"$U = 0 $", lw = 2)

ax[1, 2].legend()
ax[1, 2].set(xlim = [-6e-3, 6e-3], 
          xlabel = ("Taxa de crescimento,\n" + 
                    r"$\gamma_{RT}~(10^{-3} s^{-1})$"))





for ax in [ax[1, 1], ax[1, 2]]:
    ax.xaxis.set_major_formatter(
    ticker.FuncFormatter(lambda y, _: '{:g}'.format(y/10e-3)))




locale.setlocale(locale.LC_ALL, 'pt_pt.UTF-8')
time_str = date.strftime("%d de %B de %Y, %H:%M UT")
fig.suptitle(f"Parâmetros da taxa de crescimento Rayleigh-Taylor, \n {time_str}", y = 0.93)

fig.savefig(paths["latex"] + "growth_rate_parameters.png", 
           dpi = 1000)
plt.show()
