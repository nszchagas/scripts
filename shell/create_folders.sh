#!/bin/bash

function create_folders() {

  cd "$folder" || exit 1
  ls

}

if [ $# -ne 1 ]; then
  echo "Provide path"
else
  folder=$1
fi

create_folders
