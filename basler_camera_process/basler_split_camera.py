import itertools
import os
import shutil
import cv2

data_dir = "/mnt/Elements2/15-07-2024_Basler_DATA/test_images_oguz_3/"
base_dir = "output"
interval = 6
cam_num = 24

def copy_first_frame(source_dir):
    # Hedef dizini oluştur
    print("First Frames Copying for COLMAP..")
    target_dir = os.path.join(source_dir, "colmap_input")
    os.makedirs(target_dir, exist_ok=True)
    
    # Kaynak dizinindeki ilk tiff dosyasını bul
    for index, cam_folder in enumerate(os.listdir(os.path.join(source_dir, 'original_images'))):
        first_tiff_file = os.path.join(source_dir, 'original_images', cam_folder, 'images', f"0000.png")
        target_img = os.path.join(target_dir, f"{index:04d}.png")
    
        # Eğer dosya varsa, first_frames dizinine kopyala
        if os.path.exists(first_tiff_file):
            shutil.copy(first_tiff_file, target_img)
        else:
            print(f"0000.png dosyası bulunamadı: {first_tiff_file}")

def rename_images_in_directory(base_dir):
    print("Renaming..")
    cam_dirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

    for cam_dir in cam_dirs:
        images_dir = os.path.join(base_dir, cam_dir, 'images')
        
        if os.path.exists(images_dir):
            images = sorted(os.listdir(images_dir))  # Dosyaları sıralı olarak al
            
            for i, image in enumerate(images):
                old_image_path = os.path.join(images_dir, image)
                new_image_name = f"{i:04d}.png"
                new_image_path = os.path.join(images_dir, new_image_name)
                
                os.rename(old_image_path, new_image_path)

def create_directory_structure(base_dir, interval, cam_num):
    start_interval_list = list()

    for i in range(cam_num):
        start = i * interval + 1
        end = (i + 1) * interval
        folder_name = f"{start}-{end}"  # 1-20, 21-40, ...
        folder_path = os.path.join(base_dir, folder_name)
        
        for cam_id in range(cam_num):
            cam_folder_name = f"cam{cam_id:02d}"
            cam_folder_path = os.path.join(folder_path, 'original_images', cam_folder_name, 'images')
            os.makedirs(cam_folder_path, exist_ok=True)
        # print("fname ", cam_folder_path)
        start_interval_list.append(f"{start}-{end}")
    return start_interval_list

start_intervals = create_directory_structure(base_dir, interval, cam_num)
start_intervals = itertools.chain(start_intervals)

image_list = os.listdir(data_dir)

timestamps = list()
for item in image_list:
    timestamps.append(item.split("_")[1])

timestamps = sorted(set(timestamps)) # get unique timestamps
output_list = list()

for ts in timestamps:
    dummy = list()
    dummy = [image for image in image_list if ts in image]
    output_list.append(dummy)

counter = 0
output_interval = next(start_intervals)

for index, sequence in enumerate(output_list):
    if counter == interval:
        rename_dir = os.path.join(base_dir, output_interval, 'original_images')
        rename_images_in_directory(rename_dir)
        copy_first_frame(os.path.join(base_dir, output_interval))
        output_interval = next(start_intervals)
        counter = 0
        
    for image in sequence:
        parts = image.split('_')
        camera_id = int(parts[2].split('.')[0])
        
        source_image_path = os.path.join(data_dir, image)
        dst_image_path = os.path.join(os.path.join(os.path.join(base_dir, output_interval)), f"original_images/cam{camera_id:02d}/images/{image}")
        print(f"{source_image_path} to {dst_image_path}")
        img = cv2.imread(source_image_path)
        denoised_image = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 20)
        cv2.imwrite(f"{dst_image_path.split('.')[0]}.png", denoised_image, [cv2.IMWRITE_PNG_COMPRESSION, 1])

        # shutil.copy(source_image_path, dst_image_path)
    
    print(f"Working on {output_interval} interval")
    counter += 1