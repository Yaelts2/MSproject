import os
import numpy as np
from scipy.io import loadmat

def load_session_data(Data_path, file_name):
    """Load session data from a given path and file name."""
    file_path = os.path.join(Data_path, file_name)
    return loadmat(file_path)

def process_mask_file(mask_file_path, vector_key):
    """Load mask data and return the indices to modify based on the vector."""
    mask_data = loadmat(mask_file_path)
    if vector_key not in mask_data:
        print(f"Key {vector_key} not found in the mask file.")
        return None
    vector = mask_data[vector_key].flatten()
    indices_to_modify = np.where(vector == 1)[0]
    return indices_to_modify

def save_modified_matrix(matrix, output_file):
    """Save the modified matrix to a specified output file."""
    try:
        np.save(output_file, matrix)
        print(f"Modified matrix successfully saved to {output_file}")
        return True
    except Exception as e:
        print(f"Failed to save the file {output_file}. Error: {e}")
        return False

def extract_wrong_pix(Data_path, mask_path, mask_type, output_folder):
    """
    Purpose:
    The function processes all session files in the specified data folder. For each session file, it identifies the corresponding mask file
    based on naming conventions, modifies the matrix by setting indices to NaN where the mask vector equals 1, and saves the modified matrix
    as a Python `.npy` file.

    Parameters:
        - Data_path (str): Path to the folder containing session data files.
        - mask_path (str): Path to the folder containing mask data files.
        - mask_type (str): Type of mask file to use ('outOfV11.mat' / 'noisyPixels.mat').
        - output_folder (str): Path to save the modified matrix files.
        - verbose (bool): If True, prints detailed execution messages.

    Returns:
        dict: A summary dictionary with counts of processed and modified files.
        list: A list of all modified matrices.
    """
    count_processed = 0
    count_modified = 0

    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over session files
    for file_name in os.listdir(Data_path):
        if file_name.endswith("no_BV.mat"):
            count_processed += 1
            session_data = load_session_data(Data_path, file_name)
            session_number = file_name[0:15]  # Extract session identifier

            # Check for matrix_key
            matrix_key = 'dataByMs_no_BV'
            if matrix_key not in session_data:
                print(f"Key {matrix_key} not found in session data.")
                continue

            matrix = session_data[matrix_key]

            # Iterate over mask files
            for file_mask_name in os.listdir(mask_path):
                if file_mask_name.startswith(session_number) and file_mask_name.endswith(mask_type):
                    mask_file_path = os.path.join(mask_path, file_mask_name)
                    vector_key = file_mask_name[0:-4]

                    indices_to_modify = process_mask_file(mask_file_path, vector_key)
                    if indices_to_modify is None:
                        print("No indices to modify were found. Exiting the function.")
                        return None

                    # Modify the matrix
                    for idx in indices_to_modify:
                        matrix[idx, :, :] = np.nan
                        
                        
                    # Save modified matrix
                    output_file = os.path.join(output_folder, f"{session_number}_modified.npy")
                    if save_modified_matrix(matrix, output_file):
                        count_modified += 1
                    break  # Exit the loop after processing the matching mask file

    return {"processed_files": count_processed, "modified_files": count_modified}
