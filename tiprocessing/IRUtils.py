"""Helper functions for the thermal infrared camera Tau 2."""

import csv
import glob
import os
import sys
from datetime import datetime, timedelta
from subprocess import call

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def processIRMovie(measurement, rotation, inputfolder, exportpath,
                   timeshift=0, doRotation=True, doRenaming=True):
    """Process TMC-files of IR camera into CSV files in movie mode.

    Movie mode means, that one frame-sequence (movie) per datapoint was taken
    instead of one frame per datapoint (timelapse). In the first step, the data
    of a TMC file is exported via ThermoViewer into a CSV file. The second
    step takes care of the optional rotation of the image and in the end,
    the CSV files are renamed according to their date and time.

    Parameters
    ----------
    measurement : str
        Relative path to measurement folder
    rotation : int/str/float
        Degrees about which the image should be rotated.
        Valid values are 0, 90, 180, 270
    inputfolder : str
        Absolute path to the input folder
    exportpath : str
        Path of the export files
    timeshift : int, optional
        Timeshift in hours
    doRotation : bool, optional
        If True, the image is rotated about the given degree
    doRenaming : bool, optional
        If True, the CSV file is renamed

    """
    date = measurement[:8]
    foldername = os.path.basename(os.path.normpath(inputfolder))
    prefix = "ir_export_" + date + "_" + foldername

    # export all IR files from folder to csv files
    # ROTATION: note that as long as the rotation feature is not
    # implemented in ThermoViewer, it can't be used
    ThermoViewer(mode="folder",
                 inputpath=inputfolder,
                 exportpath=exportpath,
                 rotation=0,
                 prefix=prefix,
                 frame_start=1,
                 frame_end=1,
                 exportformat="csv",
                 colorpalette="iron",
                 meta=False,
                 close=True)

    # alternative image rotation
    if doRotation:
        for ofile in glob.glob(exportpath + prefix + "*.csv"):
            if rotation == 180:
                rotateCSVFile180(ofile)
                print("Rotated file: ", ofile)

    # include time of the file into filename
    if doRenaming:
        for ifile in glob.glob(inputfolder+"/*.TMC"):
            timestamp = int(os.path.getmtime(ifile))
            shifted_timestamp = (datetime.fromtimestamp(timestamp) +
                                 datetime.timedelta(hours=timeshift))
            time = shifted_timestamp.strftime('%H-%M-%S')
            filenumber = os.path.basename(os.path.normpath(ifile))[2:-7]
            ofilename = prefix + "_" + filenumber
            ofile = exportpath + ofilename + "_0001.csv"
            ofile_new = exportpath + ofilename + "_" + time + ".csv"
            print("Renamed file: ", ofile)
            # print("new: ", ofile_new)
            os.rename(ofile, ofile_new)


def processIRTimelapse(inputfile, rotation, exportpath, date,
                       starttime, endtime, numberofframes,
                       doRotation=True, doRenaming=True):
    """Process TMC-files of IR camera into CSV files in timelapse mode.

    Timelapse mode means, that one frame per datapoint (timelapse) was taken
    instead of one frame-sequence (movie) per datapoin. In the first step, the
    data of a TMC file is exported via ThermoViewer into a CSV file. The second
    step takes care of the optional rotation of the image and in the end,
    the CSV files are renamed according to their date and time.

    Parameters
    ----------
    inputfile : str
        Absolute path to the input file
    rotation : int/str/float
        Degrees about which the image should be rotated.
        Valid values are 0, 90, 180, 270
    exportpath : str
        Path of the export files
    date : str
        Date of the measurement, e.g. "20170821"
    starttime, endtime : str
        Time of the start and end of the measurement, e.g. "13:49"
    numberofframes : int
        Number of frames in the given timelapse
    doRotation : bool, optional
        If True, the image is rotated about the given degree
    doRenaming : bool, optional
        If True, the CSV file is renamed

    """
    filename = os.path.basename(os.path.normpath(inputfile))
    foldername = os.path.normpath(inputfile).split("/")[-2]
    prefix = "ir_export_" + date + "_" + foldername + "_" + filename[:-4]

    # export all IR files from folder to csv files
    # ROTATION: note that as long as the rotation feature is not
    # implemented in ThermoViewer, it can't be used
    ThermoViewer(mode="file",
                 inputpath=inputfile,
                 exportpath=exportpath,
                 rotation=0,
                 prefix=prefix,
                 frame_start=0,
                 frame_end=0,
                 exportformat="csv",
                 colorpalette="iron",
                 meta=False,
                 close=True)

    # alternative image rotation
    if doRotation:
        for ofile in glob.glob(exportpath + prefix + "*.csv"):
            if rotation == 180:
                rotateCSVFile180(ofile)
                print("Rotated file: ", ofile)

    # include time into filename
    if doRenaming:
        starttimestamp = datetime.strptime(starttime, "%H:%M").timestamp()
        endtimestamp = datetime.strptime(endtime, "%H:%M").timestamp()
        interval = timedelta(seconds=(endtimestamp - starttimestamp) /
                             (int(numberofframes) - 1))
        measurement_intervals = [datetime.fromtimestamp(
            starttimestamp + i*interval.total_seconds()).strftime("%H-%M-%S")
            for i in range(int(numberofframes))]
        # print(measurement_intervals)
        for i, ofile in enumerate(glob.glob(exportpath + prefix + "*.csv")):
            ofile_new = ofile[:-4] + "_" + measurement_intervals[i] + ".csv"
            print("Renamed file: ", ofile)
            # print("new: ", ofile_new)
            os.rename(ofile, ofile_new)


def ThermoViewer(mode, inputpath, exportpath, rotation, prefix,
                 frame_start, frame_end, exportformat="csv",
                 colorpalette="iron", meta="CSVfa", close=True):
    """Open the application ThermoViewer with given the options for a folder.

    Parameters
    ----------
    mode : str
        Either "file" or "folder"
    inputpath : str
        Path to the input folder/file
    exportpath : str
        Path of the export files
    rotation : int/str/float
        Degrees about which the image should be rotated.
        Valid values are 0, 90, 180, 270
    prefix : str
        Name prefix for the export file
    frame_start, frame_end : int
        Frame number to start/end the export
    exportformat : str, optional
        Export format. Valid options are png, jpg, tif, avi, csv, rjpg
    colorpalette : str, optional
        Color palette.
    meta : str/bool, optional
        Output format for the meta data.
        Valid options are: CSVpf, CSVfa, KML, RAW or False
    close : bool, optional
        True, if the application should be closed after the export.


    Options for ThermoViewer
    ------------------------
    -c : Automatically closes the application after processing all given tasks
    -cp palette : Sets the color palette. Available are: gray, iron, arctic,
        rainbow
    -folder path : Processes all files in given path
    -help : Displays this help screen
    -i file : Loads the given file after opening the application
    -ic : Enables color inversion
    -exef number : Sets export ending frame to number
    -exfn name : Sets the name prefix for exported files to name
    -exfo <format> : Sets the export format. Available are: png, jpg, tif,
        avi, csv, rjpg
    -expa path : Sets the directory to which exports are written to path
    -exsf number : Sets export starting frame to number
    -exmeta <type> : Set the ouput format for meta data. If ommited, no meta
        data will be written. Available options are:
            CSVpf - One CSV per frame
            CSVfa - One CSV for all frames
            KML - One .kml for all frames
            RAW - Binary raw data
    -tl format : T Linear settings. Available are: none, high, low
            high = Tau core is in high gain mode
            low = Tau core is in low gain mode
    -l : Adds a legend to the exported image
    -r degree : Rotates the input frames. Supported degrees are 0, 90, 180, 270

    """
    APP_LINK = "/Applications/ThermoViewer.app/Contents/MacOS/ThermoViewer"

    if mode == "file":
        calllist = [APP_LINK, "-i", inputpath]
    elif mode == "folder":
        calllist = [APP_LINK, "-folder", inputpath]
    else:
        print("Invalid mode for ThermoViewer: ", mode, ".")
        sys.exit(0)

    # rotation:
    if int(rotation) in [0, 90, 180, 270]:
        calllist.extend(["-r", str(rotation)])
    else:
        print("WARNING: The rotation option >" + rotation +
              "< is not available.")

    # color palette, export path, export prefix,
    calllist.extend(["-cp", colorpalette,
                     "-expa", exportpath,
                     "-exfn", prefix,
                     "-exsf", str(frame_start),
                     "-exef", str(frame_end)])

    # export format
    if exportformat in ["png", "jpg", "tif", "avi", "csv", "rjpg"]:
        calllist.extend(["-exfo", exportformat])
    else:
        print("WARNING: The exportformat >" + exportformat +
              "< is not available.")

    # meta data
    if meta in ["CSVpf", "CSVfa", "KML", "RAW"]:
        calllist.extend(["-exmeta", meta])
    elif meta is False:
        pass
    else:
        print("WARNING: The exmeta option >" + meta + "< is not available.")

    # close after running the application?
    if close:
        calllist.extend(["-c"])

    # print(calllist)
    call(calllist)


def showIRImageFromCSV(csvpath):
    """Show image from CSV file.

    Parameters
    ----------
    csvpath : str
        Path to CSV file

    """
    df = pd.read_csv(csvpath, delimiter=";")
    plt.imshow(df)
    plt.show()


