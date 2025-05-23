from dash import Output, Input, ctx, callback
from utils.constants import PARAM_NAMES_CURRENT_MULTIPLIERS, PARAM_NAMES_PKA


# --------------
# Callback to sync slider and box inputs for current multipliers
# ---------------


def sync_slider_box(box_value, slider_value):
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    box_value_out = box_value if trigger_id[-3:] == "box" else slider_value
    slider_value_out = slider_value if trigger_id[-6:] == "slider" else box_value

    return box_value_out, slider_value_out


def register_sync_slider_box():
    for par in PARAM_NAMES_CURRENT_MULTIPLIERS + PARAM_NAMES_PKA:
        par_id = par.replace(".", "_")
        callback(
            [
                Output("{}_box".format(par_id), "value", allow_duplicate=True),
                Output("{}_slider".format(par_id), "value", allow_duplicate=True),
            ],
            [
                Input("{}_box".format(par_id), "value"),
                Input("{}_slider".format(par_id), "value"),
            ],
            prevent_initial_call=True,
        )(sync_slider_box)
