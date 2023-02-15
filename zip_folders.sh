#!/bin/bash

for d in */ ; do
	FOLDER="$(echo "$d" | sed 's/\///g')"
	FILENAME="$FOLDER.zip"
	zip -r "$FILENAME" "$FOLDER"
done
