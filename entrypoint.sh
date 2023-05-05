#!/bin/sh -l

set -e

# Get the absolute path to the generate_readme.py script
pages_from_pyproject="/pages_from_pyproject.py"

# Get the full paths for the input and output files
input_file="$GITHUB_WORKSPACE/$1"
output_path_index="$GITHUB_WORKSPACE/$2"
output_path_quick="$GITHUB_WORKSPACE/$3"

# Execute the generate_readme.py script with the provided arguments
python $pages_from_pyproject $input_file $output_path_index $output_path_quick
