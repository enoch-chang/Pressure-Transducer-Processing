"""
Author: Enoch Chang

This program takes exported csv files from OMEGA PX409 USBH pressure
transducers and plots data onto a graph. It allows for plotting multiple
data sets and selection of data range for plotting.

This script contains the main function which initiates data processor by
collecting filenames then performing relevant data handling
"""

import handle_inputs
import os

def main():
    """Main function is executed from console to collect filenames from user input"""
    dir = input("Enter the directory for your data (Input 'N' to use the "
                "./Data/ folder): ")

    if dir == "N" or dir == "n" or dir == "":
        ### CHANGE DEFAULT DIRECTORY HERE FOR DATA SOURCE ###
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

if __name__ == "__main__":
    main()
