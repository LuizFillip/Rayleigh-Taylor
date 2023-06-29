from .base import set_data, split_by_freq, load_process
from .eq_labels import EquationsFT, EquationsRT

from .RT import (
    all_effects,
    effects_due_to_winds, 
    effects_due_to_drift,
    effects_due_to_gravity, 
    gammas_integrated,
    gammas_locals
    )


import settings as s 

s.config_labels()

from .plotting import *

s.language_mode()