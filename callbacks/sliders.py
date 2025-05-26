from dash import Output, Input, ctx, callback
from utils.constants import PARAM_NAMES_CURRENT_MULTIPLIERS, PARAM_NAMES_PKA

from dash import Output, Input, ctx, callback


# ------------
# Sync input between BCL and BPM
# --------------


def sync_input_bcl_bpm(bcl, bpm):
    input_id = ctx.triggered_id or ""
    if input_id[-3:] == "bcl":
        bpm = None if bcl is None else round(60000 / float(bcl), 2)
    else:
        bcl = None if bpm is None else round(60000 / float(bpm), 2)
    return bcl, bpm


def register_sync_input_bcl_bpm(page_id):
    @callback(
        [
            Output(f"page-{page_id}-bcl", "value", allow_duplicate=True),
            Output(f"page-{page_id}-bpm", "value"),
        ],
        [
            Input(f"page-{page_id}-bcl", "value"),
            Input(f"page-{page_id}-bpm", "value"),
        ],
        prevent_initial_call=True,
    )
    def sync_input(bcl, bpm):
        return sync_input_bcl_bpm(bcl, bpm)


# --------------
# Callback to sync slider and box inputs for current multipliers
# ---------------


def sync_slider_box(box_value, slider_value):
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    box_value_out = box_value if trigger_id[-3:] == "box" else slider_value
    slider_value_out = slider_value if trigger_id[-6:] == "slider" else box_value

    return box_value_out, slider_value_out


def register_sync_slider_box(page_id):
    for par in PARAM_NAMES_CURRENT_MULTIPLIERS + PARAM_NAMES_PKA:
        par_id = par.replace(".", "_")
        callback(
            [
                Output(f"page-{page_id}-{par_id}-box", "value", allow_duplicate=True),
                Output(
                    f"page-{page_id}-{par_id}-slider", "value", allow_duplicate=True
                ),
            ],
            [
                Input(f"page-{page_id}-{par_id}-box", "value"),
                Input(f"page-{page_id}-{par_id}-slider", "value"),
            ],
            prevent_initial_call=True,
        )(sync_slider_box)
