from dash import html, dcc
import dash_bootstrap_components as dbc

from components.slider import make_slider
from utils.constants import PARAM_NAMES_PKA

# Make sliders for phosphorylation levels
list_sliders_pka = []
for param_name in PARAM_NAMES_PKA:
    # Replace dots with underscores
    param_name = param_name.replace(".", "_")
    # Remove the PKA prefix and suffix for the label
    param_label = param_name.replace("PKA_f", "")
    param_label = param_label.replace("_PKA", " phosphorylation")
    slider = make_slider(
        label=param_label, id_prefix=param_name, default_value=0, slider_range=[0, 1]
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
