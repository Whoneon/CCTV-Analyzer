# CCTV-Analyzer
Check for movement in CCTV video frame


### REQUIREMENTS
```
pip install opencv-python-headless tqdm
```
### CLONE THE REPO
```
git clone https://github.com/Whoneon/CCTV-Analyzer.git
cd CCTV-Analyzer
```

### RUN THE SCRIPT!
```
python3 CCTV_Analyzer.py <video_path> <output_dir>
```

### (BULK) RUN THE SCRIPT!
Do you wish to automate the process? Do you have all of your videos in a single folder, and wish to create an output folder for each one according to the filename? Use the following bash script:
```
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
        # Only get the filename to pass as the folder name for the Python script
        filename=$(basename -- "$file")
        
        # Call the Python script with two arguments: full file path and filename
        echo "Processing file '$filename':"
        python3 CCTV_Analyzer.py "$file" "$filename"
    fi
done
```
I provided a copy of the script in the repo. Just run:
```
bash Analyzer.sh "/path/to/folder/with/videos"
```
