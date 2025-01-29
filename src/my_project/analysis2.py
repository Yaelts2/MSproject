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





# Define paths
gandalf_path = DATA_PATH[0]
legolas_path= DATA_PATH[1]
mask_path = DATA_PATH[2]
output_folder = DATA_PATH[3]
shuffle_path=DATA_PATH[4]



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
    


#calculating all sessions mean vector
# Monkey G 
mean_signals_G, sem_signals_G = All_session(files_path=output_folder, monkey='gandalf')
''' mean_signals_G - a list of all sessions mean vectors - monkey G
    sem_signala_G - a list of all sessions sem vectors - monkey G
'''

mean_signals_array_G = np.array(mean_signals_G)  # Shape: (num_sessions, 50)
sem_signals_array_G = np.array(sem_signals_G)    # Shape: (num_sessions, 50) 
all_session_mean_G = np.nanmean(mean_signals_array_G, axis=0) #mean vector of signals
all_session_SEM_G=np.nanmean(sem_signals_array_G,axis=0)  #mean vector of sem
grand_matrix_G=create_grand_matrix(output_folder,'gandalf')
grand_significant_indices_G,grand_shuffled_vector_G=adding_shuffled(shuffle_path,'GrandAnal',mean_signals_array_G.T,'gandalf')



#Monkey L
mean_signals_L, sem_signals_L = All_session(files_path=output_folder, monkey='legolas')
''' mean_signals_L - a list of all sessions mean vectors - monkey L
    sem_signals_L - a list of all sessions sem vectors - monkey L
'''
mean_signals_array_L = np.array(mean_signals_L)  # Shape: (num_sessions, 50)
sem_signals_array_L = np.array(sem_signals_L)    # Shape: (num_sessions, 50) 
all_session_mean_L = np.nanmean(mean_signals_array_L, axis=0)
all_session_SEM_L = np.nanmean(sem_signals_array_L,axis=0)
grand_significant_indices_L,grand_shuffled_vector_L=adding_shuffled(shuffle_path,'GrandAnal',mean_signals_array_L.T,'legolas')



# #Time course of the VSD signal for the example session
# Monkey G
file_path_G = "C:\myprojects\data\output/gandalf_240718united_modified.npy"
mean_signal_G,sem_example_G=Session_vector(file_path_G)
##adding shuffle
session_data_G =np.load(file_path_G) #session data (10000x50x60)=(pix x timeFrame x MS)
session_data_G=np.nanmean(session_data_G,axis=0) #session data (50x60)=(timeFrame x MS)
significant_indices_G,shuffled_vector_G=adding_shuffled(shuffle_path,'ExampleSession',session_data_G,'gandalf')


# Monkey L
file_path_L = "C:\myprojects\data\output/legolas_111108united_modified.npy"
mean_signal_L,sem_example_L=Session_vector(file_path_L)
##adding shuffle
session_data_L =np.load(file_path_L) #session data (10000x50x60)=(pix x timeFrame x MS)
session_data_L=np.nanmean(session_data_L,axis=0) #session data (50x60)=(timeFrame x MS)
significant_indices_L,shuffled_vector_L=adding_shuffled(shuffle_path,'ExampleSession',session_data_L,'legolas')


##plot for monkey L
time= np.arange(-150,341,10)
fig, axs = plt.subplots(1, 2, figsize=(14, 6))  # 1 row, 2 columns
for ax in axs:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.axvline(0, color="black", linestyle="--", linewidth=0.8)  # Dashed vertical line at x=0
    ax.axhline(0, color="black", linestyle="--", linewidth=0.8)  # Zero line
