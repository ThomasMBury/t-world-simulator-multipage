import dash
from dash import html, dcc, callback, Input, Output

dash.register_page(__name__)

layout = html.Div(
    [
        html.H1("App rate dep"),
        html.Div(
            [
                "Select a city: ",
                dcc.RadioItems(
                    options=["New York City", "Montreal", "San Francisco"],
                    value="Montreal",
                    id="analytics-input",
                ),
            ]
        ),
        html.Br(),
        html.Div(id="analytics-output"),
    ]
)
