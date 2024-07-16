import argparse
from collections import defaultdict
import json
import os
import shutil
from pathlib import Path
import cv2


def histogram_equalization(image):
    # Görüntüyü YUV renk uzayına çevirme
    yuv_image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    # Y kanalında histogram eşitleme
    yuv_image[:, :, 0] = cv2.equalizeHist(yuv_image[:, :, 0])
    # Görüntüyü tekrar BGR formatına çevirme
    equalized_image = cv2.cvtColor(yuv_image, cv2.COLOR_YUV2BGR)
    return equalized_image


# Setup argparse for command line arguments
parser = argparse.ArgumentParser(description="Organize and process image dataset")
parser.add_argument("data_dir", help="Directory containing the image dataset")
parser.add_argument("output_dir", help="Directory to store the organized dataset")
parser.add_argument("img_ext", default=".png", help="Image extension to use for the dataset")
parser.add_argument("num_cameras", type=int, help="Number of cameras in the dataset")
parser.add_argument("starting_frame_idx", type=int, help="Starting frame index (leave blank for no limit)")
parser.add_argument("ending_frame_idx", type=int, help="Ending frame index (leave blank for no limit)")
args = parser.parse_args()

DATA_DIR = args.data_dir
OUTPUT_DIR = args.output_dir
img_ext = args.img_ext
num_cameras = args.num_cameras
starting_frame_idx = args.starting_frame_idx
ending_frame_idx = args.ending_frame_idx

orig_img_path = os.path.join(OUTPUT_DIR, str(starting_frame_idx)+'-'+str(ending_frame_idx), 'original_images')
# Check if orig_img_path exists, else create
if not os.path.exists(orig_img_path):
    os.makedirs(orig_img_path)

# Convert input indices to integers if provided
starting_frame_idx = int(starting_frame_idx) 
ending_frame_idx = int(ending_frame_idx) 

serial_to_cam = {}
frame_to_images = defaultdict(list)

# First, gather all images per frame to count them
for filename in sorted(os.listdir(DATA_DIR)):
    parts = filename.split('_')
    if len(parts) < 3:
        continue  # Skip files that don't match the expected naming scheme

    frame_idx = int(parts[1])
    serial = parts[2]

    # If starting and ending indices are set, skip frames outside the range
    if starting_frame_idx is not None and frame_idx < starting_frame_idx:
        continue
    if ending_frame_idx is not None and frame_idx > ending_frame_idx:
        continue

    frame_to_images[frame_idx].append(filename)

# Create a frame counter for each camera
frame_counters = defaultdict(int)

# Process only the frames where the image count matches the camera count
for frame_idx in sorted(frame_to_images.keys()):
    images = frame_to_images[frame_idx]
    if len(images) == num_cameras:
        for filename in images:
            parts = filename.split('_')
            serial = parts[2]

            if serial not in serial_to_cam:
                cam_id = f"cam{len(serial_to_cam):02}"
                serial_to_cam[serial] = cam_id

                # Create necessary directories for new cam
                os.makedirs(os.path.join(orig_img_path, cam_id, "images"), exist_ok=True)

            cam_id = serial_to_cam[serial]

            # Define the source and destination paths
            src_path = os.path.join(DATA_DIR, filename)
            dest_filename = f"{frame_counters[cam_id]:04}" + img_ext
            dest_path = os.path.join(orig_img_path, cam_id, "images", dest_filename)

            # Increment the frame counter for this camera
            frame_counters[cam_id] += 1

            # Copy the image to the new location
            shutil.copy2(src_path, dest_path)

# Save mappings to JSON file
with open(os.path.join(orig_img_path, "mappings.json"), "w") as json_file:
    json.dump({
        "serial_to_cam": serial_to_cam,
    }, json_file, indent=4)

print("Dataset organized and mappings saved to ",orig_img_path)

# Also get the frist frames of each camera to another folder
colmap_input_path = os.path.join(Path(orig_img_path).parent,'colmap_input')
print('colmap_input_path: ', colmap_input_path)

# Check if colmap_input_path exists, else create
if not os.path.exists(colmap_input_path):
    os.makedirs(colmap_input_path)

colmap_input_imgs = []
# First, gather all images per frame to count them
for filename in sorted(os.listdir(DATA_DIR)):
    parts = filename.split('_')
    if len(parts) < 3:
        continue  # Skip files that don't match the expected naming scheme

    frame_idx = int(parts[1])
    serial = parts[2]

    # If starting and ending indices are set, skip frames outside the range
    if frame_idx == starting_frame_idx:
        colmap_input_imgs.append(filename)

# Now copy the first frames of each camera to colmap_input_path
for filename in colmap_input_imgs:
    print("filename -> ", filename)
    print("src_path -> ", src_path)
    print("dest_path -> ", dest_path)

    src_path = os.path.join(DATA_DIR, filename)
    dest_path = os.path.join(colmap_input_path, filename)
    
    ## 
    # img = cv2.imread(src_path)
    # img = histogram_equalization(img) # Histogram Eq for colmap Input that generates poses_bounds.npy
    # cv2.imwrite(dest_path, img)
    ##
    shutil.copy2(src_path, dest_path)


