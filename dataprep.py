import bovespa
from bovespa import *
from progress.bar import ChargingBar
from datetime import datetime
from collections import OrderedDict
import pandas as pd
import numpy as np
import time
import csv
import sys

class RecordCollection:
    def __init__(self):
        self.records = []

    def add(self, recs):
        if recs is not None:
            self.records.extend(recs)

    def to_csv(self, outpath):
        with open(outpath, 'w') as csvfile:
            fieldnames = layout.stockquote.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for rec in self.records:
#                 if rec.stock_code == stock_code or stock_code is None:
                writer.writerow(dict(rec.info))

def main():
    bf = bovespa.File(str(sys.argv[1]))
    data = []
    for rec in bf.query():
        data.append(rec)

    rc = RecordCollection()
    rc.add(data)
    rc.to_csv("recordcollection.csv")
    dataframe = pd.read_csv("recordcollection.csv")

    clr_data = pd.DataFrame()
    clr_data["Code"] = dataframe.CODNEG
    clr_data["Date"] = dataframe.DATPRG


    bar = ChargingBar("Converting to datetime format", max=clr_data["Date"].size)
    for i in range(clr_data["Date"].size):
        #clr_data["Date"][i] = datetime.strptime(clr_data["Date"][i], '%Y-%m-%d')
        bar.next()
    bar.finish()

    clr_data["AvgPrc"] = dataframe.PREMED
    clr_data["QuaTot"] = dataframe.QUATOT
    # organize by company code and date
    clr_data = clr_data.sort_values(['Code', 'Date']).reset_index()
    clr_data = clr_data.drop(["index"], axis=1)


    # creating codes dataframe
    codes_df = pd.DataFrame(columns = ["codes", "size"])

    current_code = clr_data["Code"][0]

    j=0
    bar = ChargingBar("Creating auxiliar dataframe", max=clr_data.shape[0])
    for i in range(clr_data.shape[0]):
        bar.next()
        if clr_data["Code"][i] != current_code:
            d = {'codes': [current_code], 'size': [j]}
            aux_df = pd.DataFrame(data = d)
            codes_df = codes_df.append(aux_df, sort=True)
            
            current_code = clr_data["Code"][i]
            j=1
        else:
            j += 1

    codes_df = codes_df.reset_index()
    codes_df = codes_df.drop(["index"], axis=1)
    bar.finish()


    final_df = pd.DataFrame(columns=clr_data.columns, index=codes_df["codes"])
    i = 0 # global counter for dataframe

    auxSeries = pd.Series()
    bar = ChargingBar("Splitting on Time Series Data", max=codes_df.shape[0])
    for asset in range(codes_df.shape[0]): # counter for size vector at codes_df
        bar.next()
        for column in [cl for cl in clr_data.columns if (cl != "Code" and cl != "Date")]:
            auxSeries = pd.Series(clr_data[column].iloc[i:i + codes_df["size"].iloc[asset]])
            auxSeries.index = clr_data["Date"].iloc[i:i + codes_df["size"].iloc[asset]]
            final_df[column][codes_df["codes"].iloc[asset]] = auxSeries
            #print(auxSeries)
        i += codes_df["size"].iloc[asset]    

    bar.finish()

    final_df.to_pickle(str(time.time()) + ".pkl")
    print("----- Processing is over -------\nEnjoy your data!")
    print("Saved as " + str(time.time()) + ".pkl")

if __name__ == "__main__":
    main()