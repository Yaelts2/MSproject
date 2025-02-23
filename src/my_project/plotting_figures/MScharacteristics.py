import os
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from my_project.config import DATA_PATH
from my_project.inspect_data.MScharacteristics_functions import extract_data_matlab
from scipy.stats import pearsonr,sem


##Figure 1
# input: matlab tables that has the information i need for this figure : MS amp and MS max velocity
# for loop to Go through all the data and extract the needed data:

# Monkey L:
all_ms_amp_L = []
all_max_velocity_L = []
for file_name in os.listdir(DATA_PATH[1]):
    if file_name.endswith("msMats.mat"):  # the only files i need for this analysis
        all_ms_amp_L.append(extract_data_matlab(file_name, 5, DATA_PATH[1], "msMats"))
        all_max_velocity_L.append(extract_data_matlab(file_name, 7, DATA_PATH[1], "msMats"))
all_ms_amp_L = np.concatenate(all_ms_amp_L)
all_max_velocity_L = np.concatenate(all_max_velocity_L)
print ("mean amplitude for mankey L: ", np.mean(all_ms_amp_L))
print("SEM for amplitude for monkey L: ", sem(all_ms_amp_L))

# Monkey G:
all_ms_amp_G = []
all_max_velocity_G = []
for file_name in os.listdir(DATA_PATH[0]):
    if file_name.endswith("msMats.mat"):  # the only files i need for this analysis
        all_ms_amp_G.append(extract_data_matlab(file_name, 5, DATA_PATH[0], "msMats"))
        all_max_velocity_G.append(extract_data_matlab(file_name, 7, DATA_PATH[0], "msMats"))
all_ms_amp_G = np.concatenate(all_ms_amp_G)
all_max_velocity_G = np.concatenate(all_max_velocity_G)
print ("mean amplitude for mankey G: ", np.mean(all_ms_amp_G))
print("SEM for amplitude for monkey G: ", sem(all_ms_amp_G))

# Figure 1B:
fig, axs = plt.subplots(1, 2, figsize=(12, 6), sharey=True)

# Histogram for Monkey L
sns.histplot(all_ms_amp_L, bins=18,kde=False,color="gray",edgecolor="black",stat="percent",ax=axs[0])
axs[0].set_title("Monkey L", fontsize=20)
axs[0].set_xlabel("Amplitude (deg)", fontsize=17)
axs[0].set_ylabel("Percentage (%)", fontsize=17)
axs[0].set_ylim(0, 25)  

# Histogram for Monkey G
sns.histplot(all_ms_amp_G,bins=18,kde=False,color="gray",edgecolor="black",stat="percent",ax=axs[1])
axs[1].set_title("Monkey G", fontsize=20)
axs[1].set_xlabel("Amplitude (deg)", fontsize=17)
axs[1].set_ylabel("Percentage (%)", fontsize=17)
axs[1].set_ylim(0, 25)  
plt.tight_layout()
plt.show()


r_l, p_l = pearsonr(all_ms_amp_L, all_max_velocity_L)
r_l=round(r_l,2)
r_G, p_G=pearsonr(all_ms_amp_G,all_max_velocity_G)
r_G=round(r_G,2)
print (f"monkey L: r={r_l} and p={p_l}")
print (f"monkey G: r={r_G} and p={p_G}")

# Figure 1C:
fig, axs = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

# Monkey L
sns.regplot(x=all_ms_amp_L, y=all_max_velocity_L, ax=axs[0],ci=None, scatter_kws={"alpha": 0.7}, line_kws={"color": "red"})
axs[0].set_title("Monkey L", fontsize=20)
axs[0].set_xlabel("Amplitude (deg)", fontsize=17)
axs[0].set_ylabel("Max Velocity (deg/sec)", fontsize=17)
axs[0].set_xticks([0.2, 0.4, 0.6, 0.8, 1.0])
axs[0].set_yticks([10, 20, 40, 60, 80, 100])
axs[0].text(0.3,80,f"r={r_l}\n p<0.001", fontsize=17)

# Scatter plot with regression for Monkey G
sns.regplot(x=all_ms_amp_G, y=all_max_velocity_G, ax=axs[1],ci=None, scatter_kws={"alpha": 0.7}, line_kws={"color": "red"})
axs[1].set_title("Monkey G", fontsize=20)
axs[1].set_xlabel("Amplitude (deg)", fontsize=17)
axs[1].set_ylabel("Max Velocity (deg/sec)", fontsize=17)
axs[1].set_xticks([0.2, 0.4, 0.6, 0.8, 1.0])  # Replace with desired x-tick values
axs[1].set_yticks([10, 20, 40, 60, 80, 100])
axs[1].text(0.3,80,f"r={r_G}\n p<0.001", fontsize=17)

plt.tight_layout()
plt.show()
