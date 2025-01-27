import os
from inspect_data.analysis_functions2 import extract_wrong_pix, extractBaseline, Session_vector, All_session, ask_question,calculate_means_around_indices
from config import DATA_PATH
import numpy as np
import glob
import logging
import matplotlib.pyplot as plt
import tkinter as tk

# Define paths
gandalf_path = DATA_PATH[0]
legolas_path= DATA_PATH[1]
mask_path = DATA_PATH[2]
output_folder = DATA_PATH[3]


user_response=ask_question("does the data needs to extract out of V1 pixels and noisy pixels??")

###extract out of V1 pixels and noisy pixels from all session 
if user_response:
    # monkey Gandalf
    extract_wrong_pix(gandalf_path, mask_path, 'outpix.mat', output_folder)
    ## monkey Legolas
    extract_wrong_pix(legolas_path, mask_path, 'outpix.mat', output_folder)

user_response2=ask_question("does the data needs to extract baseline??")
##extract baseline
# Loop through each file
if user_response2:
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
print("All files were processed: V1 regions were extracted, noisy pixels were removed, and the baseline was subtracted.")
    

# ################check one file
# file_path = "C:\myprojects\data\gandalf/gandalf_100718a_dataByMs_no_BV.mat"
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
mean_signals_G, sem_signals_G = All_session(files_path=output_folder, monkey='gandalf')
''' mean_signals_G - a list of all sessions mean vectors - monkey G
    sem_signala_G - a list of all sessions sem vectors - monkey G
'''
mean_signals_array_G = np.array(mean_signals_G)  # Shape: (num_sessions, 50)
sem_signals_array_G = np.array(sem_signals_G)    # Shape: (num_sessions, 50) 
all_session_mean_G = np.nanmean(mean_signals_array_G, axis=0)
all_session_SEM_G=np.nanmean(sem_signals_array_G,axis=0)
#Monkey L
mean_signals_L, sem_signals_L = All_session(files_path=output_folder, monkey='legolas')
''' mean_signals_L - a list of all sessions mean vectors - monkey L
    sem_signala_L - a list of all sessions sem vectors - monkey L
'''
mean_signals_array_L = np.array(mean_signals_L)  # Shape: (num_sessions, 50)
sem_signals_array_L = np.array(sem_signals_L)    # Shape: (num_sessions, 50) 
all_session_mean_L = np.nanmean(mean_signals_array_L, axis=0)
all_session_SEM_L = np.nanmean(sem_signals_array_L,axis=0)



# #Time course of the VSD signal for the example session
# Monkey G
file_path_G = "C:\myprojects\data\output/gandalf_240718united__modified.npy"
mean_signal_G,sem_example_G=Session_vector(file_path_G)
# Monkey L
file_path_L = "C:\myprojects\data\output/legolas_111108united__modified.npy"
mean_signal_L,sem_example_L=Session_vector(file_path_L)



##plot for monkey L
time_L = np.linspace(-100, 300, all_session_mean_L.shape[0])
fig, axs = plt.subplots(1, 2, figsize=(14, 6))  # 1 row, 2 columns
for ax in axs:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.axvline(0, color="black", linestyle="--", linewidth=0.8)  # Dashed vertical line at x=0
    ax.axhline(0, color="black", linestyle="--", linewidth=0.8)  # Zero line
# Example Session (Monkey L)
axs[0].plot(time_L, mean_signal_L, label="Example Session L", color="black", linewidth=2)
axs[0].fill_between(time_L, mean_signal_L - sem_example_L, mean_signal_L + sem_example_L, color="gray", alpha=0.2, label="±1 SEM")
axs[0].set_title("Example Session (Monkey L)",fontsize=16)
axs[0].set_xlabel("Time from MS onset (ms)",fontsize=14)
axs[0].set_ylabel("Amplitude Δf/f (x10^-4)",fontsize=14)
axs[0].set_yticks([-0.0002,0,0.0002,0.0004])
axs[0].set_yticklabels(['-2','0','2','4'])
axs[0].legend()
#Grand Analysis (Monkey L)
axs[1].plot(time_L, all_session_mean_L, label="Grand Analysis L", color="blue", linewidth=2)
axs[1].fill_between(time_L, all_session_mean_L - all_session_SEM_L , all_session_mean_L + all_session_SEM_L, color="blue", alpha=0.2, label="±1 SEM")
axs[1].set_title("Grand Analysis (Monkey L)",fontsize=16)
axs[1].set_xlabel("Time from MS onset (ms)",fontsize=14)
axs[1].set_ylabel("Amplitude Δf/f (x10^-4)",fontsize=14)
axs[1].set_yticks([-0.0001,0,0.0001,0.0002])
axs[1].set_yticklabels(['-1','0','1','2'])
axs[1].legend()
plt.tight_layout()


