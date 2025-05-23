#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 22 May, 2025

Run simulation of T-World model with periodic pacing protocol

@author: tbury
"""


import dash
from dash import html, dcc, callback, Input, Output, ctx, State
import dash_bootstrap_components as dbc

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
)
from utils.helpers import find_crossings, find_local_maxima, s2_input_to_list
from utils.model import MODEL, VARIABLE_NAMES, MODEL_PARAMS_DEFAULT, INITIAL_VALUES
from utils.config import PARAM_LIMITS
from utils.simulation import sim_model
from utils.figures import make_simulation_fig

from components.slider import make_slider

from layout.protocol import make_protocol_section
from layout.extracellular import make_extracellular_inputs
from layout.phosphorylation import make_phosphorylation_section
from layout.current_multipliers import make_current_multiplier_section
from layout.figure_panel import (
    make_plot_variable_section,
    make_fig_panel,
    make_run_save_buttons,
)

from callbacks.sync_bcl_bpm import register_sync_input_bcl_bpm
from callbacks.sync_slider_box import register_sync_slider_box
from callbacks.buttons import (
    register_phosphorylation_buttons,
    register_save_button,
    register_run_button,
)
from callbacks.presets import register_change_to_preset_params
from callbacks.display import register_sync_tabs_with_dropdown, register_switch_tabs

import myokit as myokit

import pandas as pd

dash.register_page(__name__)


# Create simulation object
simulation = myokit.Simulation(MODEL)


# Run default simulation
df_sim = sim_model(
    simulation,
    INITIAL_VALUES,
    PLOT_VARIABLES_DEFAULT,
    params={},
    bcl=BCL_DEFAULT,
    total_beats=TOTAL_BEATS_DEFAULT,
    beats_keep=SHOW_LAST_BEATS_DEFAULT,
)

# Need to convert df to dict to store as json on app
simulation_data = {"data-frame": df_sim.to_dict("records")}

# Make dict contianing all parameter values to save
parameter_data = MODEL_PARAMS_DEFAULT.copy()
parameter_data["bcl"] = BCL_DEFAULT
parameter_data["total_beats"] = TOTAL_BEATS_DEFAULT
parameter_data["beats_keep"] = SHOW_LAST_BEATS_DEFAULT


# Make default figure
fig = make_simulation_fig(df_sim, "membrane.v")
div_fig = html.Div(dcc.Graph(figure=fig))

# Setup figure tabs
list_tabs = [dcc.Tab(value=var, label=var) for var in PLOT_VARIABLES_DEFAULT]
tabs = dcc.Tabs(list_tabs, id="tabs", value="membrane.v")


# ------------
# App layout
# --------------

# width of a container is 12 units
layout = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                [
                    make_protocol_section(),
                    make_current_multiplier_section(),
                    make_extracellular_inputs(MODEL_PARAMS_DEFAULT),
                    make_phosphorylation_section(),
                ],
                width=4,
            ),
            dbc.Col(
                [
                    make_plot_variable_section(VARIABLE_NAMES, PLOT_VARIABLES_DEFAULT),
                    make_fig_panel(tabs, div_fig),
                    make_run_save_buttons(simulation_data, parameter_data),
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
register_sync_input_bcl_bpm()
register_sync_slider_box()
register_phosphorylation_buttons()
register_change_to_preset_params()

# Callbacks for display panel
register_sync_tabs_with_dropdown()
register_switch_tabs()

# Callbacks for run and save buttons
register_save_button()
register_run_button(simulation)
