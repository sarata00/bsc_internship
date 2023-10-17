import sys
import time
import os
import torch
import esm
import biotite.structure.io as bsio
from Bio import SeqIO

from fairscale.nn.data_parallel import FullyShardedDataParallel as FSDP
from fairscale.nn.wrap import enable_wrap, wrap


# initialize the model with FSDP wrapper
fsdp_params = dict(
    mixed_precision=True,
    flatten_parameters=True,
    state_dict_device=torch.device("cpu"),  # reduce GPU mem usage
    cpu_offload=True,  # enable cpu offloading
)

# Multifasta with headers
input_file = sys.argv[1]

# Output_directory
output_dir = sys.argv[2]

# Function to predict structure by ESMFold
def structures_prediction(input_file, output_dir):
    
    # Set output directory
    os.makedirs(output_dir, exist_ok=True)
    print("Directory created")

    # init the distributed world with world_size 1
    url = "tcp://localhost:23456"
    torch.distributed.init_process_group(backend="nccl", init_method=url, world_size=1, rank=0)

    print("Start wrapping")

    with enable_wrap(wrapper_cls=FSDP, **fsdp_params):
        model = esm.pretrained.esmfold_v1()
        model = model.half()  # convert all parameters to float16
        # model = model.float()  # convert all parameters to float32

         # Set requires_grad to True for all parameters
        for param in model.parameters():
            param.requires_grad = False


        model.eval().cuda()
    
        # Wrap each layer in FSDP separately
        for name, child in model.named_children():
            if name == "layers":
                for layer_name, layer in child.named_children():
                    wrapped_layer = wrap(layer)
                    setattr(child, layer_name, wrapped_layer)
        model = wrap(model)

    print("FSDP ends")

    # Load the sequence from a fasta file    
    with open(input_file, "r") as f:
       record = SeqIO.read(f, "fasta")
       sequence_id = record.id
       sequence = str(record.seq)
    print("Sequence loaded")

    # Predict structures for each sequence
    print("Starting prediction")
    with torch.no_grad():
        output = model.infer_pdb(sequence)
                         # chain_linker = "G"*25)

    print("Prediction ends")
	
	  
    output_filename = f"{output_dir}/{sequence_id}.pdb"
    with open(output_filename, "w") as f:
        f.write(output)
    print("output file created")

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