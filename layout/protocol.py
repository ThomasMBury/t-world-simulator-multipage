from dash import html, dcc
import dash_bootstrap_components as dbc
from utils.constants import (
    BCL_DEFAULT,
    TOTAL_BEATS_DEFAULT,
    SHOW_LAST_BEATS_DEFAULT,
)
from utils.config import PARAM_LIMITS


def make_protocol_section():
    return html.Div(
        [
            dcc.Markdown("-----\n**Protocol settings**:"),
            html.Div(
                [
                    html.Label("Basic cycle length =", style={"fontSize": 14}),
                    dcc.Input(
                        id="bcl",
                        value=BCL_DEFAULT,
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
                        value=TOTAL_BEATS_DEFAULT,
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
                        id="show_last_beats",
                        value=SHOW_LAST_BEATS_DEFAULT,
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
