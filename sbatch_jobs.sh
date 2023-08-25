#!/bin/bash
#SBATCH --ntasks-per-node=1
#SBATCH --time=00:10:00
#SBATCH --array=1-10

# Load modules
module load python/3.8.5

# Run the program
python jobSched.py