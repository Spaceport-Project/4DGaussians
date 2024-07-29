import sys
import time
import os

from yolox_mask_generation import image_inference, Predictor
import subprocess

sys.path.append('/home/alper/Spaceport/data_process/segment-anything')
sys.path.append('/home/alper/Spaceport/data_process/YOLOX/yolox')
sys.path.append('/home/alper/Spaceport/data_process/YOLOX/')

def prep_command(img_path, bg_img, erode_kernel, erode_iteration, output_path):
    command = ["python", 
           "yolox_mask_generation.py", 
           "images", 
           "-n", 
           "yolox-x",
           "-c",  
           "/home/alper/Spaceport/data_process/YOLOX/model_weights/yolox_x.pth",
           "--sam_checkpoint",
           "/home/alper/Spaceport/data_process/segment-anything/model_weights/sam_vit_h_4b8939.pth",
           "--sam_model_type",
           "vit_h",
           "--path", 
           f"{img_path}",
           "--bg_path",
           f"{bg_img}",
           "--erode_kernel_size",
           f"{erode_kernel}",
           "--erode_iteration",
           f"{erode_iteration}",
           "--output_path",
           f"{output_path}",
           "--conf",
           "0.25",
           "--nms",
           "0.45",
           "--tsize",
           "640",
           "--save_result",
           "--device",
           "gpu"]
    
    return command

if __name__ == "__main__":
    render_output_images_path = "/home/alper/Spaceport/render_process/render_images" # directory with ONLY images for blending from render section
    bg_image = "/home/alper/Spaceport/render_process/background_8.png" # single image
    erode_kernel_size = 5 # default
    erode_iteration = 5 # default
    output_path = "/home/alper/Spaceport/render_process/processed_render_images" # blending image outputs path

    os.makedirs(output_path, exist_ok=True)
        
    command = prep_command(img_path=render_output_images_path, 
                               bg_img=bg_image, 
                               erode_kernel=erode_kernel_size, 
                               erode_iteration=erode_iteration,
                               output_path=output_path)

    subprocess.run(command)




