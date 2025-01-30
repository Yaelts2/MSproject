import os
from inspect_data.analysis_functions2 import extract_wrong_pix, extractBaseline, Session_vector, All_session
from inspect_data.analysis_functions2 import ask_question,calculate_means_around_indices,min_max_times,adding_shuffled,create_grand_matrix
from config import DATA_PATH
import numpy as np
import glob
import logging
import matplotlib.pyplot as plt
import tkinter as tk
from scipy.stats import wilcoxon
from scipy.stats import ranksums
import pandas as pd

'''
This file is for preprocessing part. 
1) to remove noisy pix and out of V1 pix - this creates new modified files in the folder output_folder, you can change as you like 
2) second to extract baseline - this modifies the files in the output_folder 
'''
# Define paths
gandalf_path = DATA_PATH[0]
legolas_path= DATA_PATH[1]
mask_path = DATA_PATH[2]
output_folder = DATA_PATH[3]



user_response=ask_question("does the data needs to extract out of V1 pixels and noisy pixels??",True,False)
###extract out of V1 pixels and noisy pixels from all session 
if user_response==True:
    # monkey Gandalf
    extract_wrong_pix(gandalf_path, mask_path, 'outpix.mat', output_folder)
    ## monkey Legolas
    extract_wrong_pix(legolas_path, mask_path, 'outpix.mat', output_folder)

user_response2=ask_question("does the data needs to extract baseline??")
##extract baseline
# Loop through each file
if user_response2==True:
    # Find all .npy files in the directory
    npy_files = glob.glob(os.path.join(output_folder, "*.npy"))
    for file_path in npy_files:
        logging.info(f"Processing file: {file_path}")
        try:
            # Load the matrix
            session_data = np.load(file_path, allow_pickle=True)
            # Apply the extractBaseline function
            modified_data = extractBaseline(session_data)
            # Save the modified matrix back to the same file
            np.save(file_path, modified_data)
            print(f"the file {file_path} is baseline subtracted.")
        except Exception as e:
            logging.error(f"Error processing file {file_path}: {e}")
print("All files were processed: V1 regions were extracted, noisy pixels were removed, and the baseline was subtracted.",True,False)
    

