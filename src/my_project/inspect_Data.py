from scipy.io import loadmat
import os 
import pandas as pd
import numpy as np

def extrctingDATA_fromMAT(file_name,colonm_number,DATA_PATH, data_key):
    """
    Extracts numerical data from a specific column in a MATLAB .mat file.
    
    Parameters:
        file_name (str): Name of the .mat file.
        column_number (int): Column index to extract data from.
        data_key (str): Key for the MATLAB structure containing the data. Default is 'msMats'.
        data_path (str): Directory path where the .mat file is located. Default is the current directory.
    
    Returns:
        np.ndarray: A NumPy array containing the extracted numerical data.
    """
    file_path = os.path.join(DATA_PATH, file_name)
    data = loadmat(file_path)
    msMats=data[data_key]
    column_data=msMats[:,colonm_number]
    values = [row[0, 0] for row in column_data 
            if isinstance(row, np.ndarray) and row.size > 0 and isinstance(row[0, 0], (int, float, np.float64))]
    return np.array(values, dtype=float)

