class EquationsRT:
    
    
    def __init__(self, r = False):
        self.r = r
        self.L = "L^{-1}"
        self.g = "\\frac{g}{\\nu_{in}}"
        self.vp = "V_{zp}"
        self.wd = "u_n"
    
    
    @property
    def complete(self):
            
        if self.r:
            return f"$\gamma_{{RT}} = ({self.vp} - {self.wd} + {self.g}){self.L} - R$"
        else:
            return f"$\gamma_{{RT}} = ({self.vp} - {self.wd} + {self.g}){self.L}$"
        
    @property
    def winds(self):
            
        if self.r:
            return  f"$\gamma_{{RT}} = (-{self.wd}){self.L} - R$" #+ {self.g}
        else:
            return  f"$\gamma_{{RT}} = (-{self.wd}){self.L}$"
    @property
    def drift(self):
        if self.r:
            return f"$\gamma_{{RT}} = ({self.vp}){self.L} - R$" 
        else:
            return f"$\gamma_{{RT}} = ({self.vp}){self.L}$"
    @property
    def gravity(self):
        if self.r:
            return  f"$\gamma_{{RT}} = {self.g}{self.L} - R$"
        else:
            return  f"$\gamma_{{RT}} = {self.g}{self.L}$"
        
    @property
    def label(self):
        return "$\gamma_{RT} ~(\\times 10^{-4}~s^{-1})$"
        
class EquationsFT:
    
    def __init__(self, r = False):
        self.r = r
        self.ge = "\\frac{g_e}{\\nu_{eff}^{F}}"
        self.re = "R_T"
        self.kf = "K^F"
        self.vp = "V_P"
        self.ratio = "\\frac{\Sigma_P^F}{\Sigma_P^E + \Sigma_P^F}"
    
    def drift(self):
        if self.r:
            return f"$\gamma_{{FT}} = {self.ratio}({self.vp}){self.kf} - {self.re}$"
        else:
            return f"$\gamma_{{FT}} = {self.ratio}({self.vp} ){self.kf}$"
    
    def gravity(self):
        if self.r:
            return f"$\gamma_{{FT}} = {self.ratio}({self.ge}){self.kf} - {self.re}$" 
        else:
            return f"$\gamma_{{FT}} = {self.ratio}({self.ge}){self.kf}$"
    
    def complete(self):
        if self.r:
            return f"$\gamma_{{FT}} = {self.ratio}({self.vp} - U_L^P + {self.ge}){self.kf} - {self.re}$"
        else:
            return f"$\gamma_{{FT}} = {self.ratio}({self.vp} - U_L^P + {self.ge}){self.kf}$"
        
      
    
    def winds(self):
        
        if self.r:
            return f"$\gamma_{{FT}} = {self.ratio}( - U_L^P ){self.kf} - {self.re}$" #+ {self.ge}
        else:
            return f"$\gamma_{{FT}} = {self.ratio}( - U_L^P){self.kf}$"
    

    @property
    def label(self):
        return "$\gamma_{{FT}} ~(\\times 10^{{-4}}~s^{{-1}})$"
    
