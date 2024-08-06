import os

import cv2

video_path = 'video.mp4'

output_dir = 'frames'
os.makedirs(output_dir, exist_ok=True)

cap = cv2.VideoCapture(video_path)

frame_count = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame_filename = os.path.join(output_dir, f'frame_{frame_count:04d}.png')
    cv2.imwrite(frame_filename, frame)
    
    frame_count += 1

cap.release()

print(f'{frame_count} kare çıkarıldı ve {output_dir} dizinine kaydedildi.')