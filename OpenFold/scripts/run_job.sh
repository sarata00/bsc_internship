#!/bin/bash
#SBATCH --job-name="openfold"
#SBATCH --output="./out/out_openfold_%A"
#SBATCH --error="./err/err_openfold_%A"
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=40
#SBATCH --gres=gpu:1
#SBATCH --time=00:10:00
#SBATCH --qos=debug
  
# Load all the necessary modules for run the task
module purge && module load gcc openmpi anaconda3 cuda/10.2 cudnn/7.6.4 singularity 

# Run the Openfold script
singularity exec --nv /apps/SINGULARITY/SRC/images/openfold-1.0.0.sif ./
run_openfold.sh
