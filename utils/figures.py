import plotly.express as px
import plotly.graph_objects as go
from utils.constants import PLOT_VARIABLE_Y_LABELS, PLOT_Y_RANGES

cols = px.colors.qualitative.Plotly


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
        fig.add_trace(
            go.Scatter(
                x=df_sim["time"],
                y=df_sim[plot_var],
                showlegend=False,
                mode="lines",
                line={
                    "color": cols[0],
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


def make_rate_fig(df_rate, plot_var):
    line_width = 1

    fig = go.Figure()

    if plot_var == "membrane.v":
        y_var = "apd"
        y_axes_title = "APD90 (ms)"
    elif plot_var == "intracellular_ions.cai":
        y_var = "cat_amplitude"
        y_axes_title = "CaT amplitude"

    fig.add_trace(
        go.Scatter(
            x=df_rate["bcl"],
            y=df_rate[y_var],
            # showlegend=False,
            mode="markers",
            line={
                "color": cols[0],
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


def make_bcl_ts_fig(df_ts, plot_var):
    line_width = 1

    fig = px.line(df_ts, x="time", y=plot_var, color="bcl")

    fig.update_xaxes(title="Time (ms)")

    fig.update_traces(line={"width": line_width})

    fig.update_layout(
        height=400,
        margin={"l": 20, "r": 20, "t": 30, "b": 20},
    )

    return fig


def make_s1s2_fig(df_ts, plot_var):
    line_width = 1

    fig = px.line(df_ts, x="time", y=plot_var, color="s2_interval")

    fig.update_xaxes(title="Time (ms)")

    fig.update_traces(line={"width": line_width})

    fig.update_layout(
        height=400,
        margin={"l": 20, "r": 20, "t": 30, "b": 20},
    )

    return fig


def make_restitution_fig(df_restitution, plot_var):
    line_width = 1

    fig = go.Figure()

    if plot_var == "membrane.v":
        y_var = "apd"
        y_axes_title = "APD90 (ms)"
    elif plot_var == "intracellular_ions.cai":
        y_var = "cat_amplitude"
        y_axes_title = "CaT amplitude"

    fig.add_trace(
        go.Scatter(
            x=df_restitution["di"],
            y=df_restitution[y_var],
            # showlegend=False,
            mode="lines+markers",
            line={
                "color": cols[0],
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
