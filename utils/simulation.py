import numpy as np
import pandas as pd
import myokit as myokit
from utils.helpers import (
    find_local_maxima,
    s2_input_to_list,
    find_downward_crossings,
    find_upward_crossings,
)
from utils.constants import (
    STIM_DURATION_DEFAULT,
    STIM_AMPLIUDE_DEFAULT,
    STIM_LEVEL_DEFAULT,
)


def sim_model(
    s,
    initial_values,
    plot_vars,
    params={},
    bcl=1000,
    total_beats=100,
    show_last_beats=4,
):
    """
    Simulate Torord model

    Parameters
    ----------

    s : simulation class (myokit.Simulation)
    initial_values : list
    params : dict
        Dictionary of user-defined model parameter values. Those that are not
        specified are set to default.
    bcl : float
        basic cycle length
    total_beats : int
        total number of beats to simulate
    beats_kepp: int
        number of beats to display in figure (from the end of the simulation)

    Returns
    -------
    df_sim : pd.DataFrame
        Dataframe of variables at each time value.

    """

    # Assign parameters to simulation object
    for key in params.keys():
        s.set_constant(key, params[key])

    # Set pacing protocol and assign to simulation object
    p = myokit.pacing.blocktrain(bcl, duration=STIM_DURATION_DEFAULT, offset=0)
    s.set_protocol(p)

    # Pre-pacing simulation
    num_beats_pre = max(total_beats - show_last_beats, 0)
    print("Begin prepacing")
    s.pre(num_beats_pre * bcl)

    # Pacing simulation
    print("Begin recorded simulation")
    d = s.run(bcl * show_last_beats)

    # Collect data specified in plot_vars
    data_dict = {key: d[key] for key in (["environment.time"] + plot_vars)}
    df_sim = pd.DataFrame(data_dict)

    # Reset simulation (don't use s.reset as this only goes to end of pre-pacing)
    s.set_state(initial_values)
    s.set_time(0)

    return df_sim


def sim_s1s2_restitution(
    s,
    initial_values,
    params={},
    s1_interval=1000,
    s1_nbeats=10,
    s2_intervals="300:500:20, 500:1000:50",
    num_s2_intervals_max=50,
):
    """
    Simulate Torord model usign S1S2 stimulation protocol for a range of S2 values
    Allow a max number S2 values (to aviod overloading machine)
    Return time series of final S1 stimulation followed by single S2 stimulation
    Return data on APD and CaT amplitude as a function of S2 interval

    Parameters
    ----------

    s : simulation class (myokit.Simulation)
    params : dict
        Dictionary of user-defined model parameter values. Those that are not
        specified are set to default.
    s1_interval : int
    s1_nbeats : int
        number of s1 beats (prepacing)
    s2_intervals: str
        String input by the user that provides s2 values

    Returns
    -------
    df_ts : pd.DataFrame
        time series
    df_restitution: pd.DataFrame
        apd, di and cat_amplitude as a function of S1

    """

    # Unpack S2 values
    list_s2_intervals = s2_input_to_list(s2_intervals)

    # If too many - only work with last 50 vals
    if len(list_s2_intervals) > num_s2_intervals_max:
        list_s2_intervals = list_s2_intervals[:num_s2_intervals_max]
        print("too many s2 intervals given")

    # Only take values greater than 0
    list_s2_intervals = [s2 for s2 in list_s2_intervals if s2 > 0]

    # Get default state of model
    # default_state = s.default_state()

    # Assign parameters to simulation object
    for key in params.keys():
        s.set_constant(key, params[key])

    # Pre-pacing with S1 interval (only needs to be done once)
    p = myokit.pacing.blocktrain(s1_interval, duration=STIM_DURATION_DEFAULT, offset=0)
    s.set_protocol(p)
    s.pre(s1_nbeats * s1_interval)

    list_df = []
    list_di_vals = []
    list_apd_vals = []
    list_cat_amplitude_vals = []

    for s2_interval in list_s2_intervals:
        # Set pacing protocol
        p = myokit.Protocol()
        # Single S1 stimulus
        p.schedule(level=STIM_LEVEL_DEFAULT, start=0, duration=STIM_DURATION_DEFAULT)
        # Single S2 stimulus
        p.schedule(
            level=STIM_LEVEL_DEFAULT, start=s2_interval, duration=STIM_DURATION_DEFAULT
        )

        # Update protoocl
        s.set_protocol(p)

        # Pacing simulation
        d = s.run(2 * s1_interval)

        # Collect data
        data_dict = {}
        data_dict["environment.time"] = d["environment.time"]
        data_dict["membrane.v"] = d["membrane.v"]
        data_dict["intracellular_ions.cai"] = d["intracellular_ions.cai"]
        df = pd.DataFrame(data_dict)
        df["s2_interval"] = s2_interval
        list_df.append(df)

        voltage_vals = d["membrane.v"]
        time_vals = d["environment.time"]

        # # Compute APD and DI using 90% repolarization threshold of S1 beat
        # vmin = np.min(voltage_vals)
        # vmax = np.max(voltage_vals)
        # threshold_v = vmin + 0.1 * (vmax - vmin)

        # Compute APD and DI using -70 mV threshold
        threshold_v = -70

        # Times where voltage crosses zero going upwards
        crossings_ap_upwards = find_upward_crossings(time_vals, voltage_vals, 0)

        # Times where voltage crosses APD threshold
        crossings_thresh_upwards = find_upward_crossings(
            time_vals, voltage_vals, threshold_v
        )
        crossings_thresh_downwards = find_downward_crossings(
            time_vals, voltage_vals, threshold_v
        )

        # Must be 2 upwards crossings at zero voltage to determine DI and APD
        if (len(crossings_ap_upwards) == 2) & (len(crossings_thresh_upwards) == 2):
            # Get DI and APD info
            di = crossings_thresh_upwards[1] - crossings_thresh_downwards[0]
            apd = crossings_thresh_downwards[1] - crossings_thresh_upwards[1]
            # Assert that di and apd are positive
            if di < 0 or apd < 0:
                raise ValueError("DI or APD cannot be negative")

        else:
            di = np.nan
            apd = np.nan

        list_di_vals.append(di)
        list_apd_vals.append(apd)

        # Get calcium transient amplitude (the one after S2)
        local_maxima = find_local_maxima(d["intracellular_ions.cai"])
        # Require at least two peaks
        if len(local_maxima) >= 2:
            cat_amplitude = local_maxima[1]
        else:
            cat_amplitude = np.nan

        list_cat_amplitude_vals.append(cat_amplitude)

        # Reset simulation to pre-paced state
        s.reset()

    df_restitution = pd.DataFrame(
        {
            "s2_interval": list_s2_intervals,
            "di": list_di_vals,
            "apd": list_apd_vals,
            "cat_amplitude": list_cat_amplitude_vals,
        }
    )
    if len(list_df) == 0:
        df_ts = pd.DataFrame(
            columns=[
                "environment.time",
                "membrane.v",
                "intracellular_ions.cai",
                "s2_interval",
            ]
        )
    else:
        df_ts = pd.concat(list_df)

    # Reset simulation completely (including prepacing)
    s.set_state(initial_values)
    s.set_time(0)

    return df_ts, df_restitution


