import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/")


layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1(
                    "Welcome to T-World Online",
                    className="text-center mt-5 mb-4",
                ),
                width=12,
            )
        ),
        dbc.Row(
            dbc.Col(
                html.P(
                    "This application allows users to run simulations of T-World: A computational model of the human ventricular cardiomycyte. "
                    "Get started by selecting a protocol, setting parameters and clicking RUN.",
                    className="lead text-center",
                ),
                width=10,
                className="mx-auto",
            )
        ),
        dbc.Row(
            dbc.Col(
                html.Img(
                    src="/assets/homepage_banner2.png",
                    style={
                        "maxWidth": "80%",
                        "height": "auto",
                        "border-radius": "8px",
                        "display": "block",
                        "margin": "0 auto",
                    },
                ),
                className="mb-4",
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button(
                    "Get Started",
                    color="primary",
                    size="lg",
                    href="/app-reg-stim",
                    className="mt-4 d-block mx-auto",
                ),
                width=12,
            )
        ),
        dbc.Row(
            dbc.Col(
                html.Footer(
                    [
                        "Created by ",
                        html.A(
                            "Thomas Bury",
                            href="https://www.thomasbury.net/",
                            target="_blank",
                            className="text-decoration-underline text-muted",
                        ),
                        " and ",
                        html.A(
                            "Jakub Tomek",
                            href="https://www.dpag.ox.ac.uk/team/jakub-tomek",
                            target="_blank",
                            className="text-decoration-underline text-muted",
                        ),
                        " | Powered by Dash & Myokit",
                    ],
                    className="text-center mt-5 mb-3",
                ),
                width=12,
            )
        ),
    ],
    # fluid=True,
)
