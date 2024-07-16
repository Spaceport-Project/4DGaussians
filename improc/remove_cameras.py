import os
import numpy as np
import json

def remove_cams():
    

    for item in os.listdir(images_dir):

        image_full_name = item.split(".")[0].split("/")[-1]
        camera_name = image_full_name.split("_")[2]

        if camera_name in removing_cameras_list:
            os.remove(os.path.join(images_dir, item))



if __name__ == "__main__":

    f = open('removing_cameras.json') # cameras that will be REMOVED
    data = json.load(f)
    removing_cameras_list = list()
    for i in data['remove_camera']:
        removing_cameras_list.append(i)
        
    images_dir = "/home/alper/Spaceport/data/internal_dataset/less_cameras_dataset"

    print("Data count Before pruning -> ", len(os.listdir(images_dir)))
    print("Data count After pruning -> ", len(os.listdir(images_dir)))
    print(f"{len(removing_cameras_list)} Camera removed..")
    remove_cams()