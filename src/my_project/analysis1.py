from scipy.io import loadmat
import os 
from config import DATA_PATH
import pandas as pd
from inspect_Data import extrctingDATA_fromMAT
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



##Figure 1
# input: matlab tables that has the information i need for this figure : MS amp and MS max velocity
#for loop to Go through all the data and extract the needed data:

#Monkey L:
all_ms_amp_L = []
all_max_velocity_L = []
for file_name in os.listdir(DATA_PATH[1]):
    if file_name.endswith("msMats.mat"): #the only files i need for this analysis
        all_ms_amp_L.append(extrctingDATA_fromMAT(file_name,5,DATA_PATH[1],'msMats'))
        all_max_velocity_L.append(extrctingDATA_fromMAT(file_name,7,DATA_PATH[1],'msMats'))
all_ms_amp_L=np.concatenate( all_ms_amp_L)
all_max_velocity_L=np.concatenate(all_max_velocity_L)

#Monkey G:
all_ms_amp_G = []
all_max_velocity_G = []
for file_name in os.listdir(DATA_PATH[0]):
    if file_name.endswith("msMats.mat"): #the only files i need for this analysis
        all_ms_amp_G.append(extrctingDATA_fromMAT(file_name,5,DATA_PATH[0],'msMats'))
        all_max_velocity_G.append(extrctingDATA_fromMAT(file_name,7,DATA_PATH[0],'msMats'))
all_ms_amp_G=np.concatenate( all_ms_amp_G)
all_max_velocity_G=np.concatenate(all_max_velocity_G)



#Figure 1B:
fig, axs = plt.subplots(1, 2, figsize=(10, 5), sharey=True)

# Histogram for Monkey L
axs[0].hist(all_ms_amp_L, bins=18, edgecolor="black", color='gray')
axs[0].set_title("Monkey L")
axs[0].set_xlabel("Amplitude (deg)")
axs[0].set_ylabel("Percentage (%)")

# Histogram for Monkey G
axs[1].hist(all_ms_amp_G, bins=18, edgecolor="black", color='gray')
axs[1].set_title("Monkey G")
axs[1].set_xlabel("Amplitude (deg)")

plt.tight_layout()
plt.show()

#Figure 1C:
fig, axs = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

#Monkey L
sns.regplot(x=all_ms_amp_L, y=all_max_velocity_L, ax=axs[0], scatter_kws={'alpha': 0.7}, line_kws={'color': 'red'})
axs[0].set_title("Monkey L")
axs[0].set_xlabel("Amplitude (deg)")
axs[0].set_ylabel("Max Velocity (deg/sec)")
axs[0].set_xticks([0.2, 0.4, 0.6, 0.8, 1.0])  
axs[0].set_yticks([10, 20, 40, 60, 80, 100])

# Scatter plot with regression for Monkey G
sns.regplot(x=all_ms_amp_G, y=all_max_velocity_G, ax=axs[1], scatter_kws={'alpha': 0.7}, line_kws={'color': 'red'})
axs[1].set_title("Monkey G")
axs[1].set_xlabel("Amplitude (deg)")
axs[0].set_ylabel("Max Velocity (deg/sec)")
axs[0].set_xticks([0.2, 0.4, 0.6, 0.8, 1.0])  # Replace with desired x-tick values
axs[0].set_yticks([10, 20, 40, 60, 80, 100])

plt.tight_layout()
plt.show()