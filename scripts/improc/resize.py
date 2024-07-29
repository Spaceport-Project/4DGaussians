import os
import cv2

def norm(head_data_dir):
    for cam_folder in sorted(os.listdir(head_data_dir)):
        # cam00, cam01
        print(f"Processing {cam_folder}\n")
        if os.path.isdir(os.path.join(head_data_dir, cam_folder)):
            for image_name in sorted(os.listdir(os.path.join(head_data_dir, cam_folder, 'images'))):
                image_path = os.path.join(head_data_dir, cam_folder, 'images', image_name)
                original_image = cv2.imread(image_path)

                resized = cv2.resize(original_image, (0, 0), fx=0.9, fy=0.9, interpolation=cv2.INTER_LANCZOS4)

                cv2.imwrite(image_path, resized)
                print(f"\n{image_path}, Written.. ")

if __name__ == "__main__":
    # ------------ For masked (image with alpha channel) Uncomment Above Comments ------------ 
    head_data_dir = "/home/alper/Spaceport/data/20_interval_resized_test/100-119/masked_undistorted_images" # includes cam00, cam01 etc.
    norm(head_data_dir)