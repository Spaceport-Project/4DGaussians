import torch
import os
import numpy as np
import nvidia_smi
import time
from torch.utils.data import Dataset, DataLoader, Subset


class RandomImageDataset(Dataset):
    def __init__(self, image_list):
        self.image_list = image_list
    
    def __len__(self):
        return len(self.image_list)
    
    def __getitem__(self, idx):
        return self.image_list[idx]

def create_subsets_deterministic(dataset, subset_size):
    subsets = []
    total_size = len(dataset)
    for i in range(0, total_size, subset_size):
        subset_indices = list(range(i, min(i + subset_size, total_size)))
        subsets.append(Subset(dataset, subset_indices))
    return subsets
    
def create_subsets_random(dataset, subset_size):
    subsets = []
    indices = torch.randperm(len(dataset)).tolist()
    for i in range(0, len(dataset), subset_size):
        subset_indices = indices[i:i + subset_size]
        subsets.append(Subset(dataset, subset_indices))
    return subsets

if __name__ == "__main__":
    num_images = 36
    images_list = [np.random.randint(0, 10) for _ in range(num_images)]
    dataset = RandomImageDataset(image_list=images_list)
    subset_size = 10

    print("Original Images list -> ", images_list)
    print("----------------- RANDOM SUBSET GENERATION -----------------")

    subsets = create_subsets_random(dataset, subset_size)

    for i, subset in enumerate(subsets):
        print(f"Subset {i + 1}:")
        print(subset.indices)
        print("subset len ->", len(subset))
        for item in subset:
            print(item)
        print()
    
    print("----------------- DETERMINISTIC SUBSET GENERATION -----------------")
    subsets = create_subsets_deterministic(dataset, subset_size)

    for i, subset in enumerate(subsets):
        print(f"Subset {i + 1}:")
        for item in subset:
            print(item)
        print()