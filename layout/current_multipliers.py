from dash import html, dcc
import dash_bootstrap_components as dbc

from components.slider import make_slider
from utils.constants import PARAM_NAMES_CURRENT_MULTIPLIERS

# Make sliders for current multipliers
list_sliders = []
for par in PARAM_NAMES_CURRENT_MULTIPLIERS:
    slider = make_slider(
        label=par, id_prefix=par.replace(".", "_"), default_value=1, slider_range=[0, 3]
    )
    list_sliders.append(slider)


def dropdown_block(label, options, default_value, component_id):
    """Reusable block for label + dropdown."""
    return html.Div(
        [
            html.Label(label, style={"fontSize": 14}),
            dcc.Dropdown(
                options=options,
                value=default_value,
                id=component_id,
                clearable=False,
                style={"fontSize": 14},
            ),
        ]
    )


def make_current_multiplier_section():
    return html.Div(
        [
            dcc.Markdown("-----\n**Cell type and current multipliers:**"),
            dbc.Row(
                [
                    dbc.Col(
                        dropdown_block(
                            label="Cell type",
                            # options=["endo", "epi", "mid"],
                            options=[
                                {"label": "endo", "value": 0},
                                {"label": "epi", "value": 1},
                                {"label": "mid", "value": 2},
                            ],
                            default_value=0,
                            component_id="cell_type",
                        ),
                        width=4,
                    ),
                    dbc.Col(
                        dropdown_block(
                            label="Preset",
                            options=["default", "EAD"],
                            default_value="default",
                            component_id="dropdown_presets",
                        ),
                        width=4,
                    ),
                ]
            ),
            html.Br(),
            html.Div(list_sliders),
        ]
    )
