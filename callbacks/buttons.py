from dash import Output, Input, ctx, callback, State, dcc, html
from utils.constants import (
    PARAM_NAMES_CURRENT_MULTIPLIERS,
    PARAM_NAMES_PKA,
    PARAM_NAMES_EXTRACELLULAR,
    PARAM_NAMES_CELLTYPE,
)
import pandas as pd
from utils.model import MODEL_PARAMS_DEFAULT, INITIAL_VALUES
from utils.simulation import sim_model
from utils.figures import make_simulation_fig

# --------------
# Bbuttons to set all phosphorylation parameters to 0 or 1
# ---------------


def register_phosphorylation_buttons(page_id):
    list_outputs = []
    for par in PARAM_NAMES_PKA:
        # Create output for each parameter
        par_label = par.replace(".", "_")
        list_outputs.append(
            Output(f"page-{page_id}-{par_label}-slider", "value", allow_duplicate=True)
        )

    @callback(
        list_outputs,
        Input(f"page-{page_id}-no-beta-ars", "n_clicks"),
        prevent_initial_call=True,
    )
    def set_all_sliders_to_zero(n_clicks):
        return [0] * len(PARAM_NAMES_PKA)

    @callback(
        list_outputs,
        Input(f"page-{page_id}-full-beta-ars", "n_clicks"),
        prevent_initial_call=True,
    )
    def set_all_sliders_to_one(n_clicks):
        return [1] * len(PARAM_NAMES_PKA)


# ---------
# Button to save simulation and parameter data
# ---------


def register_save_button(page_id):

    @callback(
        [
            Output(f"page-{page_id}-download-simulation", "data"),
            Output(f"page-{page_id}-download-parameters", "data"),
        ],
        Input(f"page-{page_id}-button-savedata", "n_clicks"),
        State(f"page-{page_id}-simulation-data", "data"),
        State(f"page-{page_id}-parameter-data", "data"),
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


# ---------
# Button to run the simulation and make figure
# ---------


def register_run_button(page_id, simulation):

    # Output includes (i) all figures, (ii) loading sign (iii) simulation and parameter data for download
    list_outputs = [
        Output(f"page-{page_id}-tabs-container-output-div", "children"),
        Output(f"page-{page_id}-loading-output", "children"),
        Output(f"page-{page_id}-simulation-data", "data"),
        Output(f"page-{page_id}-parameter-data", "data"),
    ]
    # Input is click of run button
    dict_inputs = dict(n_clicks=[Input(f"page-{page_id}-run-button", "n_clicks")])

    # State values are all parameters contained in sliders + boxes
    dict_states = dict(
        bcl=State(f"page-{page_id}-bcl", "value"),
        total_beats=State(f"page-{page_id}-total-beats", "value"),
        show_last_beats=State(f"page-{page_id}-show-last-beats", "value"),
        cell_type=State(f"page-{page_id}-cell-type", "value"),
        plot_vars=State(f"page-{page_id}-dropdown-plot-vars", "value"),
        current_plot_var=State(f"page-{page_id}-tabs", "value"),
        params_cond={
            par: State(f"page-{page_id}-{par_id}-box", "value")
            for par in PARAM_NAMES_CURRENT_MULTIPLIERS
            for par_id in [par.replace(".", "_")]
        },
        params_extracell={
            par: State(f"page-{page_id}-{par_id}-box", "value")
            for par in PARAM_NAMES_EXTRACELLULAR
            for par_id in [par.replace(".", "_")]
        },
        params_pka={
            par: State(f"page-{page_id}-{par_id}-box", "value")
            for par in PARAM_NAMES_PKA
            for par_id in [par.replace(".", "_")]
        },
    )

    @callback(
        output=list_outputs,
        inputs=dict_inputs,
        state=dict_states,
        prevent_initial_call=True,
    )
    def run_sim_and_update_fig(
        n_clicks,
        bcl,
        total_beats,
        show_last_beats,
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
        for par in PARAM_NAMES_CURRENT_MULTIPLIERS:
            params[par] = MODEL_PARAMS_DEFAULT[par] * params_cond[par]

        # Extracellular
        for par in PARAM_NAMES_EXTRACELLULAR:
            params[par] = params_extracell[par]

        # Phosphorylation
        for par in PARAM_NAMES_PKA:
            params[par] = params_pka[par]

        # Cell type
        for par in PARAM_NAMES_CELLTYPE:
            params[par] = cell_type

        # Make dict contianing all parameter values to save
        parameter_data = params.copy()
        parameter_data["bcl"] = bcl
        parameter_data["total_beats"] = total_beats
        parameter_data["show_last_beats"] = show_last_beats

        # Run simulation
        df_sim = sim_model(
            simulation,
            INITIAL_VALUES,
            plot_vars,
            params=params,
            bcl=bcl,
            total_beats=total_beats,
            show_last_beats=show_last_beats,
        )

        # Need to convert df to dict to store as json
        simulation_data = {"data-frame": df_sim.to_dict("records")}

        fig = make_simulation_fig(df_sim, current_plot_var)
        div_fig = html.Div(dcc.Graph(figure=fig))

        return [div_fig, "", simulation_data, parameter_data]