# Example Session (Monkey L)
axs[0].plot(time, mean_signal_L, label="Example Session L", color="green", linewidth=2)
axs[0].fill_between(time, mean_signal_L - sem_example_L, mean_signal_L + sem_example_L, color="green", alpha=0.2, label="±1 SEM")
axs[0].set_title("Example Session (Monkey L)",fontsize=16)
axs[0].set_xlabel("Time from MS onset (ms)",fontsize=14)
axs[0].set_ylabel("Amplitude Δf/f (x10^-4)",fontsize=14)
axs[0].set_yticks([-0.0002,0,0.0002,0.0004])
axs[0].set_yticklabels(['-2','0','2','4'])
# Add Shuffle Vector
axs[0].plot(time, shuffled_vector_L[0], label="Shuffle", color="black", linestyle="--", linewidth=1)
axs[0].fill_between(time,shuffled_vector_L[0] - shuffled_vector_L[1], 
    shuffled_vector_L[0] + shuffled_vector_L[1], 
    color="gray", alpha=0.2,  # Transparency
    label="Shuffle ± SEM")
# Add * Markers for Significant Frames
axs[0].scatter(time[significant_indices_L],[0.00035]*len(significant_indices_L) , color="red", marker="*", s=80, label="Significant")
axs[0].legend()

#Grand Analysis (Monkey L)
axs[1].plot(time, all_session_mean_L, label="Grand Analysis L", color="blue", linewidth=2)
axs[1].fill_between(time, all_session_mean_L - all_session_SEM_L , all_session_mean_L + all_session_SEM_L, color="blue", alpha=0.2, label="±1 SEM")
axs[1].set_title("Grand Analysis (Monkey L)",fontsize=16)
axs[1].set_xlabel("Time from MS onset (ms)",fontsize=14)
axs[1].set_ylabel("Amplitude Δf/f (x10^-4)",fontsize=14)
axs[1].set_yticks([-0.0001,0,0.0001,0.0002])
axs[1].set_yticklabels(['-1','0','1','2'])
# Add Shuffle Vector
axs[1].plot(time, grand_shuffled_vector_L[0], label="Shuffle", color="black", linestyle="--", linewidth=1)
axs[1].fill_between(time,grand_shuffled_vector_L[0] - grand_shuffled_vector_L[1], 
    grand_shuffled_vector_L[0] + grand_shuffled_vector_L[1], 
    color="gray", alpha=0.2,  # Transparency
    label="Shuffle ± SEM")
# Add * Markers for Significant Frames
axs[1].scatter(time[grand_significant_indices_L],[0.00025]*len(grand_significant_indices_L) , color="red", marker="*", s=80, label="Significant")
axs[1].legend()
plt.tight_layout()


##ploting for monkey G
plt.figure(1)
fig, axs = plt.subplots(1, 2, figsize=(14, 6))  # 1 row, 2 columns
for ax in axs:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.axvline(0, color="black", linestyle="--", linewidth=0.8)  # Dashed vertical line at x=0
    ax.axhline(0, color="black", linestyle="--", linewidth=0.8)  # Zero line
#Example Session (Monkey G)
axs[0].plot(time, mean_signal_G, label="Example Session G", color="green", linewidth=2)
axs[0].fill_between(time, mean_signal_G - sem_example_G, mean_signal_G + sem_example_G, color="green", alpha=0.2, label="±1 SEM")
axs[0].set_title("Example Session (Monkey G)")
axs[0].set_xlabel("Time from MS onset (ms)")
axs[0].set_ylabel("Amplitude Δf/f(x10^-4)")
axs[0].set_yticks([-0.0001,0,0.0001])
axs[0].set_yticklabels(['-1','0','1'])
# Add Shuffle Vector
axs[0].plot(time, shuffled_vector_G[0], label="Shuffle", color="black", linestyle="--", linewidth=1)
axs[0].fill_between(time,shuffled_vector_G[0] - shuffled_vector_G[1], 
    shuffled_vector_G[0] + shuffled_vector_G[1], 
    color="gray", alpha=0.2,  # Transparency
    label="Shuffle ± SEM")
