#!/bin/bash

# Requirement exif

if [[ $# -ne 1 ]]; then
  echo "Use mv_to_root [FOLDER]"
  exit 1
fi

curr_path="$(pwd)"
folder=$1

if ! cd "$folder"; then
  echo "Folder doesn't exist."
  exit 1
fi

for file in "$folder"/*; do
  filename=$(basename "$file")
#  echo $filename
  mv "$file/$filename-exif/" "/home/nicolas/Pictures/photos/"
  #  if [[ -s $file ]]; then
  #    mv "$file" "${file/.JPG/\.jpg}" 2>/dev/null # Removes, if exists, spaces from names.
  #  fi
done
#
#for file in "$folder"/*.jpeg; do
#  if [[ -s $file ]]; then
#    mv "$file" "${file/.jpeg/\.jpg}" 2>/dev/null # Removes, if exists, spaces from names.
#  fi
#done
#
#for file in "$folder"/*.jpg; do
#  if [[ -s $file ]]; then
#    mv "$file" "${file//\ /}" 2>/dev/null # Removes, if exists, spaces from names.
#    file=${file//\ /}
#
#    echo "Starting to extract exif from file: ${file}"
#
#    read -r date time <<<"$date_time"
#    exif_date=$(date -d "${date//:/-}T${time}" +"%F-%H%M%S")
#    if extract_exif; then
#      extension=${filename##*.}
#      new_name="$folder/exif/$exif_date.$extension"
#      mv "$file" "$new_name"
#    fi
#  fi
#done

cd "$curr_path" || exit 1
