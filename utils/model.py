"""
Script to load and prepare the model for simulation.
"""

import myokit
from utils.constants import (
    PARAM_NAMES_CURRENT_MULTIPLIERS,
    PARAM_NAMES_EXTRACELLULAR,
    PARAM_NAMES_CELLTYPE,
    PARAM_NAMES_PKA,
)

# Load model and initial values
model = myokit.load_model("models/TWorld_Apr_2025_tmb.mmt")
variable_names = [var.qname() for var in list(model.variables(const=False))]
initial_values = model.initial_values(as_floats=True)

# Preset parameter configurations - default values
model_params_default = {
    par: model.get(par).value()
    for par in PARAM_NAMES_CURRENT_MULTIPLIERS
    + PARAM_NAMES_EXTRACELLULAR
    + PARAM_NAMES_CELLTYPE
    + PARAM_NAMES_PKA
}

# Make sure celltype is an int
model_params_default["environment.celltype"] = int(
    model_params_default["environment.celltype"]
)

# Expose these for import
MODEL = model
VARIABLE_NAMES = variable_names
MODEL_PARAMS_DEFAULT = model_params_default
INITIAL_VALUES = initial_values
