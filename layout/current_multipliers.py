from dash import html, dcc
import dash_bootstrap_components as dbc

from components.slider import make_slider
from utils.constants import PARAM_NAMES_CURRENT_MULTIPLIERS
from utils.presets import PARAMETER_PRESETS


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


def make_current_multiplier_section(page_id):
    # Make sliders for current multipliers
    list_sliders = []
    for param_name in PARAM_NAMES_CURRENT_MULTIPLIERS:
        # Replace dots with unnderscores
        param_name = param_name.replace(".", "_")
        # Remove the multipliers prefix for the label
        par_label = param_name.replace("multipliers_", "")
        # Use spaces instead of underscores
        par_label = par_label.replace("_", " ")
        if par_label == "ICaLPCa multiplier":
            par_label = "ICaL multiplier"
        slider = make_slider(
            page_id,
            label=par_label,
            id_prefix=param_name,
            default_value=1,
            slider_range=[0, 3],
        )
        list_sliders.append(slider)

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
                            component_id=f"page-{page_id}-cell-type",
                        ),
                        width=4,
                    ),
                    dbc.Col(
                        dropdown_block(
                            label="Preset",
                            options=list(PARAMETER_PRESETS.keys()),
                            default_value="default",
                            component_id=f"page-{page_id}-dropdown-presets",
                        ),
                        width=6,
                    ),
                ]
            ),
            html.Br(),
            html.Div(list_sliders),
        ]
    )
