import sys
import re
import os
import torch
import esm
import biotite.structure.io as bsio
from Bio import SeqIO


# Multifasta with headers
input_file = sys.argv[1]

# Output_directory
output_dir = sys.argv[2]

# Function to predict structure by ESMFold
def structures_prediction(input_file, output_dir):
    # Set output directory
    os.makedirs(output_dir, exist_ok=True)
    print("Directory created")

    model = esm.pretrained.esmfold_v1()
    model = model.eval().cuda()

    # Optionally, uncomment to set a chunk size for axial attention. This can help reduce memory.
    # Lower sizes will have lower memory requirements at the cost of increased speed.
    model.set_chunk_size(128)

    # Load sequences from multi-FASTA file
    sequences = []
    sequences_counter = 0
    with open(input_file, "r") as f:
        for record in SeqIO.parse(f, "fasta"):
            sequences.append((record.id, str(record.seq)))  # Store (sequence_id, sequence) tuple
            sequences_counter += 1  # Increment sequence counter

    # Predict structures for each sequence
    plddts = []
    for i, (sequence_id, sequence) in enumerate(sequences):
        with torch.no_grad():
            print("Start predictions")
            output = model.infer_pdb(sequence, 
                                     chain_linker="G"*25)
            print("Predictions end")

        output_filename = f"{output_dir}/{sequence_id}.pdb"
        with open(output_filename, "w") as f:
            f.write(output)
            torch.cuda.empty_cache() 

        # Load structure and calculate pLDDT
        struct = bsio.load_structure(output_filename, extra_fields=["b_factor"])
        plddts.append((sequence_id, struct.b_factor.mean()))

    # Write pLDDT values to output file
    with open(f"{output_dir}/plddts.txt", "w") as f:
        for sequence_id, plddt in plddts:
            f.write(f"{sequence_id}: {plddt}\n")

    # Write sorted pLDDT values to output file
    with open(f"{output_dir}/plddts_sorted.txt", "w") as f:
        for sequence_id, plddt in sorted(plddts, key=lambda x: x[1], reverse=True):
            f.write(f"{sequence_id}: {plddt}\n")

structures_prediction(input_file, output_dir)

