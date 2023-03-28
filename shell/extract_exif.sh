#!/bin/bash

# Requirement exif

function extract_exif() {
  if ! date_time="$(exif "$file" 2>/dev/null | grep -E -o --max-count=1 '[[:digit:]]{4}:[[:digit:]]{2}:[[:digit:]]{2} [[:digit:]]{2}:[[:digit:]]{2}:[[:digit:]]{2}')"; then
    echo " > Error extracting exif from $file"
    mv "$file" "$folder/$folder-no_exif/$filename"
    return 1
  fi
}

if [[ $# -ne 1 ]]; then
  echo "Use extract_exif [FOLDER]"
fi

curr_path="$(pwd)"
folder=$1

if ! cd "$folder"; then
  echo "Folder doesn't exist."
  exit 1
fi

mkdir -p "$folder-no_exif"
mkdir -p "$folder-exif"
for file in "$folder"/*.JPG; do
  if [[ -s $file ]]; then
    mv "$file" "${file/.JPG/\.jpg}" 2>/dev/null # Removes, if exists, spaces from names.
  fi
done

for file in "$folder"/*.jpeg; do
  if [[ -s $file ]]; then
    mv "$file" "${file/.jpeg/\.jpg}" 2>/dev/null # Removes, if exists, spaces from names.
  fi
done

for file in "$folder"/*.jpg; do
  if [[ -s $file ]]; then
    mv "$file" "${file//\ /}" 2>/dev/null # Removes, if exists, spaces from names.
    file=${file//\ /}
    filename=$(basename "$file")

    echo "Starting to extract exif from file: ${file}"

    read -r date time <<<"$date_time"
    exif_date=$(date -d "${date//:/-}T${time}" +"%F-%H%M%S")
    if extract_exif; then
      extension=${filename##*.}
      new_name="$folder/exif/$exif_date.$extension"
      mv "$file" "$new_name"
    fi
  fi
done

cd "$curr_path" || exit 1
