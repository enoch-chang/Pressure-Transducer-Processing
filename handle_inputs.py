"""
Author: Enoch Chang

Handling of main user input to handle the two main cases: single or multiple datasets
"""

import file_io
import pressure_processor
from datetime import datetime
import os

def handle_single(dir):
    """ Handles case of when only one file is to be analyzed, executing
    functions for data range selection, plotting and export

    :param dir: Directory of where the data file is located
    :return:
    """

    filename = input("Filename? ")

    try:
        raw_time, pressure, units, start, end, min, max = file_io.read_csv(dir + filename)
    except FileNotFoundError:
        print("Error: File not found in specified directory.")
        return

    start = pressure_processor.normalize_single_time(start)
    end = pressure_processor.normalize_single_time(end) - start

    time = pressure_processor.normalize_time_list(raw_time, start)

    temp = pressure_processor.plot_single_pressure(pressure, time, units)
    temp.show()

    try:
        pressure,time = handle_interval_selection(pressure,time,end)
    except TypeError:
        return

    format = input("Export filetype ('pdf' or 'png'; other input for view "
                    "only) ")

    save_dir = str("./Exported/" + datetime.now().strftime("%Y-%m-%d "
                                                               "%H-%M-%S"))
    os.mkdir(save_dir)

    export_filename = save_dir + '/' + filename + ' ' + '.' + format

    graph = pressure_processor.plot_single_pressure(pressure[0], time[0],
                                                    units)

    file_io.render_figure(graph,[filename],export_filename,format)
    pressure_processor.prepare_output_data(filename,save_dir,pressure[0],
                                           time[0])

    return


def handle_multi(dir, number_of_files):
    """ Handles case of when more than one file is to be analyzed, executing
    functions for data range selection, plotting and export

    :param dir: Directory of where the data file is located
    :param number_of_files: Number of files for analysis
    :return:
    """

    filename_list = input("Filenames? (Please separate using commas) ")

    # filename_list = filename_list.replace(" ", "")
    filename = filename_list.split(",")

    if len(filename) != number_of_files:
        print("Error: Filenames mismatch with number of files specified.")
        return

    format = input("Export filetype ('pdf' or 'png'; other input for view "
                    "only) ")

    try:
        pressure_processor.plot_multi_pressure(dir, filename, format)
    except FileNotFoundError:
        print("Error: One or more files not found in specified directory.")
        return

    return

def handle_interval_selection(pressure,time,end,new_pressure=[],new_time=[]):
    """ Facilitates selection of data range by requesting input, checking
    validity of specified range and calling the function to modify the data
    accordingly

    :param pressure: Original pressure data list
    :param time: Original time data points list
    :param end: Final time point
    :param new_pressure: Multidimensional array to store pressure
    values of separate data sets
    :param new_time: Multidimensional array to store time values of separate
    data sets
    :return: new_pressure and new_time lists, with selected range
    """

    interval_input = input("Close the graph and enter the interval of "
                           "interest in seconds by specifying the start and "
                           "end, separated with a comma ("
                           "e.g. '1, 5.7'; enter 'N' to use the full data set) ")

    interval_input = interval_input.replace(" ", "")

    if interval_input != "N" and interval_input != "n":

        interval = interval_input.split(",")

        if len(interval) != 2:
            print("Error: Please input two numbers.")
            return

        if 0 >= float(interval[0]) or float(end) <= float(
                interval[1]):
            print("Error: Out of range")
            return

        try:
                start, end = [float(interval[0]), float(interval[1])]
        except ValueError:
            print("Error: Please input two numbers.")
            return

        pressure, time = pressure_processor.select_interval(pressure, time,
                                                            start, end)

        new_pressure.append(pressure)
        new_time.append(time)

    return new_pressure,new_time
