#!/bin/bash

# Check if argument is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

# Assign the first argument to the "directory" variable
directory="$1"

# Check if the provided path is a valid directory
if [ ! -d "$directory" ]; then
    echo "Error: '$directory' is not a valid directory."
    exit 1
fi

# Iterate over video files in the directory
for file in "$directory"/*.{mp4,mkv,avi}; do
    # Check if the file exists and is a regular file
    if [ -f "$file" ]; then
        # Only get the filename to pass as the folder name for the python script
        filename=$(basename -- "$file")
        
        # Call the Python script with two arguments: full file path and filename
        echo "Processing file '$filename':"
        python3 CCTV_Analyzer.py "$file" "$filename"
        
        # Add any additional operations here if needed
    fi
done
