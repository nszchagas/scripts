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
  echo "Starting to unzip file: ${file}"
  mv "$file" "${file//\ /}" 2>/dev/null # Removes, if exists, spaces from names.
  unzip -o "$file"                      # Flag -o: overwrites files without prompting.
done

cd "$curr_path" || exit 1
