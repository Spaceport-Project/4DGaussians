#!/bin/bash

# Pathlerin bulunduğu dosyanın yolu
path_list=("path_1" "path_2" "path_3" "path_4" "path_5" "path_6")

# Liste uzunluğu
list_length=${#path_list[@]}

# Her seferinde iki path ile işlem yap
for ((i=0; i<$list_length; i+=2)); do
  # İlk path
  python train.py -s ${path_list[i]} &

  # İkinci path (varsa)
  if [ $((i+1)) -lt $list_length ]; then
    python train.py -s ${path_list[i+1]} &
  fi

  # İki sürecin tamamlanmasını bekle
  wait
done