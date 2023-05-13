


def plot_growth_rate_RT(
        ax, 
        nu, l, r, vz, u, alts
        ):
    
    name = "Taxa de crescimento Rayleigh-Taylor"
    symbol = "$\gamma_{RT}$"
    units = "$10^{-3} s^{-1}$"
    
    ax.plot(growth_rate_RT(nu, l, r, vz, u), alts, 
               color = "k", lw = 2)
    
    ax.plot(growth_rate_RT(nu, l, 0, vz, u), alts, 
               label = r"$R = 0 $", lw = 2)
    
    ax.plot(growth_rate_RT(nu, l, r, vz, 0), alts, 
               label = r"$U = 0 $", lw = 2)
    
    ax.legend()
    ax.set(
        title = name,
        xlim = [-6e-3, 6e-3], 
        xlabel = (f"{symbol} ({units})")
        )
    