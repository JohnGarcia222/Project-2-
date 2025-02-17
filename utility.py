import pandas as pd
import numpy as np
from pathlib import Path
import hvplot.pandas
import matplotlib.pyplot as plt
import os
import warnings
warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
from watermark import watermark




def csv_to_dataframe(folder_path, rename_columns = False):
    """
    Convert all CSV files in a folder to pandas DataFrames and store them in a dictionary

    Parameters
    --------
    folder_path: str
        The path to the folder containing the CSV files.
    
    rename_columns: boolean
        Determine if need to rename df columns to include file name or not
    """
    # Create an empty dictionary to hold the dataframes
    dataframes = {}

    # Loop over all files in the folder
    for file in os.listdir(folder_path):
        # Check if the file is a CSV file
        if file.endswith('.csv'):
            # Construct the full file path by joining the folder path and the file name
            file_path = os.path.join(folder_path, file)
            # Separate the file name from its extension
            file_name, _ = os.path.splitext(file)
            # Get the name of the folder
            folder_name = os.path.basename(os.path.abspath(folder_path))
            # Construct the dataframe name by combining the folder name, file name and a suffix
            df_name = f"{folder_name}_{file_name}_df"

            try:
                # Try to read the CSV file into a pandas DataFrame
                df = pd.read_csv(file_path, index_col=0, parse_dates = True, infer_datetime_format = True)
                
                #If rename_columns = True, modify column names to include the file name
                if rename_columns==True:
                    df.columns = [f"{file_name}_{col}" for col in df.columns]
                
                # Remove dollar signs and commas from the DataFrame (assuming these are in string format)
                df = df.replace({'\$': '', ',': ''}, regex=True)
                # Fill any missing values with 0
                #df.fillna(0, inplace=True)
                # Store the DataFrame in the dictionary using the constructed name as the key
                dataframes[df_name] = df
            except Exception as e:
                # If there was an error reading the file, print an error message
                print(f"Error reading file '{file}': {e}")

    # Return the dictionary of DataFrames
    return dataframes

def clean_timestamp(dataframe):
     dataframe.index = pd.DatetimeIndex( dataframe.index.tolist() ) 
     return dataframe


def resample(dataframe, resample_dataframe):
    dataframe = dataframe.reindex(resample_dataframe.index)
    dataframe = dataframe.fillna(method='ffill')
    dataframe = dataframe.dropna()
    return dataframe