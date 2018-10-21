""" Extracts filenames from specified directory and performs ECG analysis on
each dataset.
"""

import file_io
import pressure_processor
import handle_inputs
import os

def main():

    # filenames_list = file_io.collect_csv_filenames(dir)

    dir = input("Enter the directory for your data (Input 'N' to use the "
                "./Data/ folder): ")

    if dir == "N" or dir == "n" or dir == "":
        dir = './Data/'

    try:
        os.mkdir('./Exported')
    except FileExistsError:
        pass

    number_of_files = input("How many files would you like to plot? (Up to 5) ")

    if int(number_of_files) != 1 and \
            int(number_of_files) != 2 and \
            int(number_of_files) != 3 and \
            int(number_of_files) != 4 and \
            int(number_of_files) != 5:
        print("Error: Input was not a number between 1 and 5")
        return
    if int(number_of_files) == 1:
        handle_inputs.handle_single(dir)
    elif int(number_of_files) < 6:
        handle_inputs.handle_multi(dir, int(number_of_files))


    #print(time, pressure, units)

    # time_unit = input("Time is in min or sec (default = sec)? ")
    # if time_unit != "sec" and time_unit != "min":
    #     print("Warning: Input was neither 'sec' or 'min'. Data saved as "
    #           "seconds.")
    #
    # for filename in filenames_list:
    #     time, voltage = file_io.read_csv(filename)
    #     hrm = process_ecg_data.HeartRateMonitor(time, voltage, voltage_ref,
    #                                             time_unit, filename)
    #
    #     file_io.write_json(filename, hrm.output())

if __name__ == "__main__":
    main()
