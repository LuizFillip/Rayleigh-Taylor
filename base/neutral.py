import numpy as np


def ion_neutral_collision(Tn, O, O2, N2):
    """The ion-neutral collision rates (frequency)"""
    term_O = 4.45e-11 * O * np.sqrt(Tn) * (1.04 - 0.067 * np.log10(Tn))**2
    term_O2 = 6.64e-10 * O2
    term_N2 = 6.82e-10 * N2
        
    return term_O + term_O2 + term_N2

class neutrals(object):
    
    def __init__(self, TN, O, O2, N2):
        self.tn = TN
        self.o = O
        self.o2 = O2
        self.n2 = N2

    @property
    def collision(self):
        """Collision frequency from Bailey and Balan 1992"""
        nu_o = (4.45e-11 * self.o * np.sqrt(self.tn) * 
               (1.04 - 0.067 * np.log10(self.tn)) ** 2.0)
        
        nu_o2 = (6.64e-10 * self.o2)
        
        nu_n2 = 6.82e-10 * self.n2
        
        return  nu_o + nu_o2 + nu_n2
    
    @property
    def recombination(self):
        
        return (4.0e-11  * self.o2) + (1.3e-12   * self.n2)    
  