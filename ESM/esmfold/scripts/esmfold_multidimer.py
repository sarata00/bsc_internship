import sys
import os
import torch
import esm
import biotite.structure.io as bsio
from Bio import SeqIO
import time


# Multifasta with headers
input_file = sys.argv[1]

# Output_directory
output_dir = sys.argv[2]

# Function to predict structure by ESMFold
def structures_prediction(input_file, output_dir):
    # Set output directory
    os.makedirs(output_dir, exist_ok=True)
    print("Directory created")

    # Empty the cache before loading the model
    torch.cuda.empty_cache()

    model = esm.pretrained.esmfold_v1()
    print("Model loaded")

    model = model.eval().cuda()
    print("Model evaluation")

    # Optionally, uncomment to set a chunk size for axial attention. This can help reduce memory.
    # Lower sizes will have lower memory requirements at the cost of increased speed.
    model.set_chunk_size(128)
    

  # Load the sequence from a fasta file    
    with open(input_file, "r") as f:
     record = SeqIO.read(f, "fasta")
     sequence_id = record.id
     sequence = str(record.seq)
           
    # Predict structures for each sequence
    with torch.no_grad():
     print("Start prediction")
     output = model.infer_pdb(sequence,
                         chain_linker = "G"*25)
    print("Prediction ends")
	
	  
    output_filename = f"{output_dir}/{sequence_id}.pdb"
    with open(output_filename, "w") as f:
      f.write(output)

	# Load structure and calculate pLDDT
    plddt = []
    struct = bsio.load_structure(output_filename, extra_fields=["b_factor"])
    plddt = (sequence_id, struct.b_factor.mean())

    # Write pLDDT values to output file
    with open(f"{output_dir}/plddt.txt", "w") as f:
      f.write(f"{sequence_id}: {plddt}\n")

# Record the start time
start_time = time.time()

structures_prediction(input_file, output_dir)

# Record the end time
end_time = time.time()

# Calculate and print the duration
duration = end_time - start_time
print(f"The prediction took {duration} seconds.")

