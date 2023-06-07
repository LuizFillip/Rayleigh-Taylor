class EquationsRT:
    def __init__(self):
        
        self.L = "\\frac{1}{n_e} \\frac{\partial n_e}{\partial y}"
        self.g = "\\frac{g}{\\nu_{in}}"
        self.vp = "V_{zp}"
        
    def winds(self, sign = 1, rc = False):
        if sign == 1:
            self.wd = "+ u_n"
        else:
            self.wd = "- u_n"
        if rc:
            return  f"$\gamma_{{RT}} = ({self.wd} + {self.g}){self.L} - R$"
        else:
            return  f"$\gamma_{{RT}} = ({self.wd} + {self.g}){self.L}$"
    
    def complete(self, sign = 1, rc = False):
        if sign == 1:
            self.wd = "+ u_n"
        else:
            self.wd = "- u_n"
            
        if rc:
            return f"$\gamma_{{RT}} = ({self.vp} {self.wd} + {self.g}){self.L} - R$"
        else:
            return f"$\gamma_{{RT}} = ({self.vp} {self.wd} + {self.g}){self.L}$"
    
    def drift(self, rc = False):
        if rc:
            return f"$\gamma_{{RT}} = ({self.vp} + {self.g}){self.L} - R$"
        else:
            return f"$\gamma_{{RT}} = ({self.vp} + {self.g}){self.L}$"
    
    def gravity(self, rc = False):
        if rc:
            return  f"$\gamma_{{RT}} = {self.g}{self.L} - R$"
        else:
            return  f"$\gamma_{{RT}} = {self.g}{self.L}$"
        
    @property
    def label(self):
        return "$\gamma_{RT} ~(\\times 10^{-4}~s^{-1})$"
        
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
    
    def complete(self, 
              wind_sign = -1, 
              recom = False):
        
        if wind_sign == 1:     
            wd = "+ U_L^P"
        else:
            wd = "- U_L^P"
            
        if recom:
            return f"$\gamma_{{FT}} = {self.ratio}({self.vp} {wd} + {self.ge}){self.kf} - {self.re}$"
        else:
            return f"$\gamma_{{FT}} = {self.ratio}({self.vp} {wd} + {self.ge}){self.kf}$"
        
      
    
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
        return "$\gamma_{{FT}} ~(\\times 10^{{-4}}~s^{{-1}})$"
    
