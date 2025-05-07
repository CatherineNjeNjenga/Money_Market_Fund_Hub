#import needed libraries
from sqlalchemy import create_engine
import pandas as pd
import os

#extract data from sql server
def extract():
    try:
        # starting directory
        directory = dir
        # iterate over files in the directory
        for filename in os.listdir(directory):
            #get filename without ext
            file_wo_ext = os.path.splitext(filename)[0]
            # only process excel files
            if filename.endswith(".xlsx"):
                f = os.path.join(directory, filename)
                # checking if it is a file
                if os.path.isfile(f):
                    df = pd.read_excel(f)
                    # call to load
                    load(df, file_wo_ext)
    except Exception as e:
        print("Data extract error: " + str(e))

#load data to sqlite
def load(df, tbl):
    try:
        rows_imported = 0
        engine = create_engine(f'postgresql://{uid}:{pwd}@{server}:{port}/{db}')
        print(f'importing rows {rows_imported} to {rows_imported + len(df)}... ')
        # save df to sqlite
        df.to_sql(f"stg_{tbl}", engine, if_exists='replace', index=False)
        rows_imported += len(df)
        # add elapsed time to final print out
        print("Data imported successful")
    except Exception as e:
        print("Data load error: " + str(e))

try:
    #call extract function
    df = extract()
except Exception as e:
    print("Error while extracting data: " + str(e))