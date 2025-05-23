from dash import Output, Input, ctx, callback, State, dcc, html
from utils.constants import (
    PARAM_NAMES_CURRENT_MULTIPLIERS,
    PARAM_NAMES_PKA,
    PARAM_NAMES_EXTRACELLULAR,
)
import pandas as pd
from utils.model import MODEL_PARAMS_DEFAULT, INITIAL_VALUES
from utils.simulation import sim_model
from utils.figures import make_simulation_fig

# --------------
# Bbuttons to set all phosphorylation parameters to 0 or 1
# ---------------


def register_phosphorylation_buttons():

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


# ---------
# Button to save simulation and parameter data
# ---------


def register_save_button():

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


# ---------
# Button to run the simulation and make figure
# ---------


def register_run_button(simulation):

    # Output includes (i) all figures, (ii) loading sign (iii) simulation and parameter data for download
    outputs_callback_run = (
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
            for par in PARAM_NAMES_CURRENT_MULTIPLIERS
        },
        params_extracell={
            par: State("{}_box".format(par.replace(".", "_")), "value")
            for par in PARAM_NAMES_EXTRACELLULAR
        },
        params_pka={
            par: State("{}_box".format(par.replace(".", "_")), "value")
            for par in PARAM_NAMES_PKA
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
        for par in PARAM_NAMES_CURRENT_MULTIPLIERS:
            params[par] = MODEL_PARAMS_DEFAULT[par] * params_cond[par]

        # Extracellular
        for par in PARAM_NAMES_EXTRACELLULAR:
            params[par] = params_extracell[par]

        # Phosphorylation
        for par in PARAM_NAMES_PKA:
            params[par] = params_pka[par]

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
