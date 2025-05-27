from dash import Output, Input, ctx, callback, dcc, State, html
from utils.constants import PLOT_VARIABLE_TAB_LABELS
from utils.figures import (
    make_simulation_fig,
    make_s1s2_fig,
    make_restitution_fig,
    make_bcl_ts_fig,
    make_rate_fig,
)
import pandas as pd

# ---------
# Callback to sync tabs with variables selected in dropdown box
# ---------


def register_sync_tabs_with_dropdown(page_id):
    # This function updates the tabs to match the variables selected in the dropdown box
    # It also sets the default tab to be the first one in the list

    @callback(
        Output(f"page-{page_id}-tabs-container-div", "children"),
        Input(f"page-{page_id}-dropdown-plot-vars", "value"),
    )
    def display_tabs(plot_vars):
        tabs = [
            dcc.Tab(value=var, label=PLOT_VARIABLE_TAB_LABELS.get(var, var))
            for var in plot_vars
        ]
        children = (
            dcc.Tabs(
                id=f"page-{page_id}-tabs",
                value="membrane.v",
                children=tabs,
            ),
        )
        return children


# ---------
# Callback to switch between tabs
# ---------
def register_switch_tabs(page_id):

    @callback(
        Output(
            f"page-{page_id}-tabs-container-output-div",
            "children",
            allow_duplicate=True,
        ),
        Input(f"page-{page_id}-tabs", "value"),
        State(f"page-{page_id}-simulation-data", "data"),
        prevent_initial_call=True,
    )
    def render_content(tab, simulation_data):
        df_sim = pd.DataFrame(simulation_data["data-frame"])
        fig = make_simulation_fig(df_sim, tab)
        div_fig = html.Div(dcc.Graph(figure=fig))
        return div_fig


# ---------
# S1S2 app : Callback to switch between tabs
# ---------
def register_switch_tabs_s1s2(page_id):

    @callback(
        Output(
            f"page-{page_id}-tabs-container-output-div",
            "children",
            allow_duplicate=True,
        ),
        Input(f"page-{page_id}-tabs", "value"),
        State(f"page-{page_id}-ts-data", "data"),
        State(f"page-{page_id}-restitution-data", "data"),
        prevent_initial_call=True,
    )
    def render_content(tab, ts_data, restitution_data):
        df_ts = pd.DataFrame(ts_data["data-frame"])
        df_restitution = pd.DataFrame(restitution_data["data-frame"])
        fig_ts = make_s1s2_fig(df_ts, tab)
        fig_restitution = make_restitution_fig(df_restitution, tab)
        div_fig = html.Div(
            [dcc.Graph(figure=fig_ts), dcc.Graph(figure=fig_restitution)]
        )
        return div_fig


# ------------
# Rate dep app : Callback to switch between tabs
# ---------
def register_switch_tabs_ratedep(page_id):

    @callback(
        Output(
            f"page-{page_id}-tabs-container-output-div",
            "children",
            allow_duplicate=True,
        ),
        Input(f"page-{page_id}-tabs", "value"),
        State(f"page-{page_id}-ts-data", "data"),
        State(f"page-{page_id}-rate-data", "data"),
        prevent_initial_call=True,
    )
    def render_content(tab, ts_data, rate_data):
        df_ts = pd.DataFrame(ts_data["data-frame"])
        df_rate = pd.DataFrame(rate_data["data-frame"])

        # Make figs
        fig_ts = make_bcl_ts_fig(df_ts, tab)
        fig_rate = make_rate_fig(df_rate, tab)
        div_fig = html.Div([dcc.Graph(figure=fig_ts), dcc.Graph(figure=fig_rate)])
        return div_fig
