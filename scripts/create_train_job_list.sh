#!/bin/bash
echo "#!/bin/bash" > train_all.sh
echo "start=\$(date +%s)" >> train_all.sh

for folder in `find /home/alper/Spaceport/data/15-07-2024_oguz_3_348_frames_20_interval  -mindepth 1   -maxdepth 1 -type d |sort -V`
do
    base_name=`basename $folder`
    echo "python train.py -s $folder/masked_undistorted_images  --port 6017 --expname 15-07-2024_train_oguz_3_348_frames_20_interval_same_cam_poses/${base_name} --configs arguments/dynerf/default.py" >> train_all.sh
done

echo "end=\$(date +%s)" >> train_all.sh

echo 'echo "Elapsed Time: $(($end-$start)) seconds"' >> train_all.sh

