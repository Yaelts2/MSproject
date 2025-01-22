import os
import numpy as np
from scipy.io import loadmat

def extract_data_matlab(file_name, column_number, DATA_PATH, data_key):
    """Extracts numerical data from a specific column in a MATLAB .mat file.

    Parameters:
        file_name (str): Name of the .mat file.
        column_number (int): Column index to extract data from.
        DATA_PATH (str): Directory path where the .mat file is located.
        data_key (str): Key for the MATLAB structure containing the data.

        Returns:
        list: A list containing the extracted data from the column. Supports mixed data types (e.g., strings, numbers).

        """
    #build full path of the file and Load the MATLAB file
    file_path = os.path.join(DATA_PATH, file_name) 
    data = loadmat(file_path)
    
    # Raise error incase the data_key is not in the data
    if data_key not in data:
        raise KeyError(f"The key '{data_key}' does not exist in the MATLAB file.")
    msMats = data[data_key] #Extract all the data itself from the file, which is in the data_key provided 
    
    #Raise error incase the column index not exists in the data
    if column_number >= msMats.shape[1]:
        raise IndexError(f"Column {column_number} is out of range. The data has {msMats.shape[1]} columns.")
    
    # Extract the column data with column number provided, without the column name(first line)
    column_data = msMats[1:, column_number]
    
    # Filter and extract numerical values
    values = []
    for row in column_data:
        if isinstance(row, np.ndarray) and row.size > 0:  # Ensure row contains data
            value = row[0]
            if isinstance(value, np.ndarray) and value.size > 0:
                values.append(float(value[0]))  # Convert nested value to float
            else:
                values.append(float(value))  # Convert directly to float if not nested
        else:
            values.append(None)  # Add None for invalid rows
    return values


