import os
import numpy as np
from scipy.io import loadmat
import glob
import tkinter as tk
from scipy.stats import wilcoxon
from scipy.stats import ranksums



def adding_shuffled(path_shuffle,type,session_data,monkey):
    """
    Computes rank-sum significance and returns shuffled mean vector + SEM.
    Parameters:
        path_shuffle (str): Path to directory containing shuffle data files.
        type (str): Filter for selecting specific files.
        session_data (numpy array): (timeFrame x MS) matrix.
        monkey (str): Filter for selecting specific monkey data.
    Returns:
        significant_indices (numpy array): Array of significant time frames.
        (shuffled_vector, shuffled_sem) (tuple): Mean and SEM of shuffle data.
    """
    significant_indices=[]
    for file_name in os.listdir(path_shuffle):
        if monkey in file_name and type in file_name:
            file_path = os.path.join(path_shuffle, file_name)
            shuffle=loadmat(file_path)
            shuffle=next(reversed(shuffle.values())) #shuffled data (1020x50)=(fakeMS x timeFrame)
            num_time_frames = shuffle.shape[1]  # Number of time frames
            for t in range(15,num_time_frames-10):
                # Extract time frame `t`
                shuffle_t = shuffle[:,t]  # (fakeMS,)
                session_t = session_data[t, :]  # Mean across pixels for each time frame (MS,)
                # Perform rank-sum test
                _ , p_value = ranksums(shuffle_t, session_t)
                # Store significant time frames
                if p_value < 0.05:
                    significant_indices.append(t)
    shuffled_vector = np.nanmean(shuffle, axis=0)
    shuffled_sem = np.nanstd(shuffle, axis=0) / np.sqrt(shuffle.shape[0])  # SEM
    return np.array(significant_indices),(shuffled_vector, shuffled_sem)


    
    
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
            -mean_signals- list of all mean vectors to every session
            -sem_signals- "" "" "" "" sem "" "" "" ""
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
            min_mean = np.mean(vector[min_index - 1:min_index + 1])
        else:
            min_mean = np.nan  # Assign NaN if indices are out of bounds
        min_values.append(min_mean)
        
        # Mean around the max_index
        if max_index - 1 >= 0 and max_index + 1 < len(vector):
            max_mean = np.mean(vector[max_index - 1:max_index + 1])
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
        sliced_vector = vector[15:35]  # Slice the vector (from MS onset to 150ms later)
        min_idx = np.argmin(sliced_vector) + 15  
        max_idx = np.argmax(sliced_vector) + 15  
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