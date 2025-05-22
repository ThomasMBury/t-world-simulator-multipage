from dash import html, dcc
import dash_bootstrap_components as dbc

from components.slider import make_slider


def make_plot_variable_section(variable_names, default_vars):
    return html.Div(
        [
            dcc.Markdown("-----\n**Plot variables:**"),
            dcc.Dropdown(
                id="dropdown_plot_vars",
                options=variable_names,
                value=default_vars,
                multi=True,
                maxHeight=400,
                optionHeight=20,
                style={"fontSize": 12},
            ),
        ]
    )


def make_fig_panel(tabs, div_fig):
    return html.Div(
        [
            html.Div(tabs, id="tabs_container_div"),
            html.Div(id="tabs_container_output_div", children=div_fig),
        ]
    )


def make_run_save_buttons(simulation_data, parameter_data):
    return dbc.Row(
        [
            dbc.Col(
                html.Div(
                    dcc.Loading(
                        id="loading-anim",
                        type="circle",
                        children=html.Div(id="loading-output"),
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
                    id="run_button",
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
                            id="button_savedata",
                            className="d-grid gap-2",
                            n_clicks=0,
                            style={"fontSize": 14},
                        ),
                        dcc.Download(id="download_simulation"),
                        dcc.Download(id="download_parameters"),
                        dcc.Store(id="simulation_data", data=simulation_data),
                        dcc.Store(id="parameter_data", data=parameter_data),
                    ]
                ),
                className="d-grid gap-2",
                width=2,
            ),
        ]
    )
