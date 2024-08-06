import gc
import time
from statistics import mean

import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np
import nvidia_smi

class RandomImageDataset(Dataset):
    def __init__(self, num_images=40, image_size=(4080, 2950, 3)):
        self.num_images = num_images
        self.image_size = image_size
        # self.image_list = [torch.rand(image_size) for _ in range(num_images)]
        self.image_list = list()

        for i in range(num_images):
            print("Image index -> ", i)
            image = torch.rand(image_size)
            self.image_list.append(image)
        
    def __len__(self):
        return len(self.image_list)
    
    def __getitem__(self, idx):
        return self.image_list[idx]
    
    def load_to_gpu(self):
        self.image_list = [image.to('cuda') for image in self.image_list]

    def unload_gpu(self):
        self.image_list = [image.to('cpu') for image in self.image_list]
        torch.cuda.empty_cache()
        gc.collect()

def get_gpu_info(msg):
    nvidia_smi.nvmlInit()
    handle = nvidia_smi.nvmlDeviceGetHandleByIndex(0)
    info = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)

    gb_convert = 1024 * 1024
    # print("Total memory:", info.total / gb_convert)
    # print("Free memory:", info.free / gb_convert) 
    print(f"\nMessage is {msg} --- GPU Used memory:", info.used / gb_convert)
    nvidia_smi.nvmlShutdown()

def switch_dataset(dataset):
    
    st = time.time()
    get_gpu_info(msg="Start")
    dataset.load_to_gpu()
    get_gpu_info(msg="first dataset moving to dataset")
    first_dataloader = DataLoader(dataset, batch_size=1)

    # process

    dataset.unload_gpu()
    get_gpu_info(msg="Unloaded GPU")
    first_dataloader = DataLoader(dataset, batch_size=1)
    
    consumed_time = time.time() - st
    print("Consumed Time -> \n", consumed_time)
    return consumed_time

def main(dataset_list, num_images):
    time_list = list()
    while 1: 
        try:
            dataset = next(dataset_list)
            consumed_time = switch_dataset(dataset=dataset)
            time_list.append(consumed_time)
        except StopIteration:
            break

    print(f"Time list mean -> {mean(time_list)} --- images number -> {num_images}")

if __name__ == "__main__":
    instance_list = list()
    num_instances = 5
    num_images = 69

    for _ in range(num_instances):
        dataset = RandomImageDataset(num_images=num_images)
        instance_list.append(dataset)

    dataset_list = iter(instance_list) # list iterator
    main(dataset_list, num_images)

    