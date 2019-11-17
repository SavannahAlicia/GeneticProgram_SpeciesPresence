#!/bin/bash
if [ -d ./output ]; then
    rm -R ./output;
fi
mkdir ./output;
delay=-1
current_num=0
for filename in ./input_data/*.csv; do
    current_num=$((current_num+1));
    echo "$current_num: $filename";
    if ((current_num >= delay)); then
        filename=${filename#\.\/} # remove first dot
        foldername=${filename##*\/} # remove the longest matching suffix pattern (which is anything, followed by a slash)
        foldername=${foldername%%.*} # remove the longest matching prefix pattern (which is anything, preceeded by a dot)
        echo "foldername: $foldername";
        echo "filename: $filename";

        mkdir ./output/$foldername;
        for ((i=1; i<=1; i++)); do
            mkdir ./output/$foldername/$foldername.$i;
            python3 GP_Main.py "$(pwd)/$filename" "$(pwd)/output/$foldername/$foldername.$i";
        done
    fi
done
