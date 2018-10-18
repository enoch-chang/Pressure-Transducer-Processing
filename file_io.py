import glob
import csv
import json


def collect_csv_filenames(dir):
    """Collect all the *.csv files located in the test_data folder

    :return: list containing list of all filenames
    """
    filenames_list = glob.glob(dir)
    if len(filenames_list) == 0:
        print("No files found in specified directory.")
    return filenames_list


def read_csv(filename):
    """Read csv file and separate time and voltage into respective lists

    :param filename:
    :return:
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

    # pressure = list(map(float, pressure))

    return time, pressure, units, start, end, min, max


def write_json(filename, info):
    """Write data to .json file

    :param filename: Output filename
    :param info: Dictionary containing data to write
    :return:
    """
    json_filename = filename.replace('.csv', '.json')
    json_file = open(json_filename, "w")
    json.dump(info, json_file)
    json_file.close

    return
