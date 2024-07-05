import os
import shutil

def organize_frames(source_path, target_path, interval):
    # Klasörler listesi
    folders = [f for f in os.listdir(source_path) if os.path.isdir(os.path.join(source_path, f))]

    for folder in folders:
        folder_path = os.path.join(source_path, folder)
        frames = sorted(os.listdir(folder_path))
        
        for i in range(0, len(frames), interval):
            interval_folder_name = f"interval{i}-{i+interval-1}"
            interval_folder_path = os.path.join(target_path, interval_folder_name, folder, "images")

            os.makedirs(interval_folder_path, exist_ok=True)

            for j, frame in enumerate(frames[i:i+interval]):
                frame_source_path = os.path.join(folder_path, frame)
                frame_target_path = os.path.join(interval_folder_path, f"{j:04d}.png")

                shutil.copy2(frame_source_path, frame_target_path)

source_path = '/home/alper/Spaceport/data/internal_dataset/test/'
target_path = '/home/alper/Spaceport/data/internal_dataset/test/processed/'
interval = 20

organize_frames(source_path, target_path, interval)
