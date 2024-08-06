import os
import subprocess
import time

import torch

def start_seq_trains(dataset_dir):
    data_paths = list()
    experiment_names = list()

    for interval_folder in sorted(os.listdir(dataset_dir)):
        # 0-19, 20-39 ...
        data_path = os.path.join(dataset_dir, interval_folder, "masked_undistorted_images") # example -> /home/alper/Spaceport/data/20_interval_resized_test_2200_1600_shape_full/20-39/masked_undistorted_images
        data_paths.append(data_path)
        experiment_names.append(f"{interval_folder}_train")


    for data_path, expname in zip(data_paths, experiment_names):
        start_time = time.time()
        command = ["python", "train.py", "-s", data_path, "--expname", expname]
        print(f"Running command: {' '.join(command)}")
        print(f"Training Starting on {data_path} with name {expname}")
        subprocess.run(command)
        print(f"Training End on {data_path} with name {expname}")
        print("Consumed Time -> ", time.time() - start_time)
        
        try:
            torch.cuda.empty_cache()
        except:
            print("Cuda Empty Cache Fails..")

if __name__ == "__main__":
    dataset_dir = "/home/alper/Spaceport/data/fırat_process_datalar" # includes intervals, 0-19, 20-39 etc.
    start_seq_trains(dataset_dir=dataset_dir)
