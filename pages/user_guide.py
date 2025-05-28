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
                html.Li(html.A("Getting Started", href="#getting-started")),
                html.Li(html.A("Stimulation protocols", href="#stimulation-protocols")),
                html.Ul(
                    [
                        html.Li(html.A("Periodic Pacing", href="#periodic-pacing")),
                        html.Li(
                            html.A(
                                "S1-S2 Restitution",
                                href="#s1-s2-restitution",
                            )
                        ),
                        html.Li(
                            html.A(
                                "Rate Dependence and Alternans", href="#rate-dependence"
                            )
                        ),
                        html.Li(
                            html.A("Delayed Afterdepolarizations (DADs)", href="#dad")
                        ),
                    ]
                ),
                html.Li(html.A("Parameter Controls", href="#parameter-controls")),
                html.Li(html.A("Plotting Window", href="#plotting-window")),
                html.Li(html.A("Exporting Data", href="#exporting-data")),
                html.Li(html.A("Online Limits", href="#online-limits")),
                html.Li(
                    html.A(
                        "Offline Access",
                        href="#offline-access",
                    )
                ),
                html.Li(html.A("Troubleshooting", href="#troubleshooting")),
                html.Li(html.A("Feedback", href="#feedback")),
                html.Li(html.A("License", href="#license")),
                html.Li(html.A("Acknowledgments", href="#acknowledgments")),
            ]
        ),
        html.H2("Overview", id="overview", className="mt-5"),
        html.P(
            [
                "Welcome to ",
                html.Strong("T-World Online"),
                "! This web application accompanies ",
                html.A(
                    "T-world",
                    href="https://www.biorxiv.org/content/10.1101/2025.03.24.645031v1",
                    target="_blank",
                ),
                "—a state-of-the-art computational model of the human ventricular cardiomyocyte. It allows users to simulate the T-World model using a range of stimulation protocols and visualize the outputs. We hope it serves as a valuable tool for both educators and researchers.",
            ]
        ),
        html.H2("Getting Started", id="getting-started", className="mt-5"),
        html.Ol(
            [
                html.Li("Select a pacing protocol from the top navigation bar."),
                html.Li(
                    "Set the desired parameters for the pacing protocol and model using the controls on the left."
                ),
                html.Li(
                    "Choose variables to plot using the dropdown menu above the plotting window."
                ),
                html.Li(
                    [
                        "Click the green ",
                        html.Strong("Run"),
                        " button. A loading ring will appear—your plot will display when it's done.",
                    ]
                ),
            ]
        ),
        html.H2("Stimulation Protocols", id="stimulation-protocols", className="mt-5"),
        html.H4("Periodic Pacing"),
        html.Ul(
            [
                html.Li("Standard, fixed-rate pacing."),
                html.Li(
                    "Configure pacing frequency, number of beats, and how many final beats to display."
                ),
            ]
        ),
        html.H4("S1-S2 Restitution", id="s1-s2-restitution", className="mt-5"),
        html.Ul(
            [
                html.Li(
                    "A sequence of regular stimuli (S1) followed by a single extra stimulus (S2) at varying intervals."
                ),
                html.Li("Useful for constructing restitution curves (APD vs. DI)."),
                html.Li(
                    "Enter ranges in the format min:max:increment (e.g., 300:500:50 → [300, 350, 400, 450])."
                ),
                html.Li("Multiple ranges can be comma-separated."),
                html.Li("APD and DI are computed at 90% repolarization."),
                html.Li(
                    "Upper plot: final two beats per S2 interval; lower plot: restitution curve."
                ),
            ]
        ),
        html.H4(
            "Rate Dependence and Alternans", id="rate-dependence", className="mt-5"
        ),
        html.Ul(
            [
                html.Li("Fixed-rate pacing over a range of cycle lengths."),
                html.Li(
                    "Investigate APD and CaT dependence on pacing frequency and check for alternans."
                ),
                html.Li(
                    "Upper plot: last 4 APs for each pacing frequency; lower plot: APD and CaT amplitude vs. basic cycle length."
                ),
            ]
        ),
        html.H4("Delayed Afterdepolarizations (DADs)", id="dad", className="mt-5"),
        html.Ul(
            [
                html.Li("Fixed-rate pacing followed by quiescence."),
                html.Li(
                    "Configure the number of beats and the quiescence duration to study DAD behavior."
                ),
            ]
        ),
        html.H2("Parameter Controls", id="parameter-controls", className="mt-5"),
        html.P(
            "Located on the left of the app, these allow configuration via sliders, dropdowns, and input fields. Invalid inputs highlight red. Users can:"
        ),
        html.Ul(
            [
                html.Li(
                    "Choose from three cell types: endocardium, epicardium, midmyocardium."
                ),
                html.Li(
                    "Select a preset: default, EAD prone, alternans with low SERCA, DAD prone."
                ),
                html.Li("Adjust current multipliers."),
                html.Li("Set extracellular concentrations."),
                html.Li(
                    "Modify β-adrenergic signaling (β-ARS) via phosphorylation levels."
                ),
            ]
        ),
        html.H2("Plotting Window", id="plotting-window", className="mt-5"),
        html.Ul(
            [
                html.Li("Use dropdowns and tabs to select output variables."),
                html.Li("Note: rerun the simulation when new variables are selected."),
                html.Li("Click-and-drag to zoom; double-click to reset axes."),
                html.Li("Navigation tools appear in the top-right corner of the plot."),
            ]
        ),
        html.H2("Exporting Data", id="exporting-data", className="mt-5"),
        html.P(
            "After running a simulation, click the Save data button to export the simulation and parameters as CSV files."
        ),
        html.H2("Online Limits", id="online-limits", className="mt-5"),
        html.P("Due to limited compute resources, the online version imposes:"),
        html.Ul(
            [
                html.Li("Max no. of pre-pacing beats: 500"),
                html.Li("Max no. of S2 intervals for restitution curve: 50"),
                html.Li("Max no. of BCL values for rate dependent curve: 20"),
            ]
        ),
        html.P("Running the app offline removes these limits."),
        html.H2("Offline Access", id="offline-access", className="mt-5"),
        html.P(
            [
                "Please visit the ",
                html.A(
                    "GitHub respository",
                    href="https://github.com/ThomasMBury/t-world-simulator-multipage",
                    target="_blank",
                ),
                " for installation instructions.",
            ]
        ),
        html.H2("Troubleshooting", id="troubleshooting", className="mt-5"),
        html.Ul(
            [
                html.Li("If unresponsive, refresh your browser."),
                html.Li("Use a modern browser (Chrome, Firefox, Edge, Safari)."),
                html.Li("For slow performance, consider installing the app locally."),
            ]
        ),
        html.H2("Feedback", id="feedback", className="mt-5"),
        html.P(
            [
                "Encounter an issue? Please submit it through ",
                html.A(
                    "GitHub Issues",
                    href="https://github.com/ThomasMBury/t-world-simulator-multipage/issues",
                    target="_blank",
                ),
                ".",
            ]
        ),
        html.H2("License", id="license", className="mt-5"),
        html.P(
            [
                "This project is licensed under the ",
                html.A(
                    "MIT License",
                    href="https://github.com/ThomasMBury/t-world-simulator-multipage/blob/main/LICENSE",
                    target="_blank",
                ),
                ".",
            ]
        ),
        html.H2("Acknowledgements", id="acknowledgments", className="mt-5"),
        html.P(
            [
                "The app is built using ",
                html.A("Dash", href="https://dash.plotly.com/", target="_blank"),
                " and simulations are run using ",
                html.A("myokit", href="https://myokit.org", target="_blank"),
                ".",
                # ". TMB is supported by the FRQNT postdoctoral fellowship (314100). JT is supported by the Sir Henry Wellcome Fellowship (222781/Z/21/Z).",
            ]
        ),
        html.Ul(
            [
                html.Li(
                    "TMB is supported by the FRQNT postdoctoral fellowship (314100)."
                ),
                html.Li(
                    "JT is supported by the Sir Henry Wellcome Fellowship (222781/Z/21/Z)."
                ),
            ]
        ),
    ],
    style={
        "zoom": "0.8",
        "paddingBottom": "50px",
    },
)