# Add * Markers for Significant Frames
axs[0].scatter(time[significant_indices_G],[0.00015]*len(significant_indices_G) , color="red", marker="*", s=80, label="Significant")
axs[0].legend()

#Grand Analysis (Monkey G)
axs[1].plot(time, all_session_mean_G, label="Grand Analysis G", color="blue", linewidth=2)
axs[1].fill_between(time, all_session_mean_G - all_session_SEM_G, all_session_mean_G + all_session_SEM_G, color="blue", alpha=0.2, label="±1 SEM")
axs[1].set_title("Grand Analysis (Monkey G)")
axs[1].set_xlabel("Time from MS onset (ms)")
axs[1].set_ylabel("Amplitude Δf/f(x10^-4)")
axs[1].set_yticks([-0.0001,0,0.0001])
axs[1].set_yticklabels(['-1','0','1'])
# Add Shuffle Vector
axs[1].plot(time, grand_shuffled_vector_G[0], label="Shuffle", color="black", linestyle="--", linewidth=1)
axs[1].fill_between(time,grand_shuffled_vector_G[0] - grand_shuffled_vector_G[1], 
    grand_shuffled_vector_G[0] + grand_shuffled_vector_G[1], 
    color="gray", alpha=0.2,  # Transparency
    label="Shuffle ± SEM")
# Add * Markers for Significant Frames
axs[1].scatter(time[grand_significant_indices_G],[0.00015]*len(grand_significant_indices_G) , color="red", marker="*", s=80, label="Significant")
axs[1].legend()
plt.tight_layout()
plt.show()


##Figure 2 D and H
#calculating the min amd max ind from grand analysis
#monkey G
sliced_all_session_G=all_session_mean_G[15:40 ]
min_idx_G=np.argmin(sliced_all_session_G)+16
max_idx_G=np.argmax(sliced_all_session_G)+16
#monkey L
sliced_all_session_L=all_session_mean_L[15:40]
min_idx_L=np.argmin(sliced_all_session_L)+15
max_idx_L=np.argmax(sliced_all_session_L)+15

print("monkey G:", time[min_idx_G],time[max_idx_G])
print("monkey L:", time[min_idx_L],time[max_idx_L])

#calculating the avg amp of the signal for every session 
#This function calculates the mean amp of three idx around suppression and enhancement peak amplitude for every session
min_amp_G,max_amp_G=calculate_means_around_indices(mean_signals_array_G,min_idx_G,max_idx_G) 
min_amp_L,max_amp_L=calculate_means_around_indices(mean_signals_array_L,min_idx_L,max_idx_L)

#time vector of min and max for each monkey
min_time_l,max_time_l=min_max_times(mean_signals_array_L,time)
min_time_G,max_time_G=min_max_times(mean_signals_array_G,time)


#data for ploting
categories=["supp.","enha."]
#monkey L
amplitudes_L=[min_amp_L[1],max_amp_L[1]]
errors_amp_L=[min_amp_L[2],max_amp_L[2]]
times_l=[min_time_l[1],max_time_l[1]]
errors_time_l=[min_time_l[2],max_time_l[2]]
#monkey G
amplitudes_G=[min_amp_G[1],max_amp_G[1]]
errors_amp_G=[min_amp_G[2],max_amp_G[2]]
times_G=[min_time_G[1],max_time_G[1]]
errors_time_G=[min_time_G[2],max_time_G[2]]


##ploting figure D, H
#monkey L
fig, axs = plt.subplots(1, 2, figsize=(12, 10))
# Left plot: Amplitude Δf/f
axs[0].bar(categories, amplitudes_L, yerr=errors_amp_L, color=["dimgray", "silver"])
axs[0].set_ylabel("Amplitude Δf/f (x10^-4)", fontsize=14)
axs[0].axhline(0, color="black", linewidth=0.8)  # Zero line
axs[0].set_yticks([-0.0001,0,0.0001,0.0002,0.0003])
axs[0].set_yticklabels(['-1','0','1','2','3']) 
axs[0].set_title("Suppression and Enhancement Amplitudes (Monkey L)", fontsize=14)

