from inspect_data.analysis_functions2 import extract_wrong_pix
from config import DATA_PATH

# Define paths
gandalf_path = DATA_PATH[0]
legolas_path= DATA_PATH[1]
mask_path = DATA_PATH[2]
output_folder = DATA_PATH[3]
## monkey Gandalf
#extracting outOfV1 mask
#extract_wrong_pix(gandalf_path, mask_path, 'outOfV11.mat', output_folder)
#extracting noisyPixels
extract_wrong_pix(gandalf_path, mask_path, 'noisyPixels.mat', output_folder)


## monkey Legolas
#extracting outOfV1 mask
# extract_wrong_pix(legolas_path, mask_path, 'outOfV11.mat', output_folder)
#extracting noisyPixels
# extract_wrong_pix(legolas_path, mask_path, 'noisyPixels.mat', output_folder)
