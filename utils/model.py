"""
Script to load and prepare the model for simulation.
"""

import myokit
from utils.constants import (
    PARAMS_CURRENT_MULTIPLIERS,
    PARAMS_EXTRACELLULAR,
    PARAMS_CELLTYPE,
    PARAMS_PKA,
)

# Load model and initial values
model = myokit.load_model("models/TWorld_Apr_2025_tmb.mmt")
variable_names = [var.qname() for var in list(model.variables(const=False))]
initial_values = model.initial_values(as_floats=True)

# Preset parameter configurations - default values
params_default = {
    par: model.get(par).value()
    for par in PARAMS_CURRENT_MULTIPLIERS
    + PARAMS_EXTRACELLULAR
    + PARAMS_CELLTYPE
    + PARAMS_PKA
}

# Expose these for import
MODEL = model
VARIABLE_NAMES = variable_names
PARAMS_DEFAULT = params_default
INITIAL_VALUES = initial_values
