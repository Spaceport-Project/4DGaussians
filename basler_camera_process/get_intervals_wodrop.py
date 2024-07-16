"""This script takes a directory containing images and outputs the intervals as list of list where there are no frame drops."""

import argparse
from collections import defaultdict
import json
import os
import shutil
from pathlib import Path

# Setup argparse for command line arguments
parser = argparse.ArgumentParser(description="Organize and process image dataset")
parser.add_argument("data_dir", help="Directory containing the image dataset")
parser.add_argument("output_dir", help="Directory to store the organized dataset")
parser.add_argument("img_ext", default=".png", help="Image extension to use for the dataset")
parser.add_argument("num_cameras", type=int, help="Number of cameras in the dataset")
parser.add_argument("frames_count", help="Frames count in a interval")
args = parser.parse_args()

frames_count= int(args.frames_count)
DATA_DIR = args.data_dir
OUTPUT_DIR = args.output_dir
img_ext = args.img_ext
num_cameras = args.num_cameras

filenames = os.listdir(DATA_DIR)
# Extracting time indexes from filenames and counting the number of images per time index
image_count_per_time_index = defaultdict(int)
for filename in filenames:
    time_index = int(filename.split('_')[1])
    image_count_per_time_index[time_index] += 1

# Finding intervals with exactly num_cameras images per time index
intervals_with_25_images = []
current_interval = []
for time_index in sorted(image_count_per_time_index.keys()):
    if image_count_per_time_index[time_index] == num_cameras:
        if not current_interval:
            current_interval = [time_index, time_index]
        else:
            if time_index == current_interval[1] + 1:
                current_interval[1] = time_index
            else:
                intervals_with_25_images.append(current_interval)
                current_interval = [time_index, time_index]
    else:
        if current_interval:
            intervals_with_25_images.append(current_interval)
            current_interval = []

# Adding the last interval if it exists
if current_interval:
    intervals_with_25_images.append(current_interval)

# print("Intervals without frame drop: ", intervals_with_25_images)

intervals_with_approx_20_images = []  # This will store the final intervals
for interval in intervals_with_25_images:
    start, end = interval
    while start <= end:
        remaining_frames = end - start + 1
        # Check if the remaining frames fit within the desired range directly
        if frames_count -5 <= remaining_frames <= frames_count+5:
            intervals_with_approx_20_images.append([start, end])
            break  # This interval is now fully processed
        elif remaining_frames > frames_count:
            # If more than 23 frames, create an interval that fits as close to 20 as possible
            intervals_with_approx_20_images.append([start, start + frames_count -1 ])
            start += frames_count  # Move to the next segment within this interval
        else:
            # If fewer than 13 frames remain, decide based on your criteria. For now, it's skipped.
            break

# Output the refined intervals
# print (json.dumps([[1, 20], [21, 40] ]))
#[141, 160] , [761, 780], [881, 900]
# print (json.dumps([[381, 400]]))
# print (json.dumps([[381, 400], [401, 420], [421, 440], [441, 460], [461, 480], [481, 500], [501, 520], [521, 540], [541, 560], [561, 580], [581, 600], [601, 620], [621, 640], [641, 660], [661, 680], [681, 700], [701, 720], [721, 740], [741, 760], [761, 780], [781, 800], [801, 820], [821, 840], [841, 860], [861, 880], [881, 900], [901, 920], [921, 940], [941, 960], [961, 980], [981, 1000]]))

print(json.dumps(intervals_with_approx_20_images))

