import os
from inspect_data.analysis_functions2 import  Session_vector, All_session,calculate_means_around_indices,min_max_times,adding_shuffled
from my_project.inspect_data.preprocessing_functions import ask_question
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
This file plots figure 2 for each monkey , you can choose what monkey you want. 
'''

mask_path = DATA_PATH[2]
output_folder = DATA_PATH[3]
shuffle_path=DATA_PATH[4]


monkey=ask_question("which monkey do you want to do the analysis? legolas/gandalf",'legolas','gandalf')
#monkey='legolas'

#calculating all sessions mean vector
# Monkey G 
mean_signals, sem_signals = All_session(files_path=output_folder, monkey=monkey)
''' mean_signals - a list of all sessions mean vectors 
    sem_signals - a list of all sessions sem vectors 
'''

mean_signals_array = np.array(mean_signals)  # Shape: (num_sessions, 50)
sem_signals_array = np.array(sem_signals)    # Shape: (num_sessions, 50) 
all_session_mean = np.nanmean(mean_signals_array, axis=0) #mean vector of signals
all_session_SEM=np.nanmean(sem_signals_array,axis=0)  #mean vector of sem
grand_significant_indices,grand_shuffled_vector=adding_shuffled(shuffle_path,'GrandAnal',mean_signals_array.T,monkey)

#Time course of the VSD signal for the example session
if monkey=='gandalf':
    file_path = "C:\myprojects\data\output/gandalf_240718united_modified.npy"
else: #monkey='legolas'
    file_path="C:\myprojects\data\output/legolas_111108united_modified.npy"
mean_signal,sem_example=Session_vector(file_path)
##adding shuffle
session_data =np.load(file_path) #session data (10000x50x60)=(pix x timeFrame x MS)
session_data=np.nanmean(session_data,axis=0) #session data (50x60)=(timeFrame x MS)
significant_indices,shuffled_vector=adding_shuffled(shuffle_path,'ExampleSession',session_data,monkey)

##plot figure 2B- TC of signal for example session and for grand analysis
time= np.arange(-150,341,10)
fig, axs = plt.subplots(1, 2, figsize=(14, 6))  # 1 row, 2 columns
for ax in axs:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.axvline(0, color="black", linestyle="--", linewidth=0.8)  # Dashed vertical line at x=0
    ax.axhline(0, color="black", linestyle="--", linewidth=0.8)  # Zero line
# Example Session 
axs[0].plot(time, mean_signal, label="Example Session", color="green", linewidth=2)
axs[0].fill_between(time, mean_signal - sem_example, mean_signal + sem_example, color="green", alpha=0.2, label="±1 SEM")
axs[0].set_title(f"Example Session ({monkey})",fontsize=16)
axs[0].set_xlabel("Time from MS onset (ms)",fontsize=14)
axs[0].set_ylabel("Amplitude Δf/f (x10^-4)",fontsize=14)
axs[0].set_yticks([-0.0002,0,0.0002,0.0004])
axs[0].set_yticklabels(['-2','0','2','4'])
# Add Shuffle Vector
axs[0].plot(time, shuffled_vector[0], label="Shuffle", color="black", linestyle="--", linewidth=1)
axs[0].fill_between(time,shuffled_vector[0] - shuffled_vector[1], 
    shuffled_vector[0] + shuffled_vector[1], 
    color="gray", alpha=0.2,  # Transparency
    label="Shuffle ± SEM")
# Add * Markers for Significant Frames
axs[0].scatter(time[significant_indices],[0.00035]*len(significant_indices) , color="red", marker="*", s=80, label="Significant")
axs[0].legend()

#Grand Analysis (Monkey L)
axs[1].plot(time, all_session_mean, label="Grand Analysis", color="blue", linewidth=2)
axs[1].fill_between(time, all_session_mean - all_session_SEM , all_session_mean + all_session_SEM, color="blue", alpha=0.2, label="±1 SEM")
axs[1].set_title(f"Grand Analysis ({monkey})",fontsize=16)
axs[1].set_xlabel("Time from MS onset (ms)",fontsize=14)
axs[1].set_ylabel("Amplitude Δf/f (x10^-4)",fontsize=14)
axs[1].set_yticks([-0.0001,0,0.0001,0.0002])
axs[1].set_yticklabels(['-1','0','1','2'])
# Add Shuffle Vector
axs[1].plot(time, grand_shuffled_vector[0], label="Shuffle", color="black", linestyle="--", linewidth=1)
axs[1].fill_between(time,grand_shuffled_vector[0] - grand_shuffled_vector[1], 
    grand_shuffled_vector[0] + grand_shuffled_vector[1], 
    color="gray", alpha=0.2,  # Transparency
    label="Shuffle ± SEM")
# Add * Markers for Significant Frames
axs[1].scatter(time[grand_significant_indices],[0.00025]*len(grand_significant_indices) , color="red", marker="*", s=80, label="Significant")
axs[1].legend()
plt.tight_layout()



##Figure 2 D or H
#calculating the min amd max ind from grand analysis
sliced_all_session=all_session_mean[15:40]
min_idx=np.argmin(sliced_all_session)+15
max_idx=np.argmax(sliced_all_session)+15
print  ( f"{monkey}: min:{time[min_idx]}, max:{time[max_idx]}")

#calculating the avg amp of the signal for every session 
#This function calculates the mean amp of three idx around suppression and enhancement peak amplitude for every session
min_amp,max_amp=calculate_means_around_indices(mean_signals_array,min_idx,max_idx) 

#time vector of min and max for each monkey
min_time,max_time=min_max_times(mean_signals_array,time)

#data for ploting
categories=["supp.","enha."]
#monkey L
amplitudes=[min_amp[1],max_amp[1]]
errors_amp=[min_amp[2],max_amp[2]]
times=[min_time[1],max_time[1]]
errors_time=[min_time[2],max_time[2]]


##ploting figure D, H
#monkey L
fig, axs = plt.subplots(1, 2, figsize=(12, 10))
# Left plot: Amplitude Δf/f
axs[0].bar(categories, amplitudes, yerr=errors_amp, color=["dimgray", "silver"])
axs[0].set_ylabel("Amplitude Δf/f (x10^-4)", fontsize=14)
axs[0].axhline(0, color="black", linewidth=0.8)  # Zero line
axs[0].set_yticks([-0.0001,0,0.0001,0.0002,0.0003])
axs[0].set_yticklabels(['-1','0','1','2','3']) 
axs[0].set_title(f"Suppression and Enhancement Amplitudes ({monkey})", fontsize=14)

if min_amp[3][1] < 0.05:  # Check p-value for amplitude
    axs[0].text(0.03, 0.0002, "*", ha="center", fontsize=20)
if max_amp[3][1] < 0.05:  # Check p-value for amplitude
    axs[0].text(1, 0.0002, "*", ha="center", fontsize=20)

#rank sum between supp and enha:
RS_amp=ranksums(min_amp[0],max_amp[0],alternative='two-sided')
if RS_amp[1]<0.005:
    axs[0].text(0.5,0.00025, "***",ha="center", fontsize=20)

# Right plot: Time to Peak
axs[1].bar(categories, times,yerr=errors_time , color=["dimgray", "silver"])
axs[1].set_ylabel("Time to Peak (ms)", fontsize=20)
axs[1].set_ylim([0, 300])  
axs[1].set_title(f"Time to Peak ({monkey})", fontsize=20)

if min_time[3][1] < 0.05:  # Check p-value for amplitude
    axs[1].text(0.03,200, "*", ha="center", fontsize=20)
if max_time[3][1] < 0.05:  # Check p-value for amplitude
    axs[1].text(1,200, "*", ha="center", fontsize=20)
#rank sum between supp and enha
RS_time=ranksums(min_time[0],max_time[0],alternative='two-sided')
if RS_time[1]<0.005:
    axs[1].text(0.5,250, "***",ha="center", fontsize=20)


# Adjust layout
plt.tight_layout()
plt.show()