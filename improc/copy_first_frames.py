"""This script copies the first frame of each camera to a new directory"""

import os
import shutil
import argparse
from PIL import Image
import numpy as np


# Setup argparse for command line arguments
parser = argparse.ArgumentParser(description="Copy first frames of each camera")
parser.add_argument("data_dir", help="Directory containing the image dataset")
parser.add_argument("output_dir", help="Directory to store the first frames")
parser.add_argument("img_ext", default=".png", help="Image extension to use for the dataset")
parser.add_argument("num_cameras", type=int, help="Number of cameras in the dataset")
args = parser.parse_args()

DATA_DIR = args.data_dir
OUTPUT_DIR = args.output_dir
img_ext = args.img_ext
num_cameras = args.num_cameras

# Create the output directory if it doesn't exist
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Copy the first frame of each camera to the output directory
for i in range(0,num_cameras):
    src_file = os.path.join(DATA_DIR, f"cam{str(i).zfill(2)}", "images", f"0000{img_ext}")
    # img = Image.open(src_file)
    # im_data = np.array(img.convert("RGBA"))
    # bg = np.array([1,1,1])
    # norm_data = im_data / 255.0
    # arr = norm_data[:,:,:3] * norm_data[:, :, 3:4] + bg * (1 - norm_data[:, :, 3:4])
    # img = Image.fromarray(np.array(arr*255.0, dtype=np.byte), "RGB")
    # img.save(src_file)
    dst_file = os.path.join(OUTPUT_DIR, f"cam{str(i).zfill(2)}{img_ext}")
    print(f"Copying {src_file} to {dst_file}")
    shutil.copyfile(src_file, dst_file)
print("Done copying first frames!")