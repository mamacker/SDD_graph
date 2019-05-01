#!/bin/bash

#$ -M vkurtz@nd.edu
#$ -m abe
#$ -q debug

##
#
# Use gnn_formatter.py to generate attribute files for all of the 
# data in the SDD
#
##

module load python

data_dir="./full_dataset"   # directory that contains the SDD

output_dir="./gnn_data"     # directory that we'll put the finished attribute files

# find all the .mov files in the dataset directory
files=$(find $data_dir | grep .mov)
for f in $files
do
    input_dir=$(dirname $f)
    output_fname=${input_dir#"./full_dataset/"}
    output_fname=$(echo "$output_fname" | tr / _)
    echo ./gnn_formatter.py $input_dir $output_dir $output_fname

    ./gnn_formatter.py $input_dir $output_dir $output_fname
done
