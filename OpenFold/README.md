This folder contains information, scripts and other examples about how to use the **OpenFold** model, a fast, memory-efficient and trainable implementation of AlphaFold2.

You can find here some folders:

* `scripts`: it contains the necessary scripts to run the model. There you can find some explanations about the code.
    * `run_pretrained_openfold.py`: this Python scripts is directly downloaded from the model [Github](https://github.com/aqlaboratory/openfold#usage) and it is used to predict the structure from a fasta file as input. More details inside the script.

    * `run_openfold.sh`: this is the script we run inside the cluster, with the correct configuration and the necessary modules to run OpenFold there. 

* `examples`: this folder contains some protein predictions used as an example.  
    * `examples/data`: it contains the FASTA files I used as examples.
    
    * `examples/results`: it contains the predicted protein structures obtained using as input the files from the `example/data` folder.

    
