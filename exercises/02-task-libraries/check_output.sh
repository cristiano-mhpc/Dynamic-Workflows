#!/bin/bash

reference_file="result.out"
temp_output=$(mktemp)

source venv/bin/activate
python dask_application.py config.yml > "$temp_output"

# Compare output to reference
if diff -q "$reference_file" "$temp_output" > /dev/null; then
  echo "Success"
else
  echo "The output is not correct"
  echo "Differences:"
  diff "$reference_file" "$temp_output"
fi

# Clean up
rm -f "$temp_output"
