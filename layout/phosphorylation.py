from dash import html, dcc
import dash_bootstrap_components as dbc

from components.slider import make_slider
from utils.constants import PARAMS_PKA

# Make sliders for phosphorylation levels
list_sliders_pka = []
for par in PARAMS_PKA:
    slider = make_slider(
        label=par, id_prefix=par.replace(".", "_"), default_value=0, slider_range=[0, 1]
    )
    list_sliders_pka.append(slider)


def make_phosphorylation_section():

    return html.Div(
        [
            dcc.Markdown("-----\n**Phosphorylation levels**:"),
            html.Div(
                [
                    dbc.Button(
                        "no beta-ARS",
                        id="no-beta-ars",
                        n_clicks=0,
                        color="secondary",
                        style={"margin-right": "15px"},
                    ),
                    dbc.Button(
                        "full beta-ARS",
                        id="full-beta-ars",
                        n_clicks=0,
                        color="secondary",
                    ),
                ]
            ),
            html.Div(list_sliders_pka),
        ]
    )