if min_amp_L[3][1] < 0.05:  # Check p-value for amplitude
    axs[0].text(0.03, 0.0002, "*", ha="center", fontsize=20)
if max_amp_L[3][1] < 0.05:  # Check p-value for amplitude
    axs[0].text(1, 0.0002, "*", ha="center", fontsize=20)

#rank sum between supp and enha:
RS_amp_L=ranksums(min_amp_L[0],max_amp_L[0],alternative='two-sided')
if RS_amp_L[1]<0.005:
    axs[0].text(0.5,0.00025, "***",ha="center", fontsize=20)

# Right plot: Time to Peak
axs[1].bar(categories, times_l,yerr=errors_time_l , color=["dimgray", "silver"])
axs[1].set_ylabel("Time to Peak (ms)", fontsize=20)
axs[1].set_ylim([0, 300])  
axs[1].set_title("Time to Peak (Monkey L)", fontsize=20)

if min_time_l[3][1] < 0.05:  # Check p-value for amplitude
    axs[1].text(0.03,200, "*", ha="center", fontsize=16)
if max_time_l[3][1] < 0.05:  # Check p-value for amplitude
    axs[1].text(1,200, "*", ha="center", fontsize=16)
#rank sum between supp and enha
RS_time_L=ranksums(min_time_l[0],max_time_l[0],alternative='two-sided')
if RS_time_L[1]<0.005:
    axs[1].text(0.5,250, "***",ha="center", fontsize=16)

#monkey G
fig, axs = plt.subplots(1, 2, figsize=(12, 10))
# Left plot: Amplitude Δf/f
axs[0].bar(categories, amplitudes_G, yerr=errors_amp_G, color=["dimgray", "silver"])
axs[0].set_ylabel("Amplitude Δf/f (x10^-4)", fontsize=14)
axs[0].axhline(0, color="black", linewidth=0.8)  # Zero line
axs[0].set_yticks([-0.00005,0,0.00005,0.0001,0.00015])
axs[0].set_yticklabels(['-0.5','0','0.5','1','1.5']) 
axs[0].set_title("Suppression and Enhancement Amplitudes (Monkey G)", fontsize=14)

if min_amp_G[3][1] < 0.05:  # Check p-value for amplitude
    axs[0].text(0.03, 0.0001, "*", ha="center", fontsize=20)
if max_amp_G[3][1] < 0.05:  # Check p-value for amplitude
    axs[0].text(1, 0.0001, "*", ha="center", fontsize=20)
#rank sum between supp and enha:
RS_amp_G=ranksums(min_amp_G[0],max_amp_G[0],alternative='two-sided')
if RS_amp_G[1]< 0.005:
    axs[0].text(0.5,0.000125, "***",ha="center", fontsize=20)

# Right plot: Time to Peak
axs[1].bar(categories, times_G,yerr=errors_time_G , color=["dimgray", "silver"])
axs[1].set_ylabel("Time to Peak (ms)", fontsize=20)
axs[1].set_ylim([0, 300])  
axs[1].set_title("Time to Peak (Monkey G)", fontsize=20)

if min_time_G[3][1] < 0.05:  # Check p-value for amplitude
    axs[1].text(0.03,230, "*", ha="center", fontsize=16)
if max_time_G[3][1] < 0.05:  # Check p-value for amplitude
    axs[1].text(1,230, "*", ha="center", fontsize=16)
#rank sum between supp and enha
RS_time_G=ranksums(min_time_G[0],max_time_G[0],alternative='two-sided')
if RS_time_G[1]< 0.005:
    axs[1].text(0.5,260, "***",ha="center", fontsize=16)

# Adjust layout
plt.tight_layout()
plt.show()
