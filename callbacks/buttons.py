from dash import Output, Input, ctx, callback
from utils.constants import PARAM_NAMES_CURRENT_MULTIPLIERS, PARAM_NAMES_PKA


# --------------
# Callback to update phosphorylation sliders on button click to set all to 0/1
# ---------------


def register_phosphorylation_buttons():
    # This function sets all phosphorylation sliders to 0 or 1
    # depending on which button is clicked

    @callback(
        [
            Output(
                "{}_slider".format(par.replace(".", "_")), "value", allow_duplicate=True
            )
            for par in PARAM_NAMES_PKA
        ],
        Input("no-beta-ars", "n_clicks"),
        prevent_initial_call=True,
    )
    def set_all_sliders_to_zero(n_clicks):
        return [0] * len(PARAM_NAMES_PKA)

    @callback(
        [
            Output(
                "{}_slider".format(par.replace(".", "_")), "value", allow_duplicate=True
            )
            for par in PARAM_NAMES_PKA
        ],
        Input("full-beta-ars", "n_clicks"),
        prevent_initial_call=True,
    )
    def set_all_sliders_to_one(n_clicks):
        return [1] * len(PARAM_NAMES_PKA)
