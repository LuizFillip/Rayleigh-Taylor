import numpy as np


def generalized_rate_growth(nu, L, R, Vp, U):
    """
    Generalized instability rate growth
    local version
    Paramaters:
    ---------- 
    Vp: Prereversal Enhancement (PRE)
    U: Neutral wind (effective)
    nu: ion-neutral collisional frequency
    L: electron density gradient scale
    R: Recombination rate
    g: acceleration due gravity
    """
     
    return (Vp - U + (9.81 / nu))*L - R

# try:
#     from solar_index import (spectral_data, omni_data)
#     from solar_index.spectral_data import EUVspectra
#     from solar_index.omni_data import OMNIvals
# except ImportError as e:
#     logging.exception('problem importing solar_index: ' + str(e))