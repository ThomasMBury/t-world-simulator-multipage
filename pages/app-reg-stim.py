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
    PARAMS_EXTRACELLULAR,
    PARAMS_CELLTYPE,
    PARAMS_PKA,
    PARAMS_CURRENT_MULTIPLIERS,
    PLOT_VARIABLES_DEFAULT,
)
from utils.helpers import find_crossings, find_local_maxima, s2_input_to_list
from utils.model import MODEL, VARIABLE_NAMES, PARAMS_DEFAULT, INITIAL_VALUES
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
import myokit as myokit

import pandas as pd

dash.register_page(__name__)


# Create simulation object
simulation = myokit.Simulation(MODEL)

# Default protocol values
bcl_def = 1000
total_beats_def = 20
beats_keep_def = 1


# Run default simulation
df_sim = sim_model(
    simulation,
    INITIAL_VALUES,
    PLOT_VARIABLES_DEFAULT,
    params={},
    bcl=bcl_def,
    total_beats=total_beats_def,
    beats_keep=beats_keep_def,
)

# Need to convert df to dict to store as json on app
simulation_data = {"data-frame": df_sim.to_dict("records")}

# Make dict contianing all parameter values to save
parameter_data = PARAMS_DEFAULT.copy()
parameter_data["bcl"] = bcl_def
parameter_data["total_beats"] = total_beats_def
parameter_data["beats_keep"] = beats_keep_def


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
                    make_protocol_section(
                        bcl_def, total_beats_def, beats_keep_def, PARAM_LIMITS
                    ),
                    make_current_multiplier_section(),
                    make_extracellular_inputs(PARAMS_DEFAULT),
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


# -----------------
# Callback function to sync BCL and BPM boxes
# -----------------
@callback(
    [
        Output(
            "bcl",
            "value",
            allow_duplicate=True,
        ),
        Output("bpm", "value"),
    ],
    [
        Input("bcl", "value"),
        Input("bpm", "value"),
    ],
    prevent_initial_call=True,
)
def sync_input(bcl, bpm):
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if input_id == "bcl":
        bpm = None if bcl is None else int(60000 / float(bcl) * 100) / 100
    else:
        bcl = None if bpm is None else int(60000 / float(bpm) * 100) / 100
    return bcl, bpm


# --------------
# Callback functions to sync sliders with respective input boxes
# ---------------


def sync_slider_box(box_value, slider_value):
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    box_value_out = box_value if trigger_id[-3:] == "box" else slider_value
    slider_value_out = slider_value if trigger_id[-6:] == "slider" else box_value

    return box_value_out, slider_value_out


for par in PARAMS_CURRENT_MULTIPLIERS + PARAMS_PKA:
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


# --------------
# Callback to update phosphor sliders on button click to set all to 0/1
# ---------------


@callback(
    [
        Output("{}_slider".format(par.replace(".", "_")), "value", allow_duplicate=True)
        for par in PARAMS_PKA
    ],
    Input("no-beta-ars", "n_clicks"),
    prevent_initial_call=True,
)
def set_all_sliders_to_zero(n_clicks):
    return [0] * len(PARAMS_PKA)


@callback(
    [
        Output("{}_slider".format(par.replace(".", "_")), "value", allow_duplicate=True)
        for par in PARAMS_PKA
    ],
    Input("full-beta-ars", "n_clicks"),
    prevent_initial_call=True,
)
def set_all_sliders_to_one(n_clicks):
    return [1] * len(PARAMS_PKA)


# -------------
# Callback to update sliders and ECM boxes with a change in preset param config
# --------------

# Default slider and box parameters
pars_slider_box_default = PARAMS_DEFAULT.copy()
# Don't need cell type, or phosphorylation parameters here
_ = pars_slider_box_default.pop("environment.celltype")

pars_ead = {}
pars_ead["multipliers.IKr_multiplier"] = 0.15
pars_ead["extracellular.nao"] = 137
pars_ead["extracellular.clo"] = 148
pars_ead["extracellular.cao"] = 2
bcl_ead = 4000

# Output includes all sliders and ECM boxes
outputs_callback_preset = [
    Output("multipliers_IKr_multiplier_slider", "value", allow_duplicate=True),
    Output("extracellular_nao_box", "value", allow_duplicate=True),
    Output("extracellular_clo_box", "value", allow_duplicate=True),
    Output("extracellular_cao_box", "value", allow_duplicate=True),
    Output("bcl", "value", allow_duplicate=True),
]

# Input is dropdown box that contains preset labels
inputs_callback_presets = Input("dropdown_presets", "value")


@callback(
    outputs_callback_preset,
    inputs_callback_presets,
    prevent_initial_call=True,
    allow_duplicate=True,
)
def udpate_sliders_and_boxes(preset):
    if preset == "default":
        return [PARAMS_DEFAULT[key] for key in pars_ead.keys()] + [bcl_def]
    elif preset == "EAD":
        return list(pars_ead.values()) + [bcl_ead]
    else:
        return 0


