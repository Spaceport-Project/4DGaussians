import torch
import os
import numpy as np
import nvidia_smi
import time
from torch.utils.data import Dataset, DataLoader

class RandomImageDataset(Dataset):
    def __init__(self, image_list):
        self.image_list = image_list
        
    def __len__(self):
        return len(self.image_list)
    
    def __getitem__(self, idx):
        return self.image_list[idx]
    
def split_list(lst, n):
    return [lst[i:i + n] for i in range(0, len(lst), n)]

if __name__ == "__main__":
    instance_list = list()
    num_images = 36
    st = time.time()
    images_list = [np.random.randint(0, 10) for _ in range(num_images)]

    result = split_list(images_list, 5)
    print(images_list)
    print(len(result))

    for images in result:
        print(images)
        dataset = RandomImageDataset(image_list=images)
        instance_list.append(dataset)