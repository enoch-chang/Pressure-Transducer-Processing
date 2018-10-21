import matplotlib.pyplot as plt
import file_io
from datetime import datetime
import handle_inputs
import os

def normalize_single_time(time):
    """converts single time value into absolute time"""
    time_in_seconds=float(time.split(':')[0])*60 + float(time.split(':')[1])

    return time_in_seconds

def normalize_time_list(time, start):
    """converts time list into absolute time using the start time as a
    reference"""

    normalized_time=[]

    for i in time:
        single = normalize_single_time(i) - start
        normalized_time.append(round(single,2))

    return normalized_time

def select_interval(pressure, time, start, end):
    """trims time list to only the interval range specified"""

    time_interval=[]
    pressure_interval=[]

    for count, i in enumerate(time):

        if start < i < end:
            pressure_interval.append(pressure[count])
            time_interval.append(i-start)

    return pressure_interval, time_interval

def plot_single_pressure(pressure, time, units='psi', count=0,
                         title='Pressure Test'):

    colors=['b.-','g.-','r.-','c.-','m.-']
    # print(time, pressure)
    plt.plot(time,pressure,colors[count])
    plt.xlabel('Time (s)')
    plt.ylabel('Pressure (' + units + ')')
    plt.title(title)

    temp_graph = plt

    return temp_graph

def plot_multi_pressure(dir,filename,format):

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
                pressure,time,start,end,new_pressure,new_time)
        except TypeError:
            return

    save_dir = str("./Exported/" + datetime.now().strftime("%Y-%m-%d "
                                                               "%H-%M-%S"))
    os.mkdir(save_dir)

    if format != "":
        for count, i in enumerate(new_pressure):
            single = (plot_single_pressure(i, new_time[count], units))
            render_figure(single,[filename[count]],save_dir + "/" +
                          filename[count], format, False)
            single.clf()

    for count, i in enumerate(new_pressure):
        graph = plot_single_pressure(i,new_time[count],units, int(count))
        prepare_output_data(filename[count],save_dir,i,new_time[count])

    export_filename= save_dir + "/" + "combined_plots"

    render_figure(graph, filename, export_filename, format)

    return

def render_figure(graph, input_file, filename, format='none', show=True):

    graph.legend(input_file)

    if format == 'pdf' or format == 'png':
        graph.savefig( filename,
                    format=format)
        if show is True:
            graph.show()
    else:
        graph.show()

    return

def prepare_output_data(filename,save_dir,pressure,time):

    min_pressure = min(pressure)
    max_pressure = max(pressure)
    duration = max(time)

    file_io.write_csv(filename, save_dir, duration, min_pressure, max_pressure,
                      pressure, time)

    return

