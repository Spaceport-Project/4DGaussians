from ultralytics import YOLO
import cv2
import os

# Load the YOLOv8 model
model = YOLO('yolov8l.pt')

data_dir = "/home/alper/Spaceport/basler_camera_process/output/1-20/original_images"
dst_dir = "/home/alper/Spaceport/basler_camera_process/output/1-20/cropped_images"

xmin_values = list()
xmax_values = list()

os.makedirs(dst_dir, exist_ok=True)
# Perform inference on an image
for cam_folder in sorted(os.listdir(data_dir)):
    # cam00, cam01
    print(f"Processing {cam_folder}\n")
    if os.path.isdir(os.path.join(data_dir, cam_folder)):
        for image_name in sorted(os.listdir(os.path.join(data_dir, cam_folder, 'images'))):
            image_path = os.path.join(data_dir, cam_folder, 'images', image_name)
            results = model(image_path, classes=0)
            
            img = cv2.imread(image_path)

            boxes = results[0].boxes.xyxy.tolist()
            print(len(boxes))
            print(type(boxes))
            if len(boxes) > 1:
                first_bbox = results[0].boxes.xyxy.tolist()[0]
                print("bozes 1 den büyük -> ", boxes)
                boxes = list()
                boxes.append(first_bbox)

            # Iterate through the bounding boxes
            for i, box in enumerate(boxes):
                x1, y1, x2, y2 = box
                xmin_values.append(x1)
                xmax_values.append(x2)
                ultralytics_crop_object = img[int(y1):int(y2), int(x1):int(x2)]
                # Save the cropped object as an image
                # cv2.imwrite(f"{os.path.join(dst_dir, image)}", ultralytics_crop_object)

    print("xmin -> ", min(xmin_values))
    print("xmax -> ", max(xmax_values))

    x1 = int(min(xmin_values))
    x2 = int(max(xmax_values))
    y1 = 0
    y2 = 3000
    
    os.makedirs(os.path.join(dst_dir, cam_folder, 'images'), exist_ok=True)
    
    for image_name in sorted(os.listdir(os.path.join(data_dir, cam_folder, 'images'))):
        print(f"Cropping {cam_folder}\n")
        image_path = os.path.join(data_dir, cam_folder, 'images', image_name)
        img = cv2.imread(image_path)

        ultralytics_crop_object = img[int(y1):int(y2), int(x1):int(x2)]
        dst_image_name = os.path.join(dst_dir, cam_folder, 'images', image_name)
        cv2.imwrite(dst_image_name, ultralytics_crop_object)

    xmin_values = list()
    xmax_values = list()

print("Done")
# for cam_folder in sorted(os.listdir(data_dir)):
#     # cam00, cam01
#     os.makedirs(os.path.join(dst_dir, cam_folder, 'images'), exist_ok=True)
#     print(f"Processing {cam_folder}\n")
#     if os.path.isdir(os.path.join(data_dir, cam_folder)):
#         for image_name in sorted(os.listdir(os.path.join(data_dir, cam_folder, 'images'))):
#             image_path = os.path.join(data_dir, cam_folder, 'images', image_name)
#             img = cv2.imread(image_path)

#             ultralytics_crop_object = img[int(y1):int(y2), int(x1):int(x2)]
#             dst_image_name = os.path.join(dst_dir, cam_folder, 'images', image_name)
#             cv2.imwrite(dst_image_name, ultralytics_crop_object)
