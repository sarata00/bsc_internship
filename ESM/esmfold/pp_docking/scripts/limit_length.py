import sys

# Take as input file the first argument
input_file = sys.argv[1] 

# Output will be the second argument
output_file = sys.argv[2]

# Desired length

n =  sys.argv[3]

def limit_length(input_file, output_file, n):
    
    with open(input_file, "r") as input, open(output_file, "w") as output:
        pdb_id = ""
        seq = ""
        total_seq=0
        limited_seq=0
        for line in input:

            line.split("\n")
            
            if line.startswith(">"):
                #   If a new FASTA header is encountered, first check if the previous sequence meets the criteria
                total_seq +=1
                if len(seq) <= int(n):
                    output.write(f"{pdb_id}{seq}\n")
                    limited_seq+=1
                pdb_id = line
                seq=""
            else:
                seq += line.strip()

        # Check the last sequence after the loop ends
        if len(seq) <= int(n):
            output.write(f"{pdb_id}{seq}\n")

        print(f"Done! \"{output_file}\" file created with a {limited_seq} protein sequences (from a total of {total_seq}) with a length lower or equal to {n} aminoacids.")


limit_length(input_file, output_file, n)