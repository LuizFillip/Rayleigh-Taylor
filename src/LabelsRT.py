class EquationsRT:
    
    @property
    def complete():
        return  r"$(V_{zp} - U + \frac{g}{\nu_{in}})\frac{1}{n_e} \frac{\partial n_e}{\partial y} - R$"
    
    @property
    def wind():
        return r"$(V_{zp} + \frac{g}{\nu_{in}})\frac{1}{n_e} \frac{\partial n_e}{\partial y}$"
    
    @property
    def vzp():
        return r"$(V_{zp} + \\frac{g}{\nu_{in}})\frac{1}{n_e} \frac{\partial n_e}{\partial y} - R$"
    
    @property
    def recombination():
        return r"$(V_{zp} - U + \\frac{g}{\nu_{in}})\frac{1}{n_e} \frac{\partial n_e}{\partial y}$"
    
    @property
    def gravity():
        return "$(\\frac{g}{\nu_{in}})\frac{1}{n_e} \frac{\partial n_e}{\partial y} - R$"
        
class EquationsFT:
    
    def __init__(self, wind_sign = "positive"):
        
        if wind_sign == "positive":
            
            self.wd = "+ U_L^P"
        else:
            self.wd = "- U_L^P"
            
    
        self.ge = "\\frac{g_e}{\\nu_{eff}^{F}}"
        self.re = "R_T"
        self.kf = "K^F"
        self.vp = "V_P"
        self.ratio = "\\frac{\Sigma_P^F}{\Sigma_P^E + \Sigma_P^F}"
    
    @property
    def complete(self):
        return f"$\gamma_{{FT}} = {self.ratio}({self.vp} {self.wd} + {self.ge}){self.kf} - {self.re}$"
    
    
    def drift(self, recom = False):
        if recom:
            return f"$\gamma_{{FT}} = {self.ratio}({self.vp} + {self.ge}){self.kf} - {self.re}$"
        else:
            return f"$\gamma_{{FT}} = {self.ratio}({self.vp} + {self.ge}){self.kf}$"
    
    @property
    def gravity(self):
        return f"$\gamma_{{FT}} = {self.ratio}({self.ge}){self.kf}$"
    
    @property
    def winds(self):
        return f"$\gamma_{{FT}} = {self.ratio}({self.wd} + {self.ge}){self.kf}$"
    
    @property
    def recombination(self):
        return f"$\gamma_{{FT}} = {self.ratio}({self.wd} + {self.ge}){self.kf} - {self.re}$"
    
    @property
    def label(self):
        return f"$\gamma_{{FT}} ~(\\times 10^{{-4}}~s^{{-1}})$"
    
    
def main():

    import matplotlib.pyplot as plt
    
    la = EquationsFT(wind_sign="negative")
    
    final = la.winds
    
    fig, ax = plt.subplots(dpi = 300)
    
    
