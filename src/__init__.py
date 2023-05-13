from .RT import (
    effects_due_to_winds, 
    effects_due_to_recombination, 
    effects_due_to_drift
    )
from .plotting import *
from .fluxtube import load
from .base import set_data
from .LabelsRT import EquationsFT

import settings as s 

s.config_labels()

from .plotting import *