def rotateCSVFile180(csvpath):
    """Rotates image in CSV format about 180 degrees into CSV format image.

    Parameters
    ----------
    csvpath : str
        Path to CSV file

    """
    # get data and rotate
    with open(csvpath, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        csvcontent = [row for row in reader]
        csvcontent_new = [[csvcontent[i][j] for j in
                           reversed(range(len(csvcontent[0])))]
                          for i in reversed(range(len(csvcontent)))]

    # write data in the same file
    with open(csvpath, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        for row in csvcontent_new:
            writer.writerow(row)


def getIRDataFromMultipleZones(csvpath: str,
                               positions: dict,
                               zone_list: list):
    """Get IR data from multiple zones.

    Parameters
    ----------
    csvpath : str
        Path to CSV file
    positions : dict
        Dictionary containing the positions (row, column) of the zones per date
    zone_list : list of str
        List of zones

    Returns
    -------
    DataFrame
        DataFrame containing all IR data of the current CSV file in one row

    """
    filename = os.path.basename(os.path.normpath(csvpath))
    date, time, folder, filenumber = getFileInfo(filename)
    positions["measurement"] = [str(x) for x in positions["measurement"]]
    indexOfDataset = positions["measurement"].index(date)

    df = pd.read_csv(csvpath, delimiter=";")
    df = df.dropna(axis=1, how='all')

    # plt.clf()
    # _, ax = plt.subplots(1)
    # ax.imshow(df)

    irdata_dict = {"ir_date": date, "ir_time": time,
                   "ir_folder": folder, "ir_filenumber": filenumber}

    # add all x zones
    for zone in zone_list:
        # (x, y) is the upper left point
        # x = positions["zone"+str(i)+"_col_start"][indexOfDataset]
        # y = positions["zone"+str(i)+"_row_start"][indexOfDataset]
        # width = positions["zone"+str(i)+"_col_end"][indexOfDataset] - x
        # height = positions["zone"+str(i)+"_row_end"][indexOfDataset] - y
        # rect = patches.Rectangle((x, y), width, height, linewidth=1,
        #                          edgecolor='r', facecolor='none')
        # ax.add_patch(rect)

        ir_data = getIRDataFromZone(image=df.values.tolist(),
                                    positions=positions,
                                    zone_name=zone,
                                    iod=indexOfDataset)
        irdata_dict["ir_"+zone+"_med"] = [ir_data[0]]
        irdata_dict["ir_"+zone+"_mean"] = [ir_data[1]]
        irdata_dict["ir_"+zone+"_std"] = [ir_data[2]]

    # plt.show()
    return pd.DataFrame(irdata_dict)


def getIRDataFromZone(image: list, positions: dict, zone_name: str, iod: int):
    """Get IR data from one specific zone.

    Parameters
    ----------
    image : list of lists
        Content of CSV file
    positions : dict
        Dictionary containing the positions (row, column) of the zones per date
    zone_name : str
        Name of the current zone, e.g. "zone1"
    iod : int
        Index of Dataset = row number in positions CSV file

    Returns
    -------
    median : float
        Median of the IR value in the current zone
    mean : float
        Mean of the IR value in the current zone
    std : float
        Standard deviation of the IR value in the current zone

    """
    edges = [positions[zone_name+"_row_start"][iod],
             positions[zone_name+"_row_end"][iod],
             positions[zone_name+"_col_start"][iod],
             positions[zone_name+"_col_end"][iod]]

    roi = np.array(image)[edges[0]:edges[1], edges[2]:edges[3]]
    median = np.median(roi)
    mean = np.mean(roi)
    std = np.std(roi)
    return median, mean, std


def getPositionInformation(position_path):
    """Get spectralon positions for each measurement from file.

    Parameters
    ----------
    position_path : str
        Path to config file (positions.csv) with the columns `measurement`,
        `zone1_row_start`, `zone1_row_end`, `zone1_col_start`and
        `zone1_col_end`. The respective values, the zone borders, are provided
        as integer.

    Returns
    -------
    pos_info : dict
        Dictionary with information of the positions config file

    """
    if not os.path.isfile(position_path):
        print("Path %s is not available", position_path)
        sys.exit(0)

    reader = csv.DictReader(open(position_path), delimiter=" ",
                            skipinitialspace=True)
    pos_info = {}
    for row in reader:
        for c, v in row.items():
            if c == "measurement":
                pos_info.setdefault(c, []).append(v)
            else:
                pos_info.setdefault(c, []).append(int(v))
    numberOfZones = (len(pos_info.keys()) - 1) // 4
    return pos_info, numberOfZones


def getFileInfo(filename: str):
    """Get file information from filename.

    Parameters
    ----------
    filename : str
        Filename of CSV file

    Returns
    -------
    date : str
        Date of the file
    time : str
        Time of the file
    folder : str
        Measurement folder of the file
    filenumber : str
        Number of the measurement

    Example
    -------
    path = ir_export_20170815_P0000004_005_10-50-08
    date = 20170815
    time = 10-50-08
    folder = P0000004
    filenumber = 005

    """
    date = filename[10:18]
    time = filename[-12:-4]
    folder = filename[19:27]
    filenumber = filename[28:31]

    return date, time, folder, filenumber
