#!/usr/bin/env python3
"""Analyze data from IR data from CSV to CSV."""

import glob
import pandas as pd

import ir_utils as ir

if __name__ == "__main__":
    inputFolder = "path/to/IRExport/"
    positions, numberOfZones = ir.getPositionInformation("positions.csv")
    numberOfFiles = len(glob.glob(inputFolder + "ir_export_*.csv"))

    # get mean, std deviation and median for each box
    # in each file into one CSV file
    df_ir = pd.DataFrame()
    for i, csvfile in enumerate(glob.glob(inputFolder + "ir_export_*.csv")):
        if i % 100 == 0:
            print("File %i of %i analyzed." % (i, numberOfFiles))

        ir_data = ir.getIRDataFromMultipleZones(csvfile, positions,
                                                numberOfZones)
        df_ir = df_ir.append(ir_data, ignore_index=True)
        # sys.exit()

    df_ir.to_csv(inputFolder + "IR_zones.csv", sep=";")