# ---------
# Callback to sync tabs with variables selected in dropdown box
# ---------


@callback(
    Output("tabs_container_div", "children"), Input("dropdown_plot_vars", "value")
)
def display_tabs(plot_vars):
    tabs = [dcc.Tab(value=var, label=var) for var in plot_vars]
    children = (
        dcc.Tabs(
            id="tabs",
            value="membrane.v",
            children=tabs,
        ),
    )
    return children


# ---------
# Callback to save simulation and parameter data
# ---------
@callback(
    [
        Output("download_simulation", "data"),
        Output("download_parameters", "data"),
    ],
    Input("button_savedata", "n_clicks"),
    State("simulation_data", "data"),
    State("parameter_data", "data"),
    prevent_initial_call=True,
)
def func(n_clicks, simulation_data, parameter_data):
    df_sim = pd.DataFrame(simulation_data["data-frame"])
    df_pars = pd.DataFrame()
    df_pars["name"] = parameter_data.keys()
    df_pars["value"] = parameter_data.values()
    # df_pars = df_pars.astype("object")
    out1 = dcc.send_data_frame(df_sim.to_csv, "simulation_data.csv")
    out2 = dcc.send_data_frame(df_pars.to_csv, "parameters.csv")
    return [out1, out2]


# -----------
# Callback function on RUN button click - run simulation and make figure
# ------------

# Output includes (i) all figures, (ii) loading sign (iii) simulation and parameter data for download
outputs_callback_run = (
    # [Output("fig_{}".format(var).replace(".", "_"), "figure") for var in plot_vars_def]
    # [Output("div_tabs", "children")]
    Output("tabs_container_output_div", "children"),
    Output("loading-output", "children"),
    Output("simulation_data", "data"),
    Output("parameter_data", "data"),
)
# Input is click of run button
inputs_callback_run = dict(n_clicks=[Input("run_button", "n_clicks")])

# State values are all parameters contained in sliders + boxes
states_callback_run = dict(
    bcl=State("bcl", "value"),
    total_beats=State("total_beats", "value"),
    beats_keep=State("beats_keep", "value"),
    cell_type=State("cell_type", "value"),
    plot_vars=State("dropdown_plot_vars", "value"),
    current_plot_var=State("tabs", "value"),
    params_cond={
        par: State("{}_box".format(par.replace(".", "_")), "value")
        for par in PARAMS_CURRENT_MULTIPLIERS
    },
    params_extracell={
        par: State("{}_box".format(par.replace(".", "_")), "value")
        for par in PARAMS_EXTRACELLULAR
    },
    params_pka={
        par: State("{}_box".format(par.replace(".", "_")), "value")
        for par in PARAMS_PKA
    },
)


@callback(
    output=outputs_callback_run,
    inputs=inputs_callback_run,
    state=states_callback_run,
    prevent_initial_call=True,
)
def run_sim_and_update_fig(
    n_clicks,
    bcl,
    total_beats,
    beats_keep,
    cell_type,
    plot_vars,
    current_plot_var,
    params_cond,
    params_extracell,
    params_pka,
):
    # Updated parameter values
    params = {}

    # Multipliers
    for par in PARAMS_CURRENT_MULTIPLIERS:
        params[par] = PARAMS_DEFAULT[par] * params_cond[par]

    # Extracellular
    for par in PARAMS_EXTRACELLULAR:
        params[par] = params_extracell[par]

    # Phosphorylation
    for par in PARAMS_PKA:
        params[par] = params_pka[par]

    # Cell type
    cell_type_dict = {"endo": 0, "epi": 1, "mid": 2}
    params["environment.celltype"] = cell_type_dict[cell_type]

    # Make dict contianing all parameter values to save
    parameter_data = params.copy()
    parameter_data["bcl"] = bcl
    parameter_data["total_beats"] = total_beats
    parameter_data["beats_keep"] = beats_keep

    # Run simulation
    df_sim = sim_model(
        simulation,
        INITIAL_VALUES,
        plot_vars,
        params=params,
        bcl=bcl,
        total_beats=total_beats,
        beats_keep=beats_keep,
    )

    # Need to convert df to dict to store as json
    simulation_data = {"data-frame": df_sim.to_dict("records")}

    fig = make_simulation_fig(df_sim, current_plot_var)
    div_fig = html.Div(dcc.Graph(figure=fig))

    return [div_fig, "", simulation_data, parameter_data]


# ---------
# Callback to switch between tabs
# ---------
@callback(
    Output("tabs_container_output_div", "children", allow_duplicate=True),
    Input("tabs", "value"),
    State("simulation_data", "data"),
    prevent_initial_call=True,
)
def render_content(tab, simulation_data):
    df_sim = pd.DataFrame(simulation_data["data-frame"])
    fig = make_simulation_fig(df_sim, tab)
    div_fig = html.Div(dcc.Graph(figure=fig))
    return div_fig
