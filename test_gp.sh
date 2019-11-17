#!/bin/bash

# Because windows is terrible:
alias python3='winpty python.exe';
if [ -d ./output ]; then
    rm -R ./output;
fi
mkdir ./output;
mkdir ./output/lw;
mkdir ./output/nlw;

for ((i=1; i<=20; i++)); do
    mkdir ./output/lw/lw.$i;
    mkdir ./output/nlw/nlw.$i;
    echo "Running lw.$i...";
    python3 GP_Main.py "C:\Users\Savannah Rogers\Documents\MSGrizzlyProject\GeneticProgram_SpeciesPresence\input_data\lw.csv" "./output/lw/lw.$i";
    echo "Running nlw.$i...";
    python3 GP_Main.py "C:\Users\Savannah Rogers\Documents\MSGrizzlyProject\GeneticProgram_SpeciesPresence\input_data\nlw.csv" "./output/nlw/nlw.$i";
done