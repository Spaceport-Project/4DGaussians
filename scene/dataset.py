from torch.utils.data import Dataset
from scene.cameras import Camera
import numpy as np
from utils.general_utils import PILtoTorch
from utils.graphics_utils import fov2focal, focal2fov
import torch
from utils.camera_utils import loadCam
from utils.graphics_utils import focal2fov
import gc

class FourDGSdataset(Dataset):
    def __init__(
        self,
        dataset,
        args,
        dataset_type
    ):
        self.dataset = dataset # subset
        self.args = args
        self.dataset_type=dataset_type
    
    def load_to_gpu(self):
        # print("GPU Loading..")
        self.dataset.load_gpu() # call subset function
        
    def unload_gpu(self):
        # print("GPU Offloading..")
        self.dataset.unload_gpu() # call subset function

    def __getitem__(self, index):
        # breakpoint()
        # print("4DGS Dataset index ->", index)
        if self.dataset_type != "PanopticSports":
            try:
                image, w2c, time = self.dataset[index]
                # print("4DGS Dataset getitem image device ->", image.device)
                R,T = w2c
                FovX = focal2fov(self.dataset.focal[0], image.shape[2]) # first dataset represent Subset, second one is Neural3D dataset
                FovY = focal2fov(self.dataset.focal[0], image.shape[1])
                mask=None
            except:
                caminfo = self.dataset[index]
                image = caminfo.image
                R = caminfo.R
                T = caminfo.T
                FovX = caminfo.FovX
                FovY = caminfo.FovY
                time = caminfo.time
    
                mask = caminfo.mask
            return Camera(colmap_id=index,R=R,T=T,FoVx=FovX,FoVy=FovY,image=image,gt_alpha_mask=None,
                              image_name=f"{index}",uid=index,data_device=torch.device("cuda"),time=time,
                              mask=mask)
        else:
            return self.dataset[index]
    
    def __len__(self):    
        return len(self.dataset)
