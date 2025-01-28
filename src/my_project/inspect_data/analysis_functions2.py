import os
import numpy as np
from scipy.io import loadmat
import glob
import tkinter as tk
from scipy.stats import wilcoxon

def ask_question(question):
    '''
    GUI in python with package tkinter
    gets a question and sends back the response
    '''
    response = None
    def save_response(value):
        nonlocal response
        response = value
        root.destroy()
    root = tk.Tk()
    root.title('Question')
    tk.Label(root, text=question).pack(pady=10)
    tk.Button(root, text='Yes', command=lambda: save_response(True)).pack(side=tk.LEFT, padx=10, pady=10)
    tk.Button(root, text='No', command=lambda: save_response(False)).pack(side=tk.RIGHT, padx=10, pady=10)
    root.mainloop()
    return response


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
        - mask_type (str): Type of mask file to use ('outpix.mat').
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
    files_dir = glob.glob(os.path.join(Data_path, "*no_BV.mat"))
    for file_name in files_dir:
        count_processed += 1
        session_data = load_session_data(Data_path, file_name)
        session_number = file_name[0:-18]  # Extract session identifier

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




## extract baseline 
def extractBaseline(session_data):
    """
    Modifies the input matrix by subtracting the baseline mean 
    (calculated from frames 0 to 10) for each pixel and microsaccade.

    Parameters:
        session_data (numpy.ndarray): A 3D matrix representing pixels, time frames, and microsaccades.

    Returns:
        numpy.ndarray: The modified input matrix with baseline mean subtracted.
    """
    # Loop over microsaccades
    for ms_id in range(session_data.shape[2]):  # Microsaccades (3rd dimension)
        for pixel_id in range(session_data.shape[0]):  # Pixels (1st dimension)
            # Extract the time vector for the current pixel and microsaccade
            pixel_vec = session_data[pixel_id, :, ms_id]
            
            # Subtract the mean of the first 10 frames
            baseline_mean = np.nanmean(pixel_vec[0:10])
            session_data[pixel_id, :, ms_id] -= baseline_mean
    
    return session_data


def Session_vector(file_path):
    '''
    Processes a session file to compute the mean signal and SEM.

    Parameters:
        file_path (str): Path to the session file.

    Returns:
        tuple: Mean signal and SEM .
    '''
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    session_data=np.load(file_path)  #loading session data
    if session_data.ndim != 3:
        raise ValueError(f"Invalid session data shape: {session_data.shape}, expected a 3D array.")
    mean_signal=np.nanmean(session_data,axis=0) #mean on all pixls , dim=1 [0],  (num_frames, num_MS)
    sem_example= np.nanstd(mean_signal, axis=1) / np.sqrt(mean_signal.shape[1])  # Shape: (50,)
    mean_signal=np.nanmean(mean_signal,axis=1) # mean on all MS , dim=3 [1] 
    return (mean_signal,sem_example)

def All_session (files_path,monkey):
    '''
    Processes all session files for a given monkey to compute the grand mean signal and SEM.

    Parameters:
        files_path (str): Path to the folder containing session `.npy` files.
        monkey (str): Prefix for session file names ('gandalf', 'legolas').

    Returns:
        tuple: 
            - all_session_mean (numpy.ndarray): 1D array of shape (num_time_frames,) representing 
            the mean signal across all sessions.
            - all_session_SEM (numpy.ndarray): 1D array of shape (num_time_frames,) representing 
            the average SEM.
    '''
    npy_files = glob.glob(os.path.join(files_path, f"{monkey}*.npy"))
    if not npy_files:
        raise ValueError(f"No files found for monkey '{monkey}' in folder '{files_path}'")
    mean_signals= []  #List of signals for all sessions
    sem_signals= []   # List to store SEM signals
    for file_path in npy_files:
        try:
            mean_signal, sem_signal = Session_vector(file_path)
            mean_signals.append(mean_signal)
            sem_signals.append(sem_signal)
        except Exception as e:
            print(f"Skipping file {file_path} due to error: {e}")
    
    return(mean_signals,sem_signals)

import numpy as np

def calculate_means_around_indices(mean_signals, min_index, max_index):
    """
    Calculates mean values of three consecutive elements (index-1, index, index+1) 
    for specified indices (min and max) across multiple signal vectors.
    
    Parameters:
        mean_signals (list of numpy.ndarray): List of 1D arrays containing mean signal vectors.
        min_index (int): Index for calculating means around the minimum point.
        max_index (int): Index for calculating means around the maximum point.
    
    Returns:
        tuple: 
            - min_results (list): Contains [list of individual means, overall mean, SEM, signed-rank test result] for the minimum index.
            - max_results (list): Contains [list of individual means, overall mean, SEM, signed-rank test result] for the maximum index.
    """
    min_values = []
    max_values = []
    for vector in mean_signals:
        # Mean around the min_index
        if min_index - 1 >= 0 and min_index + 1 < len(vector):
            min_mean = np.mean(vector[min_index - 1:min_index + 2])
        else:
            min_mean = np.nan  # Assign NaN if indices are out of bounds
        min_values.append(min_mean)
        
        # Mean around the max_index
        if max_index - 1 >= 0 and max_index + 1 < len(vector):
            max_mean = np.mean(vector[max_index - 1:max_index + 2])
        else:
            max_mean = np.nan  # Assign NaN if indices are out of bounds
        max_values.append(max_mean)
    # Calculate overall statistics for min values
    min_mean_overall = np.nanmean(min_values)  # Mean across all sessions
    min_sem = np.nanstd(min_values) / np.sqrt(len(min_values))  # Standard Error of Mean (SEM)
    min_rank_test = wilcoxon(min_values, alternative='two-sided')  # Signed-rank test
    # Compile results for min index
    min_results = [min_values, min_mean_overall, min_sem, min_rank_test]
    # Calculate overall statistics for max values
    max_mean_overall = np.nanmean(max_values)
    max_sem = np.nanstd(max_values) / np.sqrt(len(max_values))
    max_rank_test = wilcoxon(max_values, alternative='two-sided')
    # Compile results for max index
    max_results = [max_values, max_mean_overall, max_sem, max_rank_test]
    return min_results, max_results





def min_max_times(mean_signals,time_V):
    min_times=[]
    max_times=[]
    for vector in mean_signals:
        min_idx = np.argmin(vector)  # Fix: Apply to each vector
        max_idx = np.argmax(vector)
        min_times.append(time_V[min_idx])
        max_times.append(time_V[max_idx])
    min_times = np.array(min_times)
    max_times = np.array(max_times)
    #compute mean and SEM and sighed rank test
    min_mean=np.nanmean(min_times)
    min_sem = np.nanstd(min_times) / np.sqrt(len(min_times))
    s_test_min=wilcoxon(min_times, alternative="two-sided")
    min_results=[min_times,min_mean,min_sem,s_test_min]
    ##min_results: list of all times , mean , sem , signed rank test
    max_mean=np.nanmean(max_times)
    max_sem=np.nanstd(max_times)/np.sqrt(len(max_times))
    s_test_max=wilcoxon(max_times, alternative="two-sided")
    max_results=[max_times,max_mean,max_sem,s_test_max]
    #max_results: list of all times , mean , sem , signed rank test
    return(min_results,max_results)