#!/bin/bash

if [[ $# -ne 1 ]]; then
  echo "Use unzip_folder [FOLDER]"
fi

curr_path="$(pwd)"
folder=$1

if ! cd "$folder"; then
  echo "Folder doesn't exist"
  exit 1
fi

for file in "$folder"/*.zip; do
  mv "$file" "${file//\ /}" 2>/dev/null # Removes, if exists, spaces from names.
  file=${file//\ /}
  folder_name="${file/.zip//}"
  if ! [[ -d "$folder_name" ]]; then
    echo "Starting to unzip file: ${file}"
    unzip -o "$file" -d "$folder_name" # Flag -o: overwrites files without prompting.
  else
    echo "Already unzipped $file"
  fi
done

echo "Creating backup of zip archives"
mkdir -p zip_backup
mv ./*.zip zip_backup

cd "$curr_path" || exit 1
