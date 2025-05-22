from dash import Output, Input, ctx


# --------------
# Callback functions to sync sliders with respective input boxes
# ---------------


def sync_slider_box(box_value, slider_value):
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    box_value_out = box_value if trigger_id.endswith("box") else slider_value
    slider_value_out = slider_value if trigger_id.endswith("slider") else box_value
    return box_value_out, slider_value_out


def register_slider_sync_callbacks(app, list_params):
    for par in list_params:
        par_id = par.replace(".", "_")
        app.callback(
            [
                Output(f"{par_id}_box", "value", allow_duplicate=True),
                Output(f"{par_id}_slider", "value", allow_duplicate=True),
            ],
            [
                Input(f"{par_id}_box", "value"),
                Input(f"{par_id}_slider", "value"),
            ],
            prevent_initial_call=True,
        )(sync_slider_box)
