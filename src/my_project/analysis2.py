import os
from inspect_data.analysis_functions2 import extract_wrong_pix, extractBaseline, Session_vector, All_session
from config import DATA_PATH
import numpy as np
import glob
import logging
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox


# Define paths
gandalf_path = DATA_PATH[0]
legolas_path= DATA_PATH[1]
mask_path = DATA_PATH[2]
output_folder = DATA_PATH[3]
baseline_substracted= True # if needed to substruct baselne

###extract out of V1 pixels and noisy pixels from all session 
if not os.listdir(output_folder):
    # monkey Gandalf
    extract_wrong_pix(gandalf_path, mask_path, 'outpix.mat', output_folder)
    ## monkey Legolas
    extract_wrong_pix(legolas_path, mask_path, 'outpix.mat', output_folder)


##extract baseline
# Find all .npy files in the directory
npy_files = glob.glob(os.path.join(output_folder, "*.npy"))
# Loop through each file
if baseline_substracted==False:
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
print("All files were processed: V1 regions were extracted, noisy pixels were removed, and the baseline was subtracted.")
    

# ################check one file
# file_path = "C:\myprojects\data\output/gandalf_270618b__modified.npy"
# data = np.load(file_path, allow_pickle=True)
# # Select a 2D slice for visualization
# # Example: Average across microsaccades to get a (pixels, time_frames) matrix
# data_for_image=data[:,10,15]
# # Display the 2D array using imshow
# reshaped_slice = data_for_image.reshape((100, 100))  # Example: 100x100 grid
# # Plot the 2D data using imshow
# plt.imshow(reshaped_slice, cmap="viridis", aspect="auto")
# plt.colorbar(label="Intensity")
# plt.title("Visualization of Matrix Slice (:, 10, 12)")
# plt.xlabel("X Dimension")
# plt.ylabel("Y Dimension")
# plt.show()



#calculating all sessions mean vector
# Monkey G 
mean_G, SEM_G = All_session(files_path=output_folder, monkey='gandalf')
#Monkey L
mean_L,SEM_L= All_session(files_path=output_folder,monkey='legolas')




# #Time course of the VSD signal for the example session
# Monkey G
file_path_G = "C:\myprojects\data\output/gandalf_240718united__modified.npy"
mean_signal_G,sem_example_G=Session_vector(file_path_G)
# Monkey L
file_path_L = "C:\myprojects\data\output/legolas_111108united__modified.npy"
mean_signal_L,sem_example_L=Session_vector(file_path_L)



##plot for monkey L
time = np.linspace(-100, 300, mean_L.shape[0])
fig, axs = plt.subplots(1, 2, figsize=(14, 6), sharey=True)  # 1 row, 2 columns
for ax in axs:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.axvline(0, color="black", linestyle="--", linewidth=0.8)  # Dashed vertical line at x=0
    axs[0].axhline(0, color="black", linestyle="--", linewidth=0.8)  # Zero line
# Example Session (Monkey L)
axs[0].plot(time, mean_signal_L, label="Example Session L", color="black", linewidth=2)
axs[0].fill_between(time, mean_signal_L - sem_example_L, mean_signal_L + sem_example_L, color="gray", alpha=0.2, label="±1 SEM")
axs[0].set_title("Example Session (Monkey L)")
axs[0].set_xlabel("Time from MS onset (ms)")
axs[0].set_ylabel("Amplitude Δf/f")
axs[0].legend()
#Grand Analysis (Monkey L)
axs[1].plot(time, mean_L, label="Grand Analysis L", color="blue", linewidth=2)
axs[1].fill_between(time, mean_L - SEM_L, mean_L + SEM_L, color="blue", alpha=0.2, label="±1 SEM")
axs[1].set_title("Grand Analysis (Monkey L)")
axs[1].set_xlabel("Time from MS onset (ms)")
axs[1].axhline(0, color="black", linestyle="--", linewidth=0.8)  # Zero line
axs[1].legend()
plt.tight_layout()
plt.show()


##ploting for monkey G
time = np.linspace(-100, 300, mean_G.shape[0])
fig, axs = plt.subplots(1, 2, figsize=(14, 6), sharey=True)  # 1 row, 2 columns
for ax in axs:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.axvline(0, color="black", linestyle="--", linewidth=0.8)  # Dashed vertical line at x=0
    axs[0].axhline(0, color="black", linestyle="--", linewidth=0.8)  # Zero line
#Example Session (Monkey G)
axs[0].plot(time, mean_signal_G, label="Example Session G", color="black", linewidth=2)
axs[0].fill_between(time, mean_signal_G - sem_example_G, mean_signal_G + sem_example_G, color="gray", alpha=0.2, label="±1 SEM")
axs[0].set_title("Example Session (Monkey G)")
axs[0].set_xlabel("Time from MS onset (ms)")
axs[0].set_ylabel("Amplitude Δf/f")
axs[0].legend()
#Grand Analysis (Monkey G)
axs[1].plot(time, mean_G, label="Grand Analysis G", color="blue", linewidth=2)
axs[1].fill_between(time, mean_G - SEM_G, mean_G + SEM_G, color="blue", alpha=0.2, label="±1 SEM")
axs[1].set_title("Grand Analysis (Monkey G)")
axs[1].set_xlabel("Time from MS onset (ms)")
axs[1].axhline(0, color="black", linestyle="--", linewidth=0.8)  # Zero line
axs[1].legend()
plt.tight_layout()
plt.show()

