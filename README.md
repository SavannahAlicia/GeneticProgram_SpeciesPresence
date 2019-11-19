# GeneticProgram_SpeciesPresence

## Installation and Setup
This program uses python 3. Dependencies are listed in `requirements.txt`. It is recommended you install in a virtual environment. I recommend using the built-in `venv` module for python3, as [described in the docs](https://docs.python.org/3/tutorial/venv.html). 


### In a Windows Environment
1) Prepare Python alias
    I strongly recommend using git bash if you are in a Windows environment. Run git bash as administrator. You will need to set an alias for python in Windows.
    ```bash
    $ alias python3='winpty python.exe'
    ```
    You can now proceed to the directions for a Unix-like Environment

### In a Unix-like Environment
1) Create virtual environment
    ```bash 
    $ python3 -m venv .venv # create a virtual environment with a clean python version. The virtual environment is created in the directory `venv/`
    ```
2) Start Virtual Environment
    ```bash
    $ source .venv/bin/activate # enter/start the virtual environment
    ```
3) Install Dependencies in Virtual Environment
    ```bash
    (.venv) $ pip3 install -r requirements.txt # install dependencies for the specific script into the virtual environment's python.
    ```



You are now ready to run the program.

## Running the Program

To run the algorithm, use the following format:
```bash
$ python3 GP_Main.py path/to/input.csv path/to/output.txt
```
If you would like to print all output possible for the program, include the argument `--verbose` with the above in any position after `GP_Main.py`.

### Input File
Your input file should be a csv containing columns for your covariates and one column titled `presence` that contains `1`'s and `0`'s where `1` represents a success ("species presence") and `0` represents a failure ("species psuedo absence"). All other columns will be included as covariates. It is important to balance your dataset so that the number of `1`'s and `0`'s in `presence` are approximately equivalent. 

### Output File
Your output files will be written as a text file formatted using indentations so you can visualize the tree. It will also include the fitness of the tree.

## Interrupting
To force quit the process in a Unix-like environment, use `Ctrl-C`.

