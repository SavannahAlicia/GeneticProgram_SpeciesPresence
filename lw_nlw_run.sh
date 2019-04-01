#!/bin/bash
mkdir ./lw_nlw_output;
mkdir ./lw_nlw_output/lw;
mkdir ./lw_nlw_output/nlw;
for ((i=1; i<=100; i++)); do
    echo "Evaluating LW: $i";
    mkdir ./lw_nlw_output/lw/lw.$i;
    python3 GP_Main.py "./input_data/lw.csv" "./lw_nlw_output/lw/lw.$i";
    echo "Evaluating NLW: $i";
    mkdir ./lw_nlw_output/nlw/nlw.$i;
    python3 GP_Main.py "./input_data/nlw.csv" "./lw_nlw_output/nlw/nlw.$i";
done