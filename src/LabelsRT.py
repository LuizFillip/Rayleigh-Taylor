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
    
    def __init__(self):
        
        self.ge = "\\frac{g_e}{\\nu_{eff}^{F}}"
        self.re = "R_T"
        self.kf = "K^F"
        self.vp = "V_P"
        self.ratio = "\\frac{\Sigma_P^F}{\Sigma_P^E + \Sigma_P^F}"
    
    
    
    
    def drift(self, recom = False):
        if recom:
            return f"$\gamma_{{FT}} = {self.ratio}({self.vp} + {self.ge}){self.kf} - {self.re}$"
        else:
            return f"$\gamma_{{FT}} = {self.ratio}({self.vp} + {self.ge}){self.kf}$"
    
    def gravity(self, recom = False):
        if recom:
            return f"$\gamma_{{FT}} = {self.ratio}({self.ge}){self.kf} - {self.re}$" 
        else:
            return f"$\gamma_{{FT}} = {self.ratio}({self.ge}){self.kf}$"
    
    @property
    def complete(self):
        return f"$\gamma_{{FT}} = {self.ratio}({self.vp} {self.wd} + {self.ge}){self.kf} - {self.re}$"
    
    def winds(self, 
              wind_sign = -1, 
              recom = False):
        
        if wind_sign == 1:     
            wd = "+ U_L^P"
        else:
            wd = "- U_L^P"
            
        if recom:
            return f"$\gamma_{{FT}} = {self.ratio}({wd} + {self.ge}){self.kf} - {self.re}$"
        else:
            return f"$\gamma_{{FT}} = {self.ratio}({wd} + {self.ge}){self.kf}$"
    

    @property
    def label(self):
        return f"$\gamma_{{FT}} ~(\\times 10^{{-4}}~s^{{-1}})$"
    
    
def main():

    import matplotlib.pyplot as plt
    
    la = EquationsFT(wind_sign="negative")
    
    final = la.winds
    
    fig, ax = plt.subplots(dpi = 300)
    
    
