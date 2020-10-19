#!/bin/tcsh

# Set up python and cplex environment
conda activate /usr/local/usrapps/infews/CAPOW_env

# Submit LSF job for the directory $dirName
bsub -n 8 -R "span[hosts=1]" -W 5000 -o out.%J -e err.%J "python platypus_hedge_model_VAR.py"

conda deactivate

	
