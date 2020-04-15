"""Export data (movie) from IR camera frames to CSV."""

import glob

from .IRUtils import processIRMovie

if __name__ == "__main__":

    # input directory
    input_dir = "path/to/data/"

    # names of the measurements to be processed with their respective rotation
    measurements = [("20200101_FirstMeasurement/IR/P0000004/", 180),
                    ("20200102_SecondMeasurement/IR/P0000005/", 180)]

    # export path
    export_path = "path/to/IRExport/"

    # time shift (in hours) if the time of the laptop / camera was off
    timeshift = 2

    for measurement, rotation in measurements:

        for inputfolder in glob.glob(input_dir + measurement):

            processIRMovie(measurement, rotation, inputfolder,
                           export_path, timeshift=timeshift,
                           doRotation=True, doRenaming=True)
