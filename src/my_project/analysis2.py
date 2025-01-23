import os
from inspect_data.analysis_functions2 import extract_wrong_pix, extractBaseline
from config import DATA_PATH
import numpy as np
import glob
import logging
import matplotlib.pyplot as plt


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
    baseline_substracted=True
print("All files were processed: V1 regions were extracted, noisy pixels were removed, and the baseline was subtracted.")
    

################chack one file
file_path = "C:\myprojects\data\output/gandalf_270618b__modified.npy"
data = np.load(file_path, allow_pickle=True)
# Select a 2D slice for visualization
# Example: Average across microsaccades to get a (pixels, time_frames) matrix
data_for_image=data[:,10,15]
# Display the 2D array using imshow
reshaped_slice = data_for_image.reshape((100, 100))  # Example: 100x100 grid
# Plot the 2D data using imshow
plt.imshow(reshaped_slice, cmap="viridis", aspect="auto")
plt.colorbar(label="Intensity")
plt.title("Visualization of Matrix Slice (:, 10, 12)")
plt.xlabel("X Dimension")
plt.ylabel("Y Dimension")
plt.show()

