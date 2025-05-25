from dash import Output, Input, ctx, callback, dcc, State, html
from utils.constants import PLOT_VARIABLE_TAB_LABELS
from utils.figures import make_simulation_fig
import pandas as pd

# ---------
# Callback to sync tabs with variables selected in dropdown box
# ---------


def register_sync_tabs_with_dropdown():
    # This function updates the tabs to match the variables selected in the dropdown box
    # It also sets the default tab to be the first one in the list

    @callback(
        Output("tabs_container_div", "children"), Input("dropdown_plot_vars", "value")
    )
    def display_tabs(plot_vars):
        tabs = [
            dcc.Tab(value=var, label=PLOT_VARIABLE_TAB_LABELS.get(var, var))
            for var in plot_vars
        ]
        children = (
            dcc.Tabs(
                id="tabs",
                value="membrane.v",
                children=tabs,
            ),
        )
        return children


# ---------
# Callback to switch between tabs
# ---------
def register_switch_tabs():

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
