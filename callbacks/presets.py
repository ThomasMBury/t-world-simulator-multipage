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


def register_change_to_preset_params(page_id):

    ##### Set outputs for callback
    outputs = []
    # Sliders for current multipliers
    for par in PARAM_NAMES_CURRENT_MULTIPLIERS:
        par_id = par.replace(".", "_")
        outputs.append(
            Output(f"page-{page_id}-{par_id}-slider", "value", allow_duplicate=True)
        )
    # Boxes for extracellular parameters
    for par in PARAM_NAMES_EXTRACELLULAR:
        par_id = par.replace(".", "_")
        outputs.append(
            Output(f"page-{page_id}-{par_id}-box", "value", allow_duplicate=True)
        )
    # Cell type box
    outputs.append(Output(f"page-{page_id}-cell-type", "value", allow_duplicate=True))
    # Sliders for phosphorylation parameters
    for par in PARAM_NAMES_PKA:
        par_id = par.replace(".", "_")
        outputs.append(
            Output(f"page-{page_id}-{par_id}-slider", "value", allow_duplicate=True)
        )
    # Protocol input boxes
    outputs.append(Output(f"page-{page_id}-bcl", "value", allow_duplicate=True))
    outputs.append(Output(f"page-{page_id}-total-beats", "value", allow_duplicate=True))

    # Input is dropdown box that contains preset labels
    inputs = Input(f"page-{page_id}-dropdown-presets", "value")

    @callback(
        outputs,
        inputs,
        prevent_initial_call="initial_duplicate",
        allow_duplicate=True,
    )
    def udpate_sliders_and_boxes(preset):

        preset_params = PARAMETER_PRESETS[preset].copy()
        # Update the default parameters with the preset parameters
        new_params = {**model_params_default, **preset_params}
        return list(new_params.values())
