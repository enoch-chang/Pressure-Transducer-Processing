"""
Author: Enoch Chang

This script handles reading (input data) and writing (processed data) csv data
files.
"""

import csv
import matplotlib.pyplot as plt

def read_csv(filename):
    """Read csv file and separate time and pressure into respective lists.
    Also collects other parameters such as units, the start and end times and
    the min and max data values

    :param filename:
    :return: time, pressure lists, units, start, end, min and max
    """
    csvfile = open(filename + '.csv', "r")
    time = []
    pressure = []

    temp = csv.reader(csvfile, delimiter=",")

    for num, row in enumerate(temp):

        if num == 1:
            units = row[1]

        if num == 4:
            start = row[1]

        if num == 5:
            end = row[1]

        if num == 7:
            min = row[1]

        if num == 8:
            max = row[1]

        if num > 10:
            time.append(row[0])
            pressure.append(float(row[1]))

    return time, pressure, units, start, end, min, max

def write_csv(filename, save_dir, duration, min, max, pressure, time):
    """ Writes CSV containing information about the test performed,
    including the data set within the specified time range

    :param filename: Name of the corresponding input data file
    :param save_dir: Directory of where the file is saved
    :param duration: Duration of the test
    :param min: Min pressure value during test
    :param max: Max pressure value during test
    :param pressure: Pressure data list
    :param time: Time list
    :return:
    """

    csvfile = open(save_dir + "/" + filename + '.csv', "w")

    temp = csv.writer(csvfile, delimiter=',')

    temp.writerow(["Filename"]+ [filename])
    temp.writerow(["Max Pressure"] + [max])
    temp.writerow(["Min Pressure"] + [min])
    temp.writerow(["Duration"] + [duration])

    temp.writerow([" "])
    temp.writerow(["Time"] + ["Pressure"])

    for count,i in enumerate(pressure):
        temp.writerow([time[count-1]] + [i])

    return

def render_figure(graph, input_file, filename, format='none', show=True):
    """ Displays and/or saves graphs containing plotted data

    :param graph: Graph object
    :param input_file: Filename of the raw data file
    :param filename: File name of the exported graph
    :param format: Format that the graph will be saved in
    :param show: Boolean on whether to display the graph when script is run
    :return:
    """

    graph.legend(input_file)

    if format == 'pdf' or format == 'png':
        graph.savefig( filename,
                    format=format)
        if show is True:
            graph.show()
    else:
        graph.show()

    return