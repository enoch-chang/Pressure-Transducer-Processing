import file_io
import pressure_processor
from datetime import datetime
import os

def handle_single(dir):

    #filename = 'sample_1'

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
        pressure,time = handle_interval_selection(pressure,time,start,end)
    except TypeError:
        return

    format = input("Export filetype ('pdf' or 'png'; other input for view "
                    "only) ")

    save_dir = str("./Exported/" + datetime.now().strftime("%Y-%m-%d "
                                                               "%H-%M-%S"))
    os.mkdir(save_dir)

    export_filename = save_dir + '/' + filename + ' ' + '.' + format

    print (pressure[0],time[0])

    graph = pressure_processor.plot_single_pressure(pressure[0], time[0],
                                                    units)

    pressure_processor.render_figure(graph,[filename],export_filename,format)
    pressure_processor.prepare_output_data(filename,save_dir,pressure[0],
                                           time[0])

    return


def handle_multi(dir, number_of_files):

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

def handle_interval_selection(pressure,time,start,end,new_pressure=[],
                              new_time=[]):

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
