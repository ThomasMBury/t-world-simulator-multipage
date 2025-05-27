import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__)


layout = dbc.Container(
    [
        html.H1("User guide", className="my-4"),
        html.H2("Table of Contents", className="mt-5"),
        html.Ul(
            [
                html.Li(html.A("Overview", href="#overview")),
                html.Li(html.A("Features", href="#features")),
                html.Li(html.A("Installation", href="#installation")),
                html.Ul(
                    [
                        html.Li(html.A("Online Access", href="#online-access")),
                        html.Li(
                            html.A(
                                "Offline Access - Installation Instructions",
                                href="#offline-access",
                            )
                        ),
                    ]
                ),
                html.Li(html.A("Tips for Use", href="#usage")),
                html.Li(html.A("License", href="#license")),
                html.Li(html.A("Feedback", href="#feedback")),
            ]
        ),
        html.H2("Overview", id="overview", className="mt-5"),
        html.P(
            [
                "Welcome to ",
                html.Strong("T-World Simulator"),
                "! This web application accompanies ",
                html.A(
                    "T-world",
                    href="https://elifesciences.org/articles/48890",
                    target="_blank",
                ),
                " — a state-of-the-art computational model for a human ventricular myocyte. "
                "It provides an interface for exploring different stimulation protocols, "
                "visualizing membrane voltage and conduction traces, and experimenting with model parameters.",
            ]
        ),
        html.H2("Features", id="features", className="mt-5"),
        html.Ul(
            [
                html.Li(
                    "Stimulation Protocols: Regular pacing, S1-S2 pacing, multiple rates, and pacing with a pause."
                ),
                html.Li(
                    "Parameter Variations: Channel conductances, extracellular concentrations, phosphorylation levels."
                ),
                html.Li(
                    "Visualizations: Voltage/conduction traces and restitution curves."
                ),
                html.Li(
                    "Data Export: CSV downloads of simulation results and parameters."
                ),
            ]
        ),
        html.P(
            [
                "Built with ",
                html.A("Dash", href="https://dash.plotly.com/", target="_blank"),
                " and ",
                html.A("Myokit", href="https://www.myokit.org/", target="_blank"),
                ".",
            ]
        ),
        html.H2("Installation", id="installation", className="mt-5"),
        html.H4("Online Access", id="online-access"),
        html.P("You can access T-World Simulator online without installation at:"),
        dcc.Markdown(
            "[https://t-world.up.railway.app/](https://t-world.up.railway.app/)"
        ),
        html.P("Online limitations include:"),
        html.Ul(
            [
                html.Li("Max pre-pacing beats: 500"),
                html.Li("Max S2 interval values: 50"),
                html.Li("Max basic cycle length values: 50"),
            ]
        ),
        html.H4(
            "Offline Access - Installation Instructions",
            id="offline-access",
            className="mt-4",
        ),
    ],
    style={"zoom": "0.8"},
)
