#!/bin/bash

if [[ $# -ne 1 ]]; then
  echo "Use extract_exif [FOLDER]"
fi

curr_path="$(pwd)"
folder=$1

if ! cd "$folder"; then
  echo "Folder doesn't exist."
  exit 1
fi

for subfolder in */**/; do
#  echo $subfolder
  qt=$(ls "$subfolder" -1 | wc -l)
  if [[ $qt == 0 ]]; then
    echo "$subfolder is empty"
  fi
done
