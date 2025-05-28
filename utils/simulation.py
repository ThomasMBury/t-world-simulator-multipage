import numpy as np
import pandas as pd
import myokit as myokit
from utils.helpers import find_crossings, find_local_maxima, s2_input_to_list


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
    df : pd.DataFrame
        Dataframe of variables at each time value.

    """

    # Assign parameters to simulation object
    for key in params.keys():
        s.set_constant(key, params[key])

    # Set pacing protocol and assign to simulation object
    p = myokit.pacing.blocktrain(bcl, duration=1.0, offset=0)
    s.set_protocol(p)

    # Pre-pacing simulation
    num_beats_pre = max(total_beats - show_last_beats, 0)
    print("Begin prepacing")
    s.pre(num_beats_pre * bcl)

    # Pacing simulation
    print("Begin recorded simulation")
    d = s.run(bcl * show_last_beats)

    # Collect data specified in plot_vars
    data_dict = {key: d[key] for key in plot_vars}
    data_dict["time"] = d["environment.time"]
    df = pd.DataFrame(data_dict)

    # Reset simulation (don't use s.reset as this only goes to end of pre-pacing)
    s.set_state(initial_values)
    s.set_time(0)

    return df


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
    default_state = s.default_state()

    # Assign parameters to simulation object
    for key in params.keys():
        s.set_constant(key, params[key])

    # Pre-pacing with S1 interval (only needs to be done once)
    p = myokit.pacing.blocktrain(s1_interval, duration=0.5, offset=0)
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
        p.schedule(level=1.0, start=0, duration=0.5)
        # Single S2 stimulus
        p.schedule(level=1.0, start=s2_interval, duration=0.5)

        # Update protoocl
        s.set_protocol(p)

        # Pacing simulation
        d = s.run(2 * s1_interval)

        # Collect data
        data_dict = {}
        data_dict["membrane.v"] = d["membrane.v"]
        data_dict["time"] = d["environment.time"]
        data_dict["intracellular_ions.cai"] = d["intracellular_ions.cai"]
        df = pd.DataFrame(data_dict)
        df["s2_interval"] = s2_interval
        list_df.append(df)

        # Compute APD and DI using 90% repolarization threshold of S1 beat
        voltage_vals = d["membrane.v"]
        time_vals = d["environment.time"]
        vmin = np.min(voltage_vals)
        vmax = np.max(voltage_vals)
        threshold_v = vmin + 0.1 * (vmax - vmin)
        # thresh_apd = -77  # mV - threshold for computing APD
        crossings_ap = find_crossings(
            voltage_vals, 0
        )  # places where voltage crosses zero
        crossings_thresh = find_crossings(
            voltage_vals, threshold_v
        )  # places where voltage crosses repolarization threshold

        # Must be 4 crossings at zero voltage to determine DI and APD
        if (len(crossings_ap) == 4) & (len(crossings_thresh) == 4):
            # Get DI and APD info
            di_start = crossings_thresh[1]
            di_end = crossings_thresh[2]
            ap_end = crossings_thresh[3]
            di = time_vals[di_end] - time_vals[di_start]
            apd = time_vals[ap_end] - time_vals[di_end]

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
            columns=["membrane.v", "time", "intracellular_ions.cai", "s2_interval"]
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
        p = myokit.pacing.blocktrain(bcl, duration=0.5, offset=0)
        s.set_protocol(p)
        s.pre(nbeats * bcl)

        # Set pacing protocol
        p = myokit.Protocol()
        # Schedule 4 stimuli
        p.schedule(level=1.0, start=0, duration=0.5)
        p.schedule(level=1.0, start=bcl, duration=0.5)
        p.schedule(level=1.0, start=2 * bcl, duration=0.5)
        p.schedule(level=1.0, start=3 * bcl, duration=0.5)

        # Update protoocl
        s.set_protocol(p)

        # Pacing simulation
        d = s.run(4 * bcl)

        # Collect data
        data_dict = {}
        data_dict["membrane.v"] = d["membrane.v"]
        data_dict["time"] = d["environment.time"]
        data_dict["intracellular_ions.cai"] = d["intracellular_ions.cai"]
        df = pd.DataFrame(data_dict)
        df["bcl"] = bcl
        list_df.append(df)

        # Compute APD using 90% repolarization threshold
        voltage_vals = d["membrane.v"]
        time_vals = d["environment.time"]
        vmin = np.min(voltage_vals)
        vmax = np.max(voltage_vals)
        threshold_v = vmin + 0.1 * (vmax - vmin)
        # thresh_apd = -77  # mV - threshold for computing APD
        crossings_ap = find_crossings(
            voltage_vals, 0
        )  # places where voltage crosses zero
        crossings_thresh = find_crossings(
            voltage_vals, threshold_v
        )  # places where voltage crosses repolarization threshold

        # Must be 8 crossings at zero voltage to determine APD
        if (len(crossings_ap) == 8) & (len(crossings_thresh) == 8):
            # Get DI and APD info
            ap1_start = crossings_thresh[0]
            ap1_end = crossings_thresh[1]
            ap2_start = crossings_thresh[2]
            ap2_end = crossings_thresh[3]
            ap3_start = crossings_thresh[4]
            ap3_end = crossings_thresh[5]
            ap4_start = crossings_thresh[6]
            ap4_end = crossings_thresh[7]
            apd1 = time_vals[ap1_end] - time_vals[ap1_start]
            apd2 = time_vals[ap2_end] - time_vals[ap2_start]
            apd3 = time_vals[ap3_end] - time_vals[ap3_start]
            apd4 = time_vals[ap4_end] - time_vals[ap4_start]

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
            columns=["membrane.v", "time", "intracellular_ions.cai", "bcl"]
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
    p = myokit.pacing.blocktrain(bcl, duration=1.0, offset=0)
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
    data_dict = {key: log[key] for key in plot_vars}
    data_dict["time"] = log["environment.time"]
    df = pd.DataFrame(data_dict)

    # Reset simulation (don't use s.reset as this only goes to end of pre-pacing)
    s.set_state(initial_values)
    s.set_time(0)

    return df
