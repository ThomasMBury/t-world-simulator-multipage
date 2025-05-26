from dash import html, dcc
import dash_bootstrap_components as dbc

from components.slider import make_slider

from utils.model import VARIABLE_NAMES

from utils.constants import PLOT_VARIABLES_DEFAULT


def make_plot_variable_section(page_id):
    return html.Div(
        [
            dcc.Markdown("-----\n**Plot variables:**"),
            dcc.Dropdown(
                id=f"page-{page_id}-dropdown-plot-vars",
                options=VARIABLE_NAMES,
                value=PLOT_VARIABLES_DEFAULT,
                multi=True,
                maxHeight=400,
                optionHeight=20,
                style={"fontSize": 12},
            ),
        ]
    )


def make_fig_panel(page_id, tabs, div_fig):
    return html.Div(
        [
            html.Div(tabs, id=f"page-{page_id}-tabs-container-div"),
            html.Div(id=f"page-{page_id}-tabs-container-output-div", children=div_fig),
        ]
    )


def make_run_save_buttons(page_id, simulation_data, parameter_data):
    return dbc.Row(
        [
            dbc.Col(
                html.Div(
                    dcc.Loading(
                        id=f"page-{page_id}-loading-anim",
                        type="circle",
                        children=html.Div(id=f"page-{page_id}-loading-output"),
                    ),
                    style={
                        "paddingTop": "20px",
                        "paddingBottom": "10px",
                        "verticalAlign": "middle",
                    },
                ),
                width={"size": 1, "offset": 7},
            ),
            dbc.Col(
                dbc.Button(
                    "Run",
                    id=f"page-{page_id}-run-button",
                    color="success",
                    n_clicks=0,
                    style={"fontSize": 14},
                ),
                className="d-grid gap-2",
                width=2,
            ),
            dbc.Col(
                html.Div(
                    [
                        dbc.Button(
                            "Save data",
                            id=f"page-{page_id}-button-savedata",
                            className="d-grid gap-2",
                            n_clicks=0,
                            style={"fontSize": 14},
                        ),
                        dcc.Download(id=f"page-{page_id}-download-simulation"),
                        dcc.Download(id=f"page-{page_id}-download-parameters"),
                        dcc.Store(
                            id=f"page-{page_id}-simulation-data", data=simulation_data
                        ),
                        dcc.Store(
                            id=f"page-{page_id}-parameter-data", data=parameter_data
                        ),
                    ]
                ),
                className="d-grid gap-2",
                width=2,
            ),
        ]
    )
