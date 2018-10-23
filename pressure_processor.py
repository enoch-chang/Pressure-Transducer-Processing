"""
Author: Enoch Chang

This script contains various functions to process the data, including:
- Modification of time values
- Modification of data range
- Graphical representation of data
- Prepare modified data sets for export
"""

import matplotlib.pyplot as plt
import file_io
from datetime import datetime
import handle_inputs
import os

def normalize_single_time(time):
    """Converts single time value into absolute time

    :param time: Time value in MM-SS
    :return: Time given in seconds
    """
    time_in_seconds=float(time.split(':')[0])*60 + float(time.split(':')[1])

    return time_in_seconds

def normalize_time_list(time, start):
    """Converts time list into absolute time using the start time as a
    reference

    :param time: Time list of values given in MM-SS
    :param start: Start time given in seconds
    :return: Time list with values given in seconds
    """

    normalized_time=[]

    for i in time:
        single = normalize_single_time(i) - start
        normalized_time.append(round(single,2))

    return normalized_time

def select_interval(pressure, time, start, end):
    """Trims time list to only the interval range specified

    :param pressure: List of pressure values
    :param time: List of time values in seconds
    :param start: Beginning time mark to specify interval
    :param end: Ending time mark to specify interval
    :return: pressure and time lists with the specified interval
    """

    time_interval=[]
    pressure_interval=[]

    for count, i in enumerate(time):

        if start < i < end:
            pressure_interval.append(pressure[count])
            time_interval.append(i-start)

    return pressure_interval, time_interval

def plot_single_pressure(pressure, time, units='psi', count=0,
                         title='Pressure Test'):
    """ Plots single set of pressure–time data

    :param pressure: List of pressure values
    :param time: List containing time values corresponding to data points
    :param units: Unit for pressure
    :param count: Integer indicating the series for different colored lines
    when multiple Data sets are plotted on the same axes
    :param title: Title of the graph
    :return: Graph object containing the plotted graph
    """

    colors=['b.-','g.-','r.-','c.-','m.-']
    # print(time, pressure)
    plt.plot(time,pressure,colors[count])
    plt.xlabel('Time (s)')
    plt.ylabel('Pressure (' + units + ')')
    plt.title(title)

    temp_graph = plt

    return temp_graph

def plot_multi_pressure(dir,filename,format):
    """ Gathers multiple filenames, extracts data, facilitates range selection
    and plots data sets onto a single axes

    :param dir: Directory containing the data files
    :param filename: List containing all filenames of data files
    :param format: File type for exported graphs
    :return:
    """

    temp = []
    new_pressure = []
    new_time = []

    for count, file in enumerate(filename):
        raw_time, pressure, units, start, end, min, max = file_io.read_csv(
        dir + file)

        start = normalize_single_time(start)
        end = normalize_single_time(end) - start

        time = normalize_time_list(raw_time, start)

        temp.append(plot_single_pressure(pressure, time, units))
        temp[count].show()

        try:
            new_pressure, new_time = \
                handle_inputs.handle_interval_selection(
                pressure,time,end,new_pressure,new_time)
        except TypeError:
            return

    save_dir = str("./Exported/" + datetime.now().strftime("%Y-%m-%d "
                                                               "%H-%M-%S"))
    os.mkdir(save_dir)

    if format != "":
        for count, i in enumerate(new_pressure):
            single = (plot_single_pressure(i, new_time[count], units))
            file_io.render_figure(single,[filename[count]],save_dir + "/" +
                          filename[count], format, False)
            single.clf()

    for count, i in enumerate(new_pressure):
        graph = plot_single_pressure(i,new_time[count],units, int(count))
        prepare_output_data(filename[count],save_dir,i,new_time[count])

    export_filename= save_dir + "/" + "combined_plots"

    file_io.render_figure(graph, filename, export_filename, format)

    return

def prepare_output_data(filename,save_dir,pressure,time):
    """ Prepares data for output based on the modified data set after range
    selection

    :param filename: Name of the exported file, based on the input data file
    :param save_dir: Directory where the output files will be stored
    :param pressure: List containing pressure values
    :param time: List containing time values corresponding to data points
    :return:
    """

    min_pressure = min(pressure)
    max_pressure = max(pressure)
    duration = max(time)

    file_io.write_csv(filename, save_dir, duration, min_pressure, max_pressure,
                      pressure, time)

    return