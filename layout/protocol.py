from dash import html, dcc
import dash_bootstrap_components as dbc


def make_protocol_section(bcl_def, total_beats_def, beats_keep_def, PARAM_LIMITS):
    return html.Div(
        [
            dcc.Markdown("-----\n**Protocol settings**:"),
            html.Div(
                [
                    html.Label("Basic cycle length =", style={"fontSize": 14}),
                    dcc.Input(
                        id="bcl",
                        value=bcl_def,
                        type="number",
                        style={"width": 80, "display": "inline-block"},
                        min=1,
                        max=10000,
                    ),
                    html.Label(", BPM = ", style={"fontSize": 14}),
                    dcc.Input(
                        id="bpm",
                        value=60,
                        type="number",
                        style={"width": 80, "display": "inline-block"},
                        min=6,
                        max=60000,
                    ),
                ]
            ),
            html.Div(
                [
                    html.Label("Number of beats = ", style={"fontSize": 14}),
                    dcc.Input(
                        id="total_beats",
                        value=total_beats_def,
                        type="number",
                        style={"width": 80},
                        min=1,
                        max=500 if PARAM_LIMITS else 10_000,
                        step=1,
                    ),
                ]
            ),
            html.Div(
                [
                    html.Label("Show last ", style={"fontSize": 14}),
                    dcc.Input(
                        id="beats_keep",
                        value=beats_keep_def,
                        type="number",
                        style={"width": 80},
                        min=1,
                        max=200,
                        step=1,
                    ),
                    html.Label(" beats", style={"fontSize": 14}),
                ]
            ),
        ]
    )
