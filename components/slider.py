from dash import html, dcc
import dash_bootstrap_components as dbc


def make_slider(label="ICaL", id_prefix="ical", default_value=1, slider_range=[0, 3]):
    """Make a connected slider and input box for a parameter in the model

    Args:
        label: label shown on slider
        id_prefix: prefix for reference ID used in callbacks
        default_value: default value
        slider_range: slider range

    Returns:
        Dash slider object in a Div
    """

    slider = html.Div(
        [
            # Title for slider
            html.Label(
                label,
                id="{}_slider_text".format(id_prefix),
                style={"fontSize": 14},
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            # Slider
                            dcc.Slider(
                                id="{}_slider".format(id_prefix),
                                min=slider_range[0],
                                max=slider_range[1],
                                marks={i: "{}".format(i) for i in range(4)},
                                value=default_value,
                            ),
                        ],
                        width=9,
                    ),
                    dbc.Col(
                        [
                            # Input box
                            dcc.Input(
                                id="{}_box".format(id_prefix),
                                type="number",
                                min=slider_range[0],
                                max=slider_range[1],
                                step=0.001,
                                value=default_value,
                                style=dict(width=80, display="inline-block"),
                            ),
                        ],
                        width=3,
                    ),
                ]
            ),
        ]
    )
    return slider
