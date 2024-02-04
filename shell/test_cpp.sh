#!/bin/bash

if [ $# -eq 1 ]; then
	input_files=input*
	src_file=$1
elif [ $# -eq 2 ]; then
	input_files=$2
	src_file=$1
else
	printf "Provide file to run."
	exit 1
fi

if ! [ $src_file == *\.cpp* ]; then
	src_file="$src_file.cpp"
fi

printf "Compiling $src_file."

outputs="$(ls out* 2>/dev/null)"
if ! [ -z "$outputs" ]; then
	printf "Testing input with outputs out{x}."
	test=true
else
	test=false
fi

compile $src_file 2>/dev/null || compile "$src_file.cpp" || exit 1

for f in $input_files; do

	./a.out <"$f" >"out_$f"
	if [ $test = true ]; then
		diffs=$(diff "out_$f" "${f/input/out}" --color --suppress-common-lines --ignore-blank-lines)
		printf "Run with input $f: "
		if [ -z "$diffs" ]; then
			printf "Success"
		else
			echo "Failed: $diffs"
		fi
	fi
	rm "out_$f"
	printf "\n"
done
