import os
import cv2
import time

# video names -> video_rgb_4000x2000_0.mp4, video_rgb_4000x2000_1.mp4, video_rgb_4000x2000_2.mp4 ...

# angle 0 -> last index is 0, 10, 20, 30
# angle 1 -> last index is 1, 11, 21, 31
# angle 2 -> last index is 2, 12, 22, 32
# angle 3 -> last index is 3, 13, 23, 33 
# ...

head_dir = "/home/alper/Spaceport/improc/0-19/"
dist_dir = "/home/alper/Spaceport/improc/frames/"

st = time.time()

for video_name in os.listdir(head_dir):
    if (video_name.split(".")[-1] == "mp4") and (video_name.split("_")[2] == "4000x2000"):
        print("Processing -> ", video_name)
        last_index = int((video_name.split(".")[0]).split("_")[-1]) # 0, 1, 2, 3, 4 as integer
        angle = last_index % 10
        print(f"{last_index} ID is belongs to angle {angle}")

        dist_dir_with_angle = os.path.join(dist_dir, f"angle_{angle}")
        os.makedirs(dist_dir_with_angle, exist_ok=True)
        
        video_path = os.path.join(head_dir, video_name)
        cap = cv2.VideoCapture(video_path)

        while True:
            ret, frame = cap.read()

            if not ret:
                break
            
            naming_index = len(os.listdir(dist_dir_with_angle))
            
            frame_filename = os.path.join(dist_dir_with_angle, f"{video_name.split('.')[0]}_{naming_index}.png")
            cv2.imwrite(frame_filename, frame)
            
            # print(f"{frame_filename} extracting from {video_path} with {naming_index} index..")

print(f"Done in {time.time() - st} Seconds.")