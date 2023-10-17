# Run the script of OpenFold
python3 run_pretrained_openfold.py /gpfs/scratch/bsc08/bsc08797/openfold/tests/data/1AVX_complex.fasta \
    /gpfs/projects/shared/public/AlphaFpñd/pdb_mmcif/mmcif_files \
    --uniref90_database_path="/gpfs/projects/shared/public/AlphaFold/uniref90/uniref90.fasta" \
    --mgnify_database_path="/gpfs/projects/shared/public/AlphaFold/mgnify/mgy_clusters_2018_12.fa" \
    --pdb70_database_path="/gpfs/projects/shared/public/AlphaFold/pdb70/pdb70" \
    --uniclust30_database_path="/gpfs/projects/shared/public/AlphaFold/uniclust30/uniclust30_2018_08/uniclust30_2018_08" \
    --bfd_database_path="/gpfs/projects/shared/public/AlphaFold/bfd/bfd_metaclust_clu_complete_id30_c90_final_seq.sorted_opt"\
    --output_dir="/gpfs/scratch/bsc08/bsc08797/openfold/tests/results" \
    --model_device="cuda:1" \
    --config_preset="model_1_ptm" \
    --openfold_checkpoint_path="/home/bsc08/bsc08797/.cache/openfold/finetuning_ptm_2.pt" \
    --subtract_plddt=True

