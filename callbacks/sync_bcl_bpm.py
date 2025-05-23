from dash import Output, Input, ctx, callback


def sync_input_bcl_bpm(bcl, bpm):
    input_id = ctx.triggered_id or ""
    if input_id == "bcl":
        bpm = None if bcl is None else round(60000 / float(bcl), 2)
    else:
        bcl = None if bpm is None else round(60000 / float(bpm), 2)
    return bcl, bpm


def register_sync_input_bcl_bpm():
    @callback(
        [
            Output("bcl", "value", allow_duplicate=True),
            Output("bpm", "value"),
        ],
        [
            Input("bcl", "value"),
            Input("bpm", "value"),
        ],
        prevent_initial_call=True,
    )
    def sync_input(bcl, bpm):
        return sync_input_bcl_bpm(bcl, bpm)
