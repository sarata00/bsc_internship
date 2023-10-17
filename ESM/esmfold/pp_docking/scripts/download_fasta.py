import requests as r
import sys
import os


# Take as input file the first argument
text_file = sys.argv[1] 

# Output will be the second argument
output_file = sys.argv[2]

# Initialize an empty list to store the IDs
ids_list = []


def create_id_list(input_file):
    # Open the text file for reading
    with open(input_file, "r", encoding="latin-1") as file:

        # Iterate through each line in the file
        for line in file:
            # Remove leading/trailing whitespace and check if the line is not empty
            line = line.strip()
            if line and line[0].isdigit():
                # Append the line to the list
                ids_list.append(line)

        print(ids_list)
        return ids_list

def download_fasta_from_pdb_id(input_file, output_file):

    create_id_list(input_file)

    with open(output_file, "w") as output:
        
        for pdb_id in ids_list:

            url = f"https://www.rcsb.org/fasta/entry/{pdb_id}/download"
            data = r.get(url)
            
            data = data.text.split("\n")
            
            
            sequence_list = []

            for line in data:
                if not line.startswith(">"):
                    sequence_list.append(line)
            
            output.write(f">{pdb_id}_complex\n")
            output.write(f"{sequence_list[0]}:{sequence_list[1]}\n")


download_fasta_from_pdb_id(text_file, output_file)


    



