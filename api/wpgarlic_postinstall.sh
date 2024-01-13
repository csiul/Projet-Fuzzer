#!/bin/bash

# Delete useless directories
cd ./wpgarlic
rm -r .git
rm -r bin
rm -r examples
rm -r test

# Move replacement files
cd ..
mv ./replacements/print_findings.py ./wpgarlic/
rm -r replacements

# Create required structure
cd ./wpgarlic/data
mkdir scanned_results

# Create the output.json file
touch output.json