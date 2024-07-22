#!/bin/bash

# Usage: bash get_training_data.sh <conda_env_nerf> <conda_env_llff> <input_dir> <output_dir> <llff_path> <image_extension> <camera_number> <masking_method> <bbox_json_dir> <segmentation_script_dir>

# Check if the correct number of arguments are provided
if [ "$#" -ne 10 ]; then
    echo "Usage: $0 <conda_env_nerf> <conda_env_llff> <input_dir> <output_dir> <llff_path> <image_extension> <camera_number> <frames_count> <masking_method> <bbox_json_dir>" 
    exit 1
fi

eval "$(conda shell.bash hook)"

# Activate the 'nerfspaceport' conda environment
conda init bash
conda activate "$1"

# python basler_split_camera.py
# bash basler_type_get_data.sh  nerfstudio LLFF dummy_input_dir /home/alper/Spaceport/basler_camera_process/output/101-120/  /home/alper/Spaceport/data_process/LLFF/ .png 24 20 sam none
# Set input and output directories
input_dir="$3"
output_dir="$4"
llff_path="$5"
image_extension="$6"
camera_number="$7"
frames_count="$8"
masking_method="$9"
bbox_json_dir="${10}"

# Store the current working directory
previous_dir=$(pwd)

conda activate "$1"

# # Run Colmap to get transforms.json file

colmap_input_dir="$output_dir/colmap_input" # output_dir = /home/alper/data/101-120/
colmap_output_dir="$output_dir/colmap_output"

# Replace 'your_matching_method' with your desired method
matching_method="exhaustive"
ns-process-data images --data "$colmap_input_dir" --matching_method "$matching_method" --output_dir "$colmap_output_dir"
echo "$colmap_input_dir"    

# Undistort images for LLFF img2poses.py input to get poses_bounds.npy
undistorted_input_dir="$colmap_output_dir"
undistorted_output_dir="$output_dir/undistorted_LLFF_input"
python undistort_images.py "$undistorted_input_dir" "$undistorted_output_dir" --img_ext "$image_extension"
echo "Undistorted images for LLFF input are located at: $undistorted_output_dir"

nested_undistorted_input_dir="$output_dir/original_images"
nested_undistorted_output_dir="$output_dir/undistorted_images"
json_file="$colmap_output_dir/transforms.json"
python undistort_images_nested.py "$nested_undistorted_input_dir" "$nested_undistorted_output_dir" "$json_file" --img_ext "$image_extension"
echo "Undistorted all images to: $nested_undistorted_output_dir"

# # Deactivate the 'nerfspaceport' conda environment
conda deactivate

# # Activate the 'LLFF' conda environment
conda activate "$2"

# Run imgs2poses.py
cd "$llff_path"
imgs2poses_input_dir="$undistorted_output_dir"
python imgs2poses.py "$imgs2poses_input_dir"

poses_bounds_path=$"$output_dir/undistorted_LLFF_input/poses_bounds.npy"

echo "Poses bounds file is located at: $poses_bounds_path"
# Return to the previous working directory
cd "$previous_dir"
conda deactivate

conda activate "$1"
# Copy the poses_bounds.npy file to the nested undistorted images directory
cp "$poses_bounds_path" "$nested_undistorted_output_dir/poses_bounds.npy"

# According to the masking method, apply the corresponding masking
if [ "$masking_method" == "color" ]; then
    # Apply HSV color masking
    hsv_masked_imgs_dir="$output_dir/masked_undistorted_images_hsv"
    python color_filter_imgs.py "$nested_undistorted_output_dir" "$hsv_masked_imgs_dir" "$bbox_json_dir"
elif [ "$masking_method" == "sam" ]; then
    # Apply segment anything masking
    hsv_masked_imgs_dir="$output_dir/masked_undistorted_images"
    # segmentation_dir="/home/faruk/Softwares/repos/cloned_repos"
    # cd "$segmentation_dir"
    
    echo $nested_undistorted_output_dir
    python generate_masked_data.py images \
        -n yolox-x \
        -c  /home/alper/Spaceport/data_process/YOLOX/model_weights/yolox_x.pth \
        --sam_checkpoint /home/alper/Spaceport/data_process/segment-anything/model_weights/sam_vit_h_4b8939.pth  \
        --sam_model_type vit_h \
        --path "$nested_undistorted_output_dir" \
        --conf 0.25 \
        --nms 0.45 \
        --tsize 640 \
        --save_result \
        --device gpu
else
    echo "Invalid masking method. Please choose either 'bbox' or 'hsv'."
    exit 1
fi

hsv_masked_imgs_dir="$output_dir/masked_undistorted_images" # Seperate segmentation için eklendi. 

cd "$previous_dir"
cp "$poses_bounds_path" "$hsv_masked_imgs_dir/poses_bounds.npy"
# Copy the first frame of each camera from masked undsitorted images to a new directory

filtered_first_frames="$output_dir/filtered_first_frames/images_in"
mkdir -p "$filtered_first_frames"

echo "Start copying first frames"
python copy_first_frames.py "$hsv_masked_imgs_dir" "$filtered_first_frames" "$image_extension" "$camera_number"

echo "First frames copied and renamed successfully."

colmap_run_output_dir="$output_dir/filtered_first_frames/colmap_out"
# Run colmap to ge points3D.bin
ns-process-data images --data "$filtered_first_frames" --output_dir "$colmap_run_output_dir"

cp "$colmap_run_output_dir/colmap/sparse/0/points3D.bin" "$hsv_masked_imgs_dir/points3D.bin"

echo "Processing complete."


