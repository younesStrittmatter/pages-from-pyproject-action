#!/bin/sh -l

set -e

# Get the absolute path to the generate_readme.py script
build_code_reference_script_path="/build_code_reference.py"

# Get the full paths for the input and output files
input_file="$GITHUB_WORKSPACE/$1"
output_file="$GITHUB_WORKSPACE/$2"

# Execute the generate_readme.py script with the provided arguments
python $build_code_reference_script_path $input_file $output_file
