import numpy as np


def find_upward_crossings(x, y, value):
    crossings = []
    for i in range(len(y) - 1):
        y0, y1 = y[i], y[i + 1]
        if y0 < value and y1 >= value:
            # Linear interpolation
            frac = (value - y0) / (y1 - y0)
            x_cross = x[i] + frac * (x[i + 1] - x[i])
            crossings.append(x_cross)
    return crossings


def find_downward_crossings(x, y, value):
    crossings = []
    for i in range(len(y) - 1):
        y0, y1 = y[i], y[i + 1]
        if y0 > value and y1 <= value:
            # Linear interpolation
            frac = (value - y0) / (y1 - y0)
            x_cross = x[i] + frac * (x[i + 1] - x[i])
            crossings.append(x_cross)
    return crossings


def find_local_maxima(arr):
    local_maxima = []
    n = len(arr)

    # Check for edge cases where array length is less than 3
    if n < 3:
        return local_maxima

    for i in range(1, n - 1):
        if arr[i] > arr[i - 1] and arr[i] > arr[i + 1]:
            local_maxima.append(arr[i])

    return local_maxima


def s2_input_to_list(s2_intervals):
    """
    Convert user input for s2 values to list of integers
    If invalid argument, return a single value

    Args:
        s2_intervals: str
            String input by the user.
            Can be a comma seperated list of integers
            or of the form min:max:inc
    Returns
    -------
    list(int)
        List of s2 intervals
    """

    try:
        # Remove any whitepsace
        s2_intervals = s2_intervals.replace(" ", "")

        # Separate arguments
        list_entry = s2_intervals.split(",")

        list_s2_intervals = []
        for entry in list_entry:
            if entry.isnumeric():
                list_s2_intervals.append(int(entry))

            else:
                # Unpack range of values
                low, high, inc = [int(s) for s in entry.split(":")]
                for s2 in np.arange(low, high, inc):
                    list_s2_intervals.append(s2)

    except:
        print("invalid input")
        return []

    return list_s2_intervals


# Test functions
if __name__ == "__main__":
    x = 3
    print(x)
