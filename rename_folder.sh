#!/bin/bash

if [[ $# -ne 1 ]]
then 
echo "Provide new name"
else
echo "$1"

mkdir misc
for f in *
    do
        if [[ "$f" =~ ' ' ]] 
            then
            mv "$f" `echo $f | tr ' ' '_'`;
            f=${f// /_}
        fi
        if [ -f $f ]
            then
            echo "$f -> file found"
            mv "$f" misc
        elif [ -d $f ]
            then
            mv -- $f "$1_$f"
            echo "new folder name: $1_$f"
        else 
            echo "$f"
        fi    
    done
fi 

# read move 
mv misc "$1_misc/" || echo "Already renamed"
mv $1_* ..
echo "After moving:"
ls .
cd ..