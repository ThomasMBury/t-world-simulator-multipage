from dash import html, dcc
import dash_bootstrap_components as dbc
from utils.constants import (
    BCL_DEFAULT,
    TOTAL_BEATS_DEFAULT,
    SHOW_LAST_BEATS_DEFAULT,
    QUIESCENCE_DURATION_DEFAULT,
    S2_INTERVALS_DEFAULT,
    BCL_VALUES_DEFAULT,
    NUM_S2_INTERVALS_LIMIT_ONLINE,
    NUM_S2_INTERVALS_LIMIT_OFFLINE,
    TOTAL_BEATS_LIMIT_OFFLINE,
    TOTAL_BEATS_LIMIT_ONLINE,
)
from utils.config import LIMIT_PARAMS


def make_protocol_section(page_id):
    return html.Div(
        [
            dcc.Markdown("-----\n**Protocol: Periodic stimulation**"),
            html.Div(
                [
                    html.Label("Basic cycle length =", style={"fontSize": 14}),
                    dcc.Input(
                        id=f"page-{page_id}-bcl",
                        value=BCL_DEFAULT,
                        type="number",
                        style={"width": 80, "display": "inline-block"},
                        min=1,
                        max=10000,
                    ),
                    html.Label(", BPM = ", style={"fontSize": 14}),
                    dcc.Input(
                        id=f"page-{page_id}-bpm",
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
                        id=f"page-{page_id}-total-beats",
                        value=TOTAL_BEATS_DEFAULT,
                        type="number",
                        style={"width": 80},
                        min=1,
                        max=(
                            TOTAL_BEATS_LIMIT_ONLINE
                            if LIMIT_PARAMS
                            else TOTAL_BEATS_LIMIT_OFFLINE
                        ),
                        step=1,
                    ),
                ]
            ),
            html.Div(
                [
                    html.Label("Show last ", style={"fontSize": 14}),
                    dcc.Input(
                        id=f"page-{page_id}-show-last-beats",
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


def make_protocol_section_dad(page_id):
    return html.Div(
        [
            dcc.Markdown("-----\n**Protocol: Delayed afterdepolarizations**"),
            html.Div(
                [
                    html.Label("Basic cycle length =", style={"fontSize": 14}),
                    dcc.Input(
                        id=f"page-{page_id}-bcl",
                        value=BCL_DEFAULT,
                        type="number",
                        style={"width": 80, "display": "inline-block"},
                        min=1,
                        max=10000,
                    ),
                    html.Label(", BPM = ", style={"fontSize": 14}),
                    dcc.Input(
                        id=f"page-{page_id}-bpm",
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
                        id=f"page-{page_id}-total-beats",
                        value=TOTAL_BEATS_DEFAULT,
                        type="number",
                        style={"width": 80},
                        min=1,
                        max=(
                            TOTAL_BEATS_LIMIT_ONLINE
                            if LIMIT_PARAMS
                            else TOTAL_BEATS_LIMIT_OFFLINE
                        ),
                        step=1,
                    ),
                ]
            ),
            html.Div(
                [
                    html.Label("Quiescence = ", style={"fontSize": 14}),
                    dcc.Input(
                        id=f"page-{page_id}-quiescence-duration",
                        value=QUIESCENCE_DURATION_DEFAULT,
                        type="number",
                        style={"width": 80},
                        min=1,
                        max=100,
                        step=1,
                    ),
                    html.Label(" seconds", style={"fontSize": 14}),
                ]
            ),
        ]
    )


def make_protocol_section_s1s2(page_id):
    return html.Div(
        [
            dcc.Markdown("-----\n**Protocol: S1-S2 restitution**"),
            html.Div(
                [
                    html.Label("S1 cycle length =", style={"fontSize": 14}),
                    dcc.Input(
                        id=f"page-{page_id}-bcl",
                        value=BCL_DEFAULT,
                        type="number",
                        style={"width": 80, "display": "inline-block"},
                        min=1,
                        max=10000,
                    ),
                    html.Label(", BPM = ", style={"fontSize": 14}),
                    dcc.Input(
                        id=f"page-{page_id}-bpm",
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
                    html.Label("Number of S1 pulses = ", style={"fontSize": 14}),
                    dcc.Input(
                        id=f"page-{page_id}-total-beats",
                        value=TOTAL_BEATS_DEFAULT,
                        type="number",
                        style={"width": 80},
                        min=1,
                        max=(
                            TOTAL_BEATS_LIMIT_ONLINE
                            if LIMIT_PARAMS
                            else TOTAL_BEATS_LIMIT_OFFLINE
                        ),
                        step=1,
                    ),
                ],
                style=dict(display="inline-block", width="100%"),
            ),
            # Input box for S2 intervals
            html.Div(
                [
                    html.Label(
                        "S2 intervals (comma separated list, min:max:inc) ",
                        style=dict(fontSize=14),
                    ),
                    dcc.Input(
                        id=f"page-{page_id}-s2-intervals",
                        value=S2_INTERVALS_DEFAULT,
                        type="text",
                        style=dict(width=300),
                        placeholder=S2_INTERVALS_DEFAULT,
                        pattern=r"^\s*\d+:\d+:\d+\s*(,\s*\d+:\d+:\d+\s*)*$",
                    ),
                ]
            ),
        ]
    )


def make_protocol_section_ratedep(page_id):
    return html.Div(
        [
            dcc.Markdown("-----\n**Protocol: Rate dependence and alternans**"),
            # BCL div is hidden
            html.Div(
                dcc.Input(id=f"page-{page_id}-bcl", value=BCL_DEFAULT, type="number"),
                style={"display": "none"},
            ),
            # BCL values list input
            html.Div(
                [
                    html.Label(
                        "BCL values (comma separated list, min:max:inc) ",
                        style=dict(fontSize=14),
                    ),
                    dcc.Input(
                        id=f"page-{page_id}-bcl-values",
                        value=BCL_VALUES_DEFAULT,
                        type="text",
                        style=dict(width=300, display="inline-block"),
                        placeholder=BCL_VALUES_DEFAULT,
                        pattern=r"^\s*\d+:\d+:\d+\s*(,\s*\d+:\d+:\d+\s*)*$",
                    ),
                ]
            ),
            html.Div(
                [
                    html.Label("Number of pulses = ", style={"fontSize": 14}),
                    dcc.Input(
                        id=f"page-{page_id}-total-beats",
                        value=TOTAL_BEATS_DEFAULT,
                        type="number",
                        style={"width": 80},
                        min=1,
                        max=(
                            TOTAL_BEATS_LIMIT_ONLINE
                            if LIMIT_PARAMS
                            else TOTAL_BEATS_LIMIT_OFFLINE
                        ),
                        step=1,
                    ),
                ],
                style=dict(display="inline-block", width="100%"),
            ),
        ]
    )
