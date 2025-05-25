from dash import Output, Input, ctx, callback
from utils.constants import (
    PARAM_NAMES_CURRENT_MULTIPLIERS,
    PARAM_NAMES_PKA,
    PARAM_NAMES_EXTRACELLULAR,
    CELL_TYPE_DICT,
    BCL_DEFAULT,
    TOTAL_BEATS_DEFAULT,
    SHOW_LAST_BEATS_DEFAULT,
)
from utils.presets import PARAMETER_PRESETS
from utils.model import MODEL_PARAMS_DEFAULT


# -------------
# Callback to update sliders and ECM boxes with a change in preset param config
# --------------

# Include BCL in the default parameters
model_params_default = MODEL_PARAMS_DEFAULT.copy()
model_params_default["bcl"] = BCL_DEFAULT
model_params_default["total_beats"] = TOTAL_BEATS_DEFAULT
model_params_default["show_last_beats"] = SHOW_LAST_BEATS_DEFAULT

##### Set outputs for callback
outputs = []
# Sliders for current multipliers
for par in PARAM_NAMES_CURRENT_MULTIPLIERS:
    par_id = par.replace(".", "_")
    outputs.append(Output("{}_slider".format(par_id), "value", allow_duplicate=True))
# Boxes for extracellular parameters
for par in PARAM_NAMES_EXTRACELLULAR:
    par_id = par.replace(".", "_")
    outputs.append(Output("{}_box".format(par_id), "value", allow_duplicate=True))
# Cell type box
outputs.append(Output("cell_type", "value", allow_duplicate=True))
# Sliders for phosphorylation parameters
for par in PARAM_NAMES_PKA:
    par_id = par.replace(".", "_")
    outputs.append(Output("{}_slider".format(par_id), "value", allow_duplicate=True))
# Protocol input boxes
outputs.append(Output("bcl", "value", allow_duplicate=True))
outputs.append(Output("total_beats", "value", allow_duplicate=True))
outputs.append(Output("show_last_beats", "value", allow_duplicate=True))


# Input is dropdown box that contains preset labels
inputs = Input("dropdown_presets", "value")


def register_change_to_preset_params():

    @callback(
        outputs,
        inputs,
        prevent_initial_call=True,
        allow_duplicate=True,
    )
    def udpate_sliders_and_boxes(preset):

        preset_params = PARAMETER_PRESETS[preset].copy()
        # Update the default parameters with the preset parameters
        new_params = {**model_params_default, **preset_params}
        return list(new_params.values())

        # if preset == "default":
        #     return list(model_params_default.values())

        # elif preset == "EAD":
        #     preset_params = PARAMETER_PRESETS["EAD"].copy()
        #     # Update the default parameters with the preset parameters
        #     new_params = {**model_params_default, **preset_params}
        #     return list(new_params.values())

        # else:
        #     return 0
