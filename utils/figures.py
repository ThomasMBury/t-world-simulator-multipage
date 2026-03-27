import plotly.express as px
import plotly.graph_objects as go
from utils.constants import PLOT_VARIABLE_Y_LABELS, PLOT_Y_RANGES
from itertools import cycle

colors = px.colors.qualitative.Plotly


def make_simulation_fig(df_sim, plot_var):
    """
    Make figure showing variable vs time
    If plot_var is not in df_sim, output empty graph

    Parameters
    ----------
    df_sim : pd.DataFrame
        simulation data of model
    var_plot : variable to plot

    Returns
    -------
    fig

    """

    line_width = 1

    fig = go.Figure()

    if plot_var in df_sim.columns:

        # If plotting Cai, scale from mM to nM for better visualization
        if plot_var == "intracellular_ions.cai":
            df_sim[plot_var] = df_sim[plot_var] * 1e6

        fig.add_trace(
            go.Scatter(
                x=df_sim["environment.time"],
                y=df_sim[plot_var],
                showlegend=False,
                mode="lines",
                line={
                    "color": colors[0],
                    "width": line_width,
                },
            ),
        )

    fig.update_xaxes(title="Time (ms)")
    fig.update_yaxes(
        title=PLOT_VARIABLE_Y_LABELS.get(plot_var, plot_var),
        range=PLOT_Y_RANGES.get(plot_var, None),
    )

    fig.update_layout(
        height=600,
        margin={"l": 20, "r": 20, "t": 30, "b": 20},
    )

    return fig


def make_bcl_ts_fig(df_ts, plot_var):
    line_width = 1

    color_cycle = cycle(colors)

    fig = go.Figure()

    if plot_var in df_ts.columns:

        # If plotting Cai, scale from mM to nM for better visualization
        if plot_var == "intracellular_ions.cai":
            df_ts[plot_var] = df_ts[plot_var] * 1e6

        for idx, bcl in enumerate(df_ts["bcl"].unique()):
            df_bcl = df_ts[df_ts["bcl"] == bcl]
            fig.add_trace(
                go.Scatter(
                    x=df_bcl["environment.time"],
                    y=df_bcl[plot_var],
                    name=f"{bcl}",
                    mode="lines",
                    line={
                        "color": next(color_cycle),
                        "width": line_width,
                    },
                    visible="legendonly" if idx > 0 else True,
                ),
            )
    fig.update_xaxes(title="Time (ms)")
    fig.update_yaxes(
        title=PLOT_VARIABLE_Y_LABELS.get(plot_var, plot_var),
        range=PLOT_Y_RANGES.get(plot_var, None),
    )
    fig.update_traces(line={"width": line_width})

    fig.update_layout(
        height=400,
        margin={"l": 20, "r": 20, "t": 30, "b": 20},
        legend=dict(title="BCL (ms)"),
    )

    return fig


def make_rate_fig(df_rate, plot_var):

    line_width = 1
    fig = go.Figure()

    if plot_var == "membrane.v":
        y_var = "apd"
        y_axes_title = "APD (ms)"
    elif plot_var == "intracellular_ions.cai":
        y_var = "cat_amplitude"
        y_axes_title = "CaT amplitude (nM)"

    if ("apd" in df_rate.columns) | ("cat_amplitude" in df_rate.columns):

        # If plotting Cai, scale from mM to nM for better visualization
        if plot_var == "intracellular_ions.cai":
            df_rate[y_var] = df_rate[y_var] * 1e6

        fig.add_trace(
            go.Scatter(
                x=df_rate["bcl"],
                y=df_rate[y_var],
                # showlegend=False,
                mode="markers",
                line={
                    "color": colors[0],
                    "width": line_width,
                },
            ),
        )

    fig.update_xaxes(title="BCL (ms)")
    fig.update_yaxes(title=y_axes_title)

    fig.update_layout(
        height=400,
        margin={"l": 20, "r": 20, "t": 30, "b": 20},
    )

    return fig


def make_s1s2_fig(df_ts, plot_var):
    line_width = 1
    fig = go.Figure()

    color_cycle = cycle(colors)

    if plot_var in df_ts.columns:

        # If plotting Cai, scale from mM to nM for better visualization
        if plot_var == "intracellular_ions.cai":
            df_ts[plot_var] = df_ts[plot_var] * 1e6

        for idx, s2_interval in enumerate(df_ts["s2_interval"].unique()):
            df_s2 = df_ts[df_ts["s2_interval"] == s2_interval]
            fig.add_trace(
                go.Scatter(
                    x=df_s2["environment.time"],
                    y=df_s2[plot_var],
                    name=f"{s2_interval}",
                    mode="lines",
                    line={
                        "color": next(color_cycle),
                        "width": line_width,
                    },
                    visible="legendonly" if idx > 0 else True,
                ),
            )

    fig.update_xaxes(title="Time (ms)")
    fig.update_yaxes(
        title=PLOT_VARIABLE_Y_LABELS.get(plot_var, plot_var),
        range=PLOT_Y_RANGES.get(plot_var, None),
    )

    fig.update_traces(line={"width": line_width})

    fig.update_layout(
        height=400,
        margin={"l": 20, "r": 20, "t": 30, "b": 20},
        legend=dict(title="S2 interval (ms)"),
    )
    return fig


def make_restitution_fig(df_restitution, plot_var):
    line_width = 1
    add_trace = False

    fig = go.Figure()

    if plot_var == "membrane.v":
        y_var = "apd"
        y_axes_title = "APD (ms)"
    elif plot_var == "intracellular_ions.cai":
        y_var = "cat_amplitude"
        y_axes_title = "CaT amplitude (nM)"

    if ("apd" in df_restitution.columns) | ("cat_amplitude" in df_restitution.columns):

        # If plotting Cai, scale from mM to nM for better visualization
        if plot_var == "intracellular_ions.cai":
            df_restitution[y_var] = df_restitution[y_var] * 1e6

        fig.add_trace(
            go.Scatter(
                x=df_restitution["di"],
                y=df_restitution[y_var],
                # showlegend=False,
                mode="lines+markers",
                line={
                    "color": colors[0],
                    "width": line_width,
                },
            ),
        )

    fig.update_xaxes(title="DI (ms)")
    fig.update_yaxes(title=y_axes_title)

    fig.update_layout(
        height=400,
        margin={"l": 20, "r": 20, "t": 30, "b": 20},
    )

    return fig
