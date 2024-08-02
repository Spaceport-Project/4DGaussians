import math

library_inits = 850 # mb
per_img = 138 # mb
train_model = 8000 # 6000-8000 MB (min max)
eval_model = 8500 # 7.500-8.500 MB (min max)

gpu_vram = 24500 # RTX 3090
interval = 4
camera_number = 24

train_diff = gpu_vram - (library_inits + (per_img * (interval * camera_number)) + train_model)
eval_diff = gpu_vram - (library_inits + (per_img * (interval * camera_number)) + eval_model)

print(f"Train Diff -> {train_diff} -- Eval Diff -> {eval_diff}")

if train_diff > 0:
    print(f"Congrats Train is Available, Interval fit into GPU with {train_diff} difference")
else:
    print(f"Train Failed, difference is {train_diff}. Try lower Interval")

if eval_diff > 0:
    print(f"Congrats Eval is available, Interval fit into GPU with {train_diff} difference")
else:
    print(f"Eval Failed, diffrence is {train_diff}. Try lower Interval")
    

