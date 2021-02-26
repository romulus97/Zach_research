#!/bin/tcsh

# Set up python
conda activate /usr/local/usrapps/infews/CAPOW_env


cd "OKGE_SEILING"
cd "observed"

bsub -n 8 -R "span[hosts=1]" -W 5000 -o out.%J -e err.%J "python platypus_hedge_model.py"
cd ../..

cd "OKGECEDAR5LD2"
cd "observed"
bsub -n 8 -R "span[hosts=1]" -W 5000 -o out.%J -e err.%J "python platypus_hedge_model.py"
cd ../..

cd "OKGECEDAVLD2"
cd "observed"
bsub -n 8 -R "span[hosts=1]" -W 5000 -o out.%J -e err.%J "python platypus_hedge_model.py"
cd ../..

cd "OKGEIODINE4LD2"
cd "observed"
bsub -n 8 -R "span[hosts=1]" -W 5000 -o out.%J -e err.%J "python platypus_hedge_model.py"
cd ../..

cd "OKGEKEENANWIND"
cd "observed"
bsub -n 8 -R "span[hosts=1]" -W 5000 -o out.%J -e err.%J "python platypus_hedge_model.py"
cd ../..

cd "OKGESPIRITWIND"
cd "observed"
bsub -n 8 -R "span[hosts=1]" -W 5000 -o out.%J -e err.%J "python platypus_hedge_model.py"
cd ../..

cd "OKGEWDWRD1LD2"
cd "observed"
bsub -n 8 -R "span[hosts=1]" -W 5000 -o out.%J -e err.%J "python platypus_hedge_model.py"
cd ../..

cd "OKGEWDWRDEHVUNKEENAN_WIND"
cd "observed"
bsub -n 8 -R "span[hosts=1]" -W 5000 -o out.%J -e err.%J "python platypus_hedge_model.py"
cd ../..

cd "WFEC_MOORELAND_2"
cd "observed"
bsub -n 8 -R "span[hosts=1]" -W 5000 -o out.%J -e err.%J "python platypus_hedge_model.py"
cd ../..

cd "WFECVICILD2"
cd "observed"
bsub -n 8 -R "span[hosts=1]" -W 5000 -o out.%J -e err.%J "python platypus_hedge_model.py"
cd ../..


conda deactivate

	
