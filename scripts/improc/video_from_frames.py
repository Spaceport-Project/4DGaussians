import cv2
import os

frames_dir = 'frames'

output_video_path = 'output_video.mp4'

frame_files = sorted([f for f in os.listdir(frames_dir) if f.endswith('.jpg') or f.endswith('.png')])

frame = cv2.imread(os.path.join(frames_dir, frame_files[0]))
height, width, layers = frame.shape

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(output_video_path, fourcc, 30.0, (width, height))

for frame_file in frame_files:
    frame = cv2.imread(os.path.join(frames_dir, frame_file))
    video_writer.write(frame)

video_writer.release()