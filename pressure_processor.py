import matplotlib.pyplot as plt
import file_io
from datetime import datetime
import handle_inputs

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
    plt.plot(time,pressure,colors[count])
    plt.xlabel('Time (s)')
    plt.ylabel('Pressure (' + units + ')')
    plt.title(title)

    temp_graph = plt

    return temp_graph

def plot_multi_pressure(dir,filename,format):

    temp = []

    for count, file in enumerate(filename):
        raw_time, pressure, units, start, end, min, max = file_io.read_csv(
        dir + file)

        start = normalize_single_time(start)
        end = normalize_single_time(end) - start

        time = normalize_time_list(raw_time, start)

        temp.append(plot_single_pressure(pressure, time, units))
        temp[count].show()

        try:
            pressure[count], time[count] = \
                handle_inputs.handle_interval_selection(
                pressure,time,start,end)
        except TypeError:
            return


    for count, i in enumerate(pressure):
        graph = plot_single_pressure(i,time[count-1],units, int(count-1))

    export_filename= "./Exported/combined_plots_" + str(datetime.now().strftime("%Y-%m-%d %H-%M-%S")) ####

    render_figure(graph, filename, export_filename, format)

    return

def render_figure(graph, input_file, filename, format='none'):

    graph.legend(input_file)

    if format == 'pdf' or format == 'png':
        graph.savefig( filename,
                    format=format)
        graph.show()
    else:
        graph.show()

    return