def sim_rate_change(
    s,
    initial_values,
    params={},
    bcl_values="250:500:50, 500:1000:100",
    nbeats=10,
    num_bcl_values_max=50,
):
    """
    Simulate Torord model for a range of bcl values
    Restrict to a max number  bcl values (to aviod overloading machine)
    Return data on APD and CaT amplitude as a function of bcl
    Reset model to initial state before prepacing.

    Parameters
    ----------

    s : simulation class (myokit.Simulation)
    params : dict
        Dictionary of user-defined model parameter values. Those that are not
        specified are set to default.
    bcl_values: str
        String input by the user that provides bcl values
    nbeats : int
        number of pulses

    Returns
    -------
    df_rate: pd.DataFrame
        apd and cat_amplitude as a function of bcl

    """

    # Unpack S2 values
    list_bcl_values = s2_input_to_list(bcl_values)

    # If too many - only work with last 20 vals
    if len(list_bcl_values) > num_bcl_values_max:
        list_bcl_values = list_bcl_values[:num_bcl_values_max]

    # Only take values greater than 0
    list_bcl_values = [s2 for s2 in list_bcl_values if s2 > 0]

    # Assign parameters to simulation object
    for key in params.keys():
        s.set_constant(key, params[key])

    list_df = []
    list_apd_vals = []
    list_cat_amplitude_vals = []

    for bcl in list_bcl_values:

        # Pre-pacing
        p = myokit.pacing.blocktrain(
            bcl, duration=STIM_DURATION_DEFAULT, level=STIM_LEVEL_DEFAULT, offset=0
        )
        s.set_protocol(p)
        s.pre(nbeats * bcl)

        # Set pacing protocol
        p = myokit.Protocol()
        # Schedule 4 stimuli
        p.schedule(level=STIM_LEVEL_DEFAULT, start=0, duration=STIM_DURATION_DEFAULT)
        p.schedule(level=STIM_LEVEL_DEFAULT, start=bcl, duration=STIM_DURATION_DEFAULT)
        p.schedule(
            level=STIM_LEVEL_DEFAULT, start=2 * bcl, duration=STIM_DURATION_DEFAULT
        )
        p.schedule(
            level=STIM_LEVEL_DEFAULT, start=3 * bcl, duration=STIM_DURATION_DEFAULT
        )

        # Update protoocl
        s.set_protocol(p)

        # Pacing simulation
        d = s.run(4 * bcl)

        # Collect data
        data_dict = {}
        data_dict["environment.time"] = d["environment.time"]
        data_dict["membrane.v"] = d["membrane.v"]
        data_dict["intracellular_ions.cai"] = d["intracellular_ions.cai"]
        df = pd.DataFrame(data_dict)
        df["bcl"] = bcl
        list_df.append(df)

        voltage_vals = d["membrane.v"]
        time_vals = d["environment.time"]
        # # Compute APD and DI using 90% repolarization threshold of S1 beat
        # vmin = np.min(voltage_vals)
        # vmax = np.max(voltage_vals)
        # threshold_v = vmin + 0.1 * (vmax - vmin)

        # Compute APD and DI using -70 mV threshold
        threshold_v = -70

        # Times where voltage crosses zero going upwards
        crossings_ap_upwards = find_upward_crossings(time_vals, voltage_vals, 0)

        # Times where voltage crosses APD threshold
        crossings_thresh_upwards = find_upward_crossings(
            time_vals, voltage_vals, threshold_v
        )
        crossings_thresh_downwards = find_downward_crossings(
            time_vals, voltage_vals, threshold_v
        )

        crossings_ap_upwards = find_upward_crossings(time_vals, voltage_vals, 0)
        crossings_thresh_upwards = find_upward_crossings(
            time_vals, voltage_vals, threshold_v
        )
        crossings_thresh_downwards = find_downward_crossings(
            time_vals, voltage_vals, threshold_v
        )

        # Must be 4 upwards crossings at zero voltage to determine APD
        if (len(crossings_ap_upwards) == 4) & (len(crossings_thresh_upwards) == 4):
            # Get DI and APD info
            ap1_start = crossings_thresh_upwards[0]
            ap1_end = crossings_thresh_downwards[0]
            ap2_start = crossings_thresh_upwards[1]
            ap2_end = crossings_thresh_downwards[1]
            ap3_start = crossings_thresh_upwards[2]
            ap3_end = crossings_thresh_downwards[2]
            ap4_start = crossings_thresh_upwards[3]
            ap4_end = crossings_thresh_downwards[3]
            apd1 = ap1_end - ap1_start
            apd2 = ap2_end - ap2_start
            apd3 = ap3_end - ap3_start
            apd4 = ap4_end - ap4_start

        else:
            apd1 = np.nan
            apd2 = np.nan
            apd3 = np.nan
            apd4 = np.nan

        list_apd_vals.append(apd1)
        list_apd_vals.append(apd2)
        list_apd_vals.append(apd3)
        list_apd_vals.append(apd4)

        # Compute calcium transient amplitude
        local_maxima = find_local_maxima(d["intracellular_ions.cai"])
        # Require at least two peaks
        if len(local_maxima) >= 4:
            cat1, cat2, cat3, cat4 = local_maxima[:4]
        else:
            cat1, cat2, cat3, cat4 = np.nan, np.nan, np.nan, np.nan

        list_cat_amplitude_vals.append(cat1)
        list_cat_amplitude_vals.append(cat2)
        list_cat_amplitude_vals.append(cat3)
        list_cat_amplitude_vals.append(cat4)

        # Reset simulation to state that was before pre-pacing
        s.set_state(initial_values)
        s.set_time(0)

    df_rate = pd.DataFrame(
        {
            "bcl": [bcl for bcl in list_bcl_values for _ in range(4)],
            "apd": list_apd_vals,
            "cat_amplitude": list_cat_amplitude_vals,
        }
    )

    if len(list_df) == 0:
        df_ts = pd.DataFrame(
            columns=["environment.time", "membrane.v", "intracellular_ions.cai", "bcl"]
        )
    else:
        df_ts = pd.concat(list_df)

    return df_ts, df_rate


