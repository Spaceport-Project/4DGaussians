import os
import re

import numpy as np
import cv2

# video_name1.mp4, video_name2.mp4 ... frame extraction.

def process_videos(input_folder, output_folder):
    for filename in sorted(os.listdir(input_folder)):
        if filename.endswith(".mp4"):
            video_path = os.path.join(input_folder, filename)
            video_number = extract_number_from_filename(filename)

            if video_number is None:
                raise NotImplementedError("Videos Must Contain Numbers, for instance stream1, stream10, stream23 etc.")
        
            output_subfolder = os.path.join(output_folder, f"cam{int(video_number):02d}")
            print(f"Filename -> {filename} -- Output Folder -> {output_subfolder}")
            extract_frames(video_path, output_subfolder)

def extract_number_from_filename(filename):
    match = re.search(r'\d+', filename)
    if match:
        return match.group()
    return None

def extract_frames(video_path, output_folder):
    vidcap = cv2.VideoCapture(video_path)
    
    os.makedirs(output_folder, exist_ok=True)
    
    total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    for i in range(total_frames):
        success, image = vidcap.read()
        if not success:
            break
        
        frame_path = os.path.join(output_folder, f"{i:04d}.png")
        cv2.imwrite(frame_path, image)
    
    vidcap.release()

if __name__ == "__main__":
    data_dir = "/mnt/Elements2/04-04-2024_Data/test_data/seperate_videos_alper_test" # mp4 and npy pose files
    output_dir = "/home/alper/Spaceport/data/internal_dataset/"
    os.makedirs(output_dir, exist_ok=True)
    process_videos(data_dir, output_dir)