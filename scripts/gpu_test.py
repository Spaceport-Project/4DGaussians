import os
import torch
import numpy as np
import nvidia_smi
import time

test = list()
nvidia_smi.nvmlInit()

for i in range(50):
    data = torch.randn(1, 3, 1920, 1080)
    data = data.to('cuda')
    handle = nvidia_smi.nvmlDeviceGetHandleByIndex(0)
    info = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)

    gb_convertion = (1024 * 1024)
    print("Device {}: {}, Memory : ({:.2f}% free): {}(total GB), {} (free GB), {} (used GB)".format(i, nvidia_smi.nvmlDeviceGetName(handle), 100*info.free/info.total, info.total / gb_convertion, info.free / gb_convertion, info.used / gb_convertion))
    test.append(data)
    print(len(test))



nvidia_smi.nvmlShutdown()
