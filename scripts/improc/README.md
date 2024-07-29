## Grouping angle based images from videos which names video_rgb_4000x2000_0.mp4, video_rgb_4000x2000_1.mp4, video_rgb_4000x2000_2.mp4 etc.

There is a 4 180 degree lines with 10 cameras on every line from 0 to 9 index.

Generating images follows the rules angle,
angle 0 -> last index is 0, 10, 20, 30
angle 1 -> last index is 1, 11, 21, 31
angle 2 -> last index is 2, 12, 22, 32
angle 3 -> last index is 3, 13, 23, 33


On command python `angle_hierarchly_prep.py`, you need to prepare the `head_dir` varible as has videos (names as top) inside it.


---

Resize, bg_extraction and resize_bg_extraction runs on dir that has cam00, cam01, cam02 folders that includes images and image files as DyNerf dataset architecture.