##ploting for monkey G
time_G = np.linspace(-100, 300, all_session_mean_G.shape[0])
plt.figure(1)
fig, axs = plt.subplots(1, 2, figsize=(14, 6))  # 1 row, 2 columns
for ax in axs:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.axvline(0, color="black", linestyle="--", linewidth=0.8)  # Dashed vertical line at x=0
    ax.axhline(0, color="black", linestyle="--", linewidth=0.8)  # Zero line
#Example Session (Monkey G)
axs[0].plot(time_G, mean_signal_G, label="Example Session G", color="black", linewidth=2)
axs[0].fill_between(time_G, mean_signal_G - sem_example_G, mean_signal_G + sem_example_G, color="gray", alpha=0.2, label="±1 SEM")
axs[0].set_title("Example Session (Monkey G)")
axs[0].set_xlabel("Time from MS onset (ms)")
axs[0].set_ylabel("Amplitude Δf/f(x10^-4)")
axs[0].set_yticks([-0.0001,0,0.0001])
axs[0].set_yticklabels(['-1','0','1'])
axs[0].legend()
#Grand Analysis (Monkey G)
axs[1].plot(time_G, all_session_mean_G, label="Grand Analysis G", color="blue", linewidth=2)
axs[1].fill_between(time_G, all_session_mean_G - all_session_SEM_G, all_session_mean_G + all_session_SEM_G, color="blue", alpha=0.2, label="±1 SEM")
axs[1].set_title("Grand Analysis (Monkey G)")
axs[1].set_xlabel("Time from MS onset (ms)")
axs[1].set_ylabel("Amplitude Δf/f(x10^-4)")
axs[1].set_yticks([-0.0001,0,0.0001])
axs[1].set_yticklabels(['-1','0','1'])
axs[1].legend()
plt.tight_layout()
plt.show()


##Figure 2 D and H
#calculating the min amd max ind for min, max time and min,max amp 
#monkey G
min_idx_G=np.argmin(all_session_mean_G)
min_time_G=time_G[min_idx_G]
max_idx_G=np.argmax(all_session_mean_G)
max_time_G=time_G[max_idx_G]
#monkey L
min_idx_L=np.argmin(all_session_mean_L)
min_time_L=time_L[min_idx_L]
max_idx_L=np.argmax(all_session_mean_L)
max_time_L=time_L[max_idx_L]


#calculating the avg amp of the signal for every session 
#This function calculates the mean amp of three idx around suppression and enhancement peak amplitude for every session
#returns the mean value of all sessions
min_amp_G_mean,max_amp_G_mean,min_amp_G_sem,max_amp_G_sem=calculate_means_around_indices(mean_signals_G,min_idx_G,max_idx_G) # 2 lists of mean amp in min and in max for monkey G
min_amp_L_mean,max_amp_L_mean,min_amp_L_sem,max_amp_L_sem=calculate_means_around_indices(mean_signals_L,min_idx_L,max_idx_L)# 2 lists of mean amp in min and in max for monkey L


## Data for plotting
categories = ["supp.", "enha."]
# Amplitudes
amplitudes_G = [min_amp_G_mean, max_amp_G_mean]
errors_amp_G = [min_amp_G_sem, max_amp_G_sem]
amplitudes_L = [min_amp_L_mean, max_amp_L_mean]
errors_amp_L = [min_amp_L_sem, max_amp_L_sem]

print("monkey L amp: ",amplitudes_L,"\nmonkey G amp: ", amplitudes_G)
# Times
times_G = [min_time_G, max_time_G]
times_L = [min_time_L, max_time_L]
print("monkey L time: ",times_L,"\nmonkey G time: ", times_G)

fig, axs = plt.subplots(1, 2, figsize=(12, 6))
# Left plot: Amplitude Δf/f
axs[0].bar(categories, amplitudes_L, yerr=errors_amp_L, color=["dimgray", "silver"])
axs[0].set_ylabel("Amplitude Δf/f (x10^-4)", fontsize=14)
axs[0].axhline(0, color="black", linewidth=0.8)  # Zero line
axs[0].set_yticks([-0.0001,0,0.0001,0.0002])
axs[0].set_yticklabels(['-1','0','1','2']) 
axs[0].set_title("Suppression and Enhancement Amplitudes (Monkey L)", fontsize=14)

# Right plot: Time to Peak
axs[1].bar(categories, times_L, color=["darkgray", "lightgray"])
axs[1].set_ylabel("Time to Peak (ms)", fontsize=14)
axs[1].set_ylim([0, 250])  
axs[1].set_title("Time to Peak (Monkey L)", fontsize=14)

# Adjust layout
plt.tight_layout()
plt.show()