def sim_model_dad(
    s,
    initial_values,
    plot_vars,
    params={},
    bcl=1000,
    total_beats=100,
    quiescence_duration=5,
):
    """
    Simulate Torord model
    Period of stimulation followed by period of quiescence
    Keep the last 2 beats that were stimulated, then simulate for another quiescence_duration seconds

    Parameters
    ----------

    s : simulation class (myokit.Simulation)
    params : dict
        Dictionary of user-defined model parameter values. Those that are not
        specified are set to default.
    bcl : float
        basic cycle length
    total_beats : int
        total number of beats to simulate
    quiescence_duration: int
        duration after stimulation to keep running simulation

    Returns
    -------
    df : pd.DataFrame
        Dataframe of variables at each time value.

    """

    # Assign parameters to simulation object
    for key in params.keys():
        s.set_constant(key, params[key])

    # Set pacing protocol and assign to simulation object
    p = myokit.pacing.blocktrain(bcl, duration=STIM_DURATION_DEFAULT, offset=0)
    s.set_protocol(p)

    # Pre-pacing simulation
    num_beats_pre = max(total_beats - 2, 0)
    print("Begin prepacing")
    s.pre(num_beats_pre * bcl)

    # Pacing simulation
    print("Begin recorded simulation")
    log = s.run(bcl * 2)

    # Quiescence
    s.set_protocol(None)
    log = s.run(quiescence_duration * 1000, log=log)

    # Collect data specified in plot_vars
    data_dict = {key: log[key] for key in (["environment.time"] + plot_vars)}
    df = pd.DataFrame(data_dict)

    # Reset simulation (don't use s.reset as this only goes to end of pre-pacing)
    s.set_state(initial_values)
    s.set_time(0)

    return df
