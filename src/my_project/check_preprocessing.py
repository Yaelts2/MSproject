import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
import os
from config import DATA_PATH
import glob

'''
This file is for conforming the preprocessing on the data by showing the map of chamber to
see if the right pixels were extracted.
one map before preprocessing and secound map after preprocessing.
you can change the file name

'''
# #open Before preprocessing 
# file_name_B="C:\myprojects\data\gandalf/gandalf_100718a_dataByMs_no_BV.mat"
# file_path_B = os.path.join(DATA_PATH[0], file_name_B) 
# data_B = loadmat(file_path_B)
# data_B= data_B['dataByMs_no_BV']
# data_for_image_B=data_B[:,10,15]
# # Display the 2D array using imshow
# reshaped_slice_B = data_for_image_B.reshape((100, 100))  
# # Plot the 2D data using imshow
# plt.figure(0)
# plt.imshow(reshaped_slice_B, cmap="viridis", aspect="auto")
# plt.colorbar(label="Intensity")
# plt.title("Visualization of Matrix Slice (:, 10, 12)")
# plt.xlabel("X Dimension")
# plt.ylabel("Y Dimension")
# plt.show()


# ##open After preprocessing
# file_name_A = "C:\myprojects\data\output/gandalf_100718a__modified.npy"
# file_path_A= np.load(file_name_A, allow_pickle=True)
# #2D slice for visualization
# data_for_image_A=file_path_A[:,10,15]
# # Display the 2D array using imshow
# reshaped_slice_A = data_for_image_A.reshape((100, 100)) 
# # Plot the 2D data using imshow
# plt.figure(1)
# plt.imshow(reshaped_slice_A, cmap="viridis", aspect="auto")
# plt.colorbar(label="Intensity")
# plt.title("Visualization of Matrix Slice (:, 10, 12)")
# plt.xlabel("X Dimension")
# plt.ylabel("Y Dimension")
# plt.show()




# file_path = os.path.join('C:\myprojects\data\shuffled', 'gandalfExampleSession_shuffledData.mat')
# shuffle=loadmat(file_path)
# shuffle=next(reversed(shuffle.values()))

# file_path_s = os.path.join('C:\myprojects\data\output', 'gandalf_270618b__modified.npy')
# data=np.load(file_path_s)
# data=np.nanmean(data,axis=0)
# print(type(data), data.shape, np.sum(np.isnan(data)))
# print(type(shuffle), shuffle.shape, np.sum(np.isnan(shuffle)))



print(grand_G.shape)

    