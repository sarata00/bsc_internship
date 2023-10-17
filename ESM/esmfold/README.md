# How to run ESMFold step by step


  								    
For predictions and other high-computing jobs, we use CTE-POWER   
cluster (bsc08797@plogin1.bsc.es). Then, when we are inside we    
go to the scratch folder:
	
	cd /gpfs/scratch/bsc08/bsc08797/		            
 								    
---


## 1. Download ESMFold models (MareNostrum cluster)

	THIS SECTION HERE YOU HAVE TO DO ONLY ONCE! 

---

- They require a lot of space, so we need to connect to MareNostrum cluster login 0 (bsc08797@mn0.bsc.es)
because is the only login with internet conexion:

		ssh bsc08797@mn0.bsc.es

- Once we are inside the cluster, we create the following folder:

		mkdir /home/bsc08/bsc08797/.cache/torch/hub/checkpoints
	
- Then we can download from ESM GitHub the following models:
	
	* esm2_t36_3B_UR50D-contact-regression.pt
			
			curl https://dl.fbaipublicfiles.com/fair-esm/regression/esm2_t36_3B_UR50D-contact-regression.pt -O
		
	* esm2_t36_3B_UR50D.pt
		
			curl https://dl.fbaipublicfiles.com/fair-esm/models/esm2_t36_3B_UR50D.pt -O
	
	* esmfold_3B_v1.pt
		
			curl https://dl.fbaipublicfiles.com/fair-esm/models/esmfold_3B_v1.pt -O

	These model URLs are automatically downloaded to: 
			
		~/.cache/torch/hub/checkpoints




## 2. Run the model (CTE-POWER cluster)

- We change to CTE-POWER cluster (bsc08797@plogin1.bsc.es).
	
		ssh bsc08797@plogin1.bsc.es

- Go to the scratch folder:
	
		cd /gpfs/scratch/bsc08/bsc08797

- Here we create a .sh file called "esmfold_run.sh" with the following content:
	
		#!/bin/bash
		
		#SBATCH --job-name="esmfold"
		#SBATCH --output="./out_esmfold_%A"
		#SBATCH --error="./err_esmfold_%A"
		#SBATCH --ntasks=1
		#SBATCH --cpus-per-task=40
		#SBATCH --gres=gpu:1
		#SBATCH --time=00:10:00
		#SBATCH --qos=debug

		module purge && module load gcc openmpi anaconda3 cuda/10.2 cudnn/7.6.4

		source activate esmfold

		python3 esmfold_from_multifasta_new.py ./data/input.fasta ./results/output

		conda deactivate
	
**NOTE**

* `esmfold_from_multifasta_new.py`: refers to Python script to run the ESMFold model
* `./data/input.fasta`: refers to the directory of the input file
* `./results/output`: refers to the directory of the output file

---


The `esmfold_from_multifasta_new.py` should be inside this scratch folder, where the .sh file is. In my local computer I have this script in the following directory `/home/sara/Documents/BSC_internship/ESM2/esmfold/scripts`

After that, we can run the model and create structures by running:

	sbatch esmfold_run.sh


		
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
