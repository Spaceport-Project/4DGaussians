import os
import cv2

def get_size(path):
    img_size = os.path.getsize(path)
    print(f"{path} size is {img_size / (1024 * 1024)} MB")

def norm(head_data_dir):
    for cam_folder in sorted(os.listdir(head_data_dir)):
        # cam00, cam01
        print(f"Processing {cam_folder}\n")
        if os.path.isdir(os.path.join(head_data_dir, cam_folder)):
            for image_name in sorted(os.listdir(os.path.join(head_data_dir, cam_folder, 'images'))):
                image_path = os.path.join(head_data_dir, cam_folder, 'images', image_name)
                get_size(image_path)
                original_image = cv2.imread(image_path)

                # Alpha Channel Processes
                # original_image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
                # alpha_channel = original_image[:,:,3]
                # original_image = cv2.cvtColor(original_image, cv2.COLOR_BGRA2BGR)

                denoised_image = cv2.fastNlMeansDenoisingColored(original_image, None, 10, 10, 7, 20)
                # denoised_image = cv2.cvtColor(denoised_image, cv2.COLOR_BGR2BGRA)
                # denoised_image[:, :, 3] = alpha_channel
                
                cv2.imwrite(image_path, denoised_image)
                get_size(image_path)
                print(f"\n{image_path}, Written.. ")

if __name__ == "__main__":
    # ------------ For masked (image with alpha channel) Uncomment Above Comments ------------ 
    head_data_dir = "/home/alper/Spaceport/data/20_interval_bash_output/34-53/masked_undistorted_images" # includes cam00, cam01 etc.
    norm(head_data_dir)