import os

import torch
import numpy as np 
import cv2
from PIL import Image

def post_proc(head_data_dir):
    for cam_folder in sorted(os.listdir(head_data_dir)):
        if os.path.isdir(os.path.join(head_data_dir, cam_folder)):
            print(f"Processing {cam_folder}\n")
            for image_name in sorted(os.listdir(os.path.join(head_data_dir, cam_folder, 'images'))):
                image_path = os.path.join(head_data_dir, cam_folder, 'images', image_name)

                img = Image.open(image_path)
                im_data = np.array(img.convert("RGBA"))
                bg = np.array([1,1,1])
                norm_data = im_data / 255.0
                arr = norm_data[:,:,:3] * norm_data[:, :, 3:4] + bg * (1 - norm_data[:, :, 3:4])
                img = Image.fromarray(np.array(arr*255.0, dtype=np.byte), "RGB")
                
                img.save(image_path)
                print(f"{image_path} saved and ready to be trained.")

if __name__ == "__main__":
    head_data_dir = "/home/alper/Spaceport/data/20_interval_resized_test_2200_1600_shape_full/140-159/masked_undistorted_images" # cam00, cam01
    post_proc(head_data_dir)