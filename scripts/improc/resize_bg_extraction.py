import os
import cv2
from PIL import Image
import numpy as np

def main(head_data_dir):
    for cam_folder in sorted(os.listdir(head_data_dir)):
        # cam00, cam01
        print(f"Processing {cam_folder}\n")
        if os.path.isdir(os.path.join(head_data_dir, cam_folder)):
            for image_name in sorted(os.listdir(os.path.join(head_data_dir, cam_folder, 'images'))):
                image_path = os.path.join(head_data_dir, cam_folder, 'images', image_name)
                original_image = cv2.imread(image_path)

                resized = cv2.resize(original_image, (0, 0), fx=0.9, fy=0.9, interpolation=cv2.INTER_LANCZOS4)
                im_data = cv2.cvtColor(resized, cv2.COLOR_BGR2RGBA)
                # img = Image.open(image_path)
                # im_data = np.array(img.convert("RGBA"))
                bg = np.array([1,1,1])
                norm_data = im_data / 255.0
                arr = norm_data[:,:,:3] * norm_data[:, :, 3:4] + bg * (1 - norm_data[:, :, 3:4])
                img = Image.fromarray(np.array(arr*255.0, dtype=np.byte), "RGB")
                
                img.save(image_path)

                cv2.imwrite(image_path, resized)
                print(f"\n{image_path}, Written.. ")

if __name__ == "__main__":
    # ------------ For masked (image with alpha channel) Uncomment Above Comments ------------ 
    head_data_dir = "/home/alper/Spaceport/data/20_interval_resized_test/100-119/masked_undistorted_images" # includes cam00, cam01 etc.
    main(head_data_dir)