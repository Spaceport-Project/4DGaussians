#!/bin/bash

# Usage: bash get_training_data.sh <conda_env_nerf> <conda_env_llff> <input_dir> <output_dir> <llff_path> <image_extension> <camera_number> <masking_method> <bbox_json_dir> <segmentation_script_dir>

# Check if the correct number of arguments are provided
if [ "$#" -ne 10 ]; then
    echo "Usage: $0 <conda_env_nerf> <conda_env_llff> <input_dir> <output_dir> <llff_path> <image_extension> <camera_number> <frames_count> <masking_method> <bbox_json_dir> " 
    exit 1
fi

eval "$(conda shell.bash hook)"

# Activate the 'nerfspaceport' conda environment
conda init bash
conda activate "$1"

# Set input and output directories
input_dir="$3"
output_dir="$4"
llff_path="$5"
image_extension="$6"
camera_number="$7"
frames_count="$8"
masking_method="$9"
bbox_json_dir="${10}"
#segmentation_dir="${10}"

# Store the current working directory
previous_dir=$(pwd)
echo "$camera_number"
# Count the all image data folder to get intervals without any missing frames
intervals_wodrop=$(python get_intervals_wodrop.py "$input_dir" "$output_dir" "$image_extension" "$camera_number" "$frames_count")

# Here we will divide intervals to get around 20 consecutive timestamps for each interval
echo "Intervals without any missing frames are: $intervals_wodrop"
# exit

# Remove the outer brackets and split by '], [' to get individual intervals if there are more than one
formatted_intervals=$(echo "$intervals_wodrop" | tr -d '[]')

IFS=',' # Set the separator as comma
read -ra ADDR <<< "$formatted_intervals" # Read the intervals into an array

formatted_intervals=$(echo "$formatted_intervals" | tr -d ' ') # Remove the brackets
# Assuming formatted_intervals is a string of numbers separated by commas, representing start and end points
# Convert the string into an array
IFS=',' read -ra intervals_array <<< "$formatted_intervals"

# Calculate the number of intervals
num_intervals=$((${#intervals_array[@]} / 2))

# Iterate over the intervals
for ((i=0; i < num_intervals; i++)); do
    conda activate "$1"
    if [ $i -eq 0 ]; then
        first_int_start=${intervals_array[0]}
        first_int_end=${intervals_array[1]}
    fi
    # Calculate index of start and end points
    start_index=$((2*i))
    end_index=$((2*i + 1))

    # Extract start and end points from the array
    start_frame=${intervals_array[$start_index]}
    end_frame=${intervals_array[$end_index]}

    if [ "$start_frame" -eq 101 ] && [ "$end_frame" -eq 120 ]; then
        echo "Processing interval from $start_frame to $end_frame"
        # Place your processing commands here

        echo "Processing interval from $start_frame to $end_frame"

        # Now, call the Python script with the interval start and end as the last two arguments
        
        python organize_image_folders_new.py "$input_dir" "$output_dir" "$image_extension" "$camera_number" "$start_frame" "$end_frame"

        # Run Colmap to get transforms.json file
        colmap_input_dir="$output_dir/$start_frame-$end_frame/colmap_input"
        colmap_output_dir="$output_dir/$start_frame-$end_frame/colmap_output"

        # Replace 'your_matching_method' with your desired method
        matching_method="exhaustive"
        ns-process-data images --data "$colmap_input_dir" --matching_method "$matching_method" --output_dir "$colmap_output_dir"
        echo "$colmap_input_dir"    
        # Undistort images for LLFF img2poses.py input to get poses_bounds.npy
        undistorted_input_dir="$colmap_output_dir"
        undistorted_output_dir="$output_dir/$start_frame-$end_frame/undistorted_LLFF_input"
        python undistort_images.py "$undistorted_input_dir" "$undistorted_output_dir" --img_ext "$image_extension"
        echo "Undistorted images for LLFF input are located at: $undistorted_output_dir"

        nested_undistorted_input_dir="$output_dir/$start_frame-$end_frame/original_images"
        nested_undistorted_output_dir="$output_dir/$start_frame-$end_frame/undistorted_images"
        json_file="$colmap_output_dir/transforms.json"
        python undistort_images_nested.py "$nested_undistorted_input_dir" "$nested_undistorted_output_dir" "$json_file" --img_ext "$image_extension"
        echo "Undistorted all images to: $nested_undistorted_output_dir"
        
        # Deactivate the 'nerfspaceport' conda environment
        conda deactivate

        # Activate the 'LLFF' conda environment
        conda activate "$2"

        # Run imgs2poses.py
        cd "$llff_path"
        imgs2poses_input_dir="$undistorted_output_dir"
        python imgs2poses.py "$imgs2poses_input_dir"
        
        # if [ $i -eq 0 ]; then
        #     poses_bounds_path=$"$output_dir/$first_int_start-$first_int_end/undistorted_LLFF_input/poses_bounds.npy"
        # fi
        poses_bounds_path=$"$output_dir/$first_int_start-$first_int_end/undistorted_LLFF_input/poses_bounds.npy"

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
            hsv_masked_imgs_dir="$output_dir/$start_frame-$end_frame/masked_undistorted_images_hsv"
            python color_filter_imgs.py "$nested_undistorted_output_dir" "$hsv_masked_imgs_dir" "$bbox_json_dir"
        elif [ "$masking_method" == "sam" ]; then
            # Apply segment anything masking
            hsv_masked_imgs_dir="$output_dir/$start_frame-$end_frame/masked_undistorted_images"
            # segmentation_dir="/home/faruk/Softwares/repos/cloned_repos"
            # cd "$segmentation_dir"
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
                --device gpu \
        else
            echo "Invalid masking method. Please choose either 'bbox' or 'hsv'."
            exit 1
        fi

        cd "$previous_dir"
        cp "$poses_bounds_path" "$hsv_masked_imgs_dir/poses_bounds.npy"
        # Copy the first frame of each camera from masked undsitorted images to a new directory

        filtered_first_frames="$output_dir/$start_frame-$end_frame/filtered_first_frames/images_in"
        mkdir -p "$filtered_first_frames"

        echo "Start copying first frames"
        python copy_first_frames.py "$hsv_masked_imgs_dir" "$filtered_first_frames" "$image_extension" "$camera_number"


        echo "First frames copied and renamed successfully."
        
        colmap_run_output_dir="$output_dir/$start_frame-$end_frame/filtered_first_frames/colmap_out"
        # Run colmap to ge points3D.bin
        ns-process-data images --data "$filtered_first_frames" --output_dir "$colmap_run_output_dir"

        cp "$colmap_run_output_dir/colmap/sparse/0/points3D.bin" "$hsv_masked_imgs_dir/points3D.bin"

    else
        echo "Skipping interval from $start_frame to $end_frame"
    fi
done

echo "Processing complete."


