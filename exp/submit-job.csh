#!/bin/tcsh

# Set up python and cplex environment
conda activate /usr/local/usrapps/infews/CAPOW_env

# Submit LSF job for the directory $dirName

cd "WFECVICILD2"

cd "mean_zero"

bsub -n 8 -R "span[hosts=1]" -W 5000 -o out.%J -e err.%J "python platypus_hedge_model.py"

cd ..
cd "mean_zero_10p_std"
bsub -n 8 -R "span[hosts=1]" -W 5000 -o out.%J -e err.%J "python platypus_hedge_model.py"

cd ..
cd "mean_zero_20p_std"
bsub -n 8 -R "span[hosts=1]" -W 5000 -o out.%J -e err.%J "python platypus_hedge_model.py"

cd ..
cd "mean_zero_30p_std"
bsub -n 8 -R "span[hosts=1]" -W 5000 -o out.%J -e err.%J "python platypus_hedge_model.py"

cd ..
cd "mean_zero_40p_std"
bsub -n 8 -R "span[hosts=1]" -W 5000 -o out.%J -e err.%J "python platypus_hedge_model.py"

cd ..
cd "mean_zero_50p_std"
bsub -n 8 -R "span[hosts=1]" -W 5000 -o out.%J -e err.%J "python platypus_hedge_model.py"

cd ..
cd "mean_zero_60p_std"
bsub -n 8 -R "span[hosts=1]" -W 5000 -o out.%J -e err.%J "python platypus_hedge_model.py"

cd ..
cd "mean_zero_70p_std"
bsub -n 8 -R "span[hosts=1]" -W 5000 -o out.%J -e err.%J "python platypus_hedge_model.py"

cd ..
cd "mean_zero_80p_std"
bsub -n 8 -R "span[hosts=1]" -W 5000 -o out.%J -e err.%J "python platypus_hedge_model.py"

cd ..
cd "mean_zero_90p_std"
bsub -n 8 -R "span[hosts=1]" -W 5000 -o out.%J -e err.%J "python platypus_hedge_model.py"

cd ..
cd "no_basis_risk"
bsub -n 8 -R "span[hosts=1]" -W 5000 -o out.%J -e err.%J "python platypus_hedge_model.py"

cd ..
cd "std_normal"
bsub -n 8 -R "span[hosts=1]" -W 5000 -o out.%J -e err.%J "python platypus_hedge_model.py"


conda deactivate

	
