"""Export data (timelapse) from IR camera frames to CSV."""

import csv

from .IRUtils import processIRTimelapse

if __name__ == "__main__":

    # input directory
    input_dir = "/path/to/inputfiles/"

    # export path
    export_path = "/IRExport/"

    # list of .TMC files
    ir_list = "ir_list_myexperiment.csv"

    reader = csv.DictReader(open(ir_list), delimiter=";",
                            skipinitialspace=True)
    meas_dict = {}
    for i, row in enumerate(reader):
        for c, v in row.items():
            meas_dict.setdefault(c, []).append(v)

    for i, inputfile in enumerate(meas_dict["File"]):
        processIRTimelapse(
            inputfile=inputfile,
            rotation=meas_dict["Rotation"][i],
            exportpath=export_path,
            date=meas_dict["Date"][i],
            starttime=meas_dict["StartTime"][i],
            endtime=meas_dict["EndTime"][i],
            numberofframes=int(meas_dict["NumberOfFrames"][i]),
            doRotation=False,
            doRenaming=True)
