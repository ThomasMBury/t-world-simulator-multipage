#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 22 May, 2025

Run simulation of T-World model using S1-S2 protocol

@author: tbury
"""


import dash
from dash import html, dcc, callback, Input, Output, ctx, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go


from utils.constants import (
    PARAM_NAMES_EXTRACELLULAR,
    PARAM_NAMES_CELLTYPE,
    PARAM_NAMES_PKA,
    PARAM_NAMES_CURRENT_MULTIPLIERS,
    PLOT_VARIABLES_DEFAULT,
    BCL_DEFAULT,
    SHOW_LAST_BEATS_DEFAULT,
    TOTAL_BEATS_DEFAULT,
    CELL_TYPE_DICT,
    PLOT_VARIABLE_TAB_LABELS,
    S2_INTERVALS_DEFAULT,
)
from utils.helpers import find_crossings, find_local_maxima, s2_input_to_list
from utils.model import MODEL, VARIABLE_NAMES, MODEL_PARAMS_DEFAULT, INITIAL_VALUES
from utils.config import LIMIT_PARAMS
from utils.simulation import sim_model
from utils.figures import make_bcl_ts_fig, make_rate_fig

from components.slider import make_slider

from layout.protocol import make_protocol_section_ratedep
from layout.extracellular import make_extracellular_inputs
from layout.phosphorylation import make_phosphorylation_section
from layout.current_multipliers import make_current_multiplier_section
from layout.figure_panel import make_run_save_buttons_ratedep, make_fig_panel


from callbacks.sliders import register_sync_slider_box, register_sync_input_bcl_bpm
from callbacks.buttons import (
    register_phosphorylation_buttons,
    register_save_button_ratedep,
    register_run_button_ratedep,
)
from callbacks.presets import register_change_to_preset_params
from callbacks.display import (
    register_sync_tabs_with_dropdown,
    register_switch_tabs_ratedep,
)

import myokit as myokit

import pandas as pd

dash.register_page(__name__)

# Set the page ID for this protocol - used for callbacks and layout
page_id = 3

# Create simulation object
simulation = myokit.Simulation(MODEL)

# Create empty DataFrame for simulation data
df_ts = pd.DataFrame(columns=VARIABLE_NAMES + ["time", "bcl"])
df_rate = pd.DataFrame(columns=["bcl", "apd", "cat_amplitude"])
# Need to convert df to dict to store as json on app
ts_data = {"data-frame": df_ts.to_dict("records")}
rate_data = {"data-frame": df_rate.to_dict("records")}

# Make dict contianing all parameter values to save
parameter_data = MODEL_PARAMS_DEFAULT.copy()
parameter_data["bcl"] = BCL_DEFAULT
parameter_data["total_beats"] = TOTAL_BEATS_DEFAULT

# Make figs
fig_ts = make_bcl_ts_fig(df_ts, "membrane.v")
fig_rate = make_rate_fig(df_rate, "membrane.v")
div_fig = html.Div([dcc.Graph(figure=fig_ts), dcc.Graph(figure=fig_rate)])

# Setup figure tabs
list_tabs = [
    dcc.Tab(value=var, label=PLOT_VARIABLE_TAB_LABELS.get(var, var))
    for var in ["membrane.v", "intracellular_ions.cai"]
]
tabs = dcc.Tabs(list_tabs, id=f"page-{page_id}-tabs", value="membrane.v")


# ------------
# App layout
# --------------

# width of a container is 12 units
layout = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                [
                    make_protocol_section_ratedep(page_id),
                    make_current_multiplier_section(page_id),
                    make_extracellular_inputs(page_id),
                    make_phosphorylation_section(page_id),
                ],
                width=4,
            ),
            dbc.Col(
                [
                    html.Div([dcc.Markdown("-----\n**Plot variables:**")]),
                    make_fig_panel(page_id, tabs, div_fig),
                    make_run_save_buttons_ratedep(
                        page_id, ts_data, rate_data, parameter_data
                    ),
                ],
                width=8,
            ),
        ]
    ),
    # fluid=True,
    # style={"paddingLeft": "100px", "paddingRight": "100px"},
)
layout = html.Div(layout)

# --------------
# Callback functions
# --------------

# Callbacks for input boxes and sliders
register_sync_slider_box(page_id)
register_phosphorylation_buttons(page_id)
register_change_to_preset_params(page_id)

# Callbacks for display panel
register_switch_tabs_ratedep(page_id)

# Callbacks for run and save buttons
register_save_button_ratedep(page_id)
register_run_button_ratedep(page_id, simulation)
