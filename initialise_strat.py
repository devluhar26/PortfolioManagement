import os
import subprocess

# Specify the folder containing the Python files
folder_path = "test_strategies"

# List all files in the folder
for filename in os.listdir(folder_path):
    # Check if the file is a Python script
    if filename.endswith(".py"):
        file_path = os.path.join(folder_path, filename)
        print(f"Running {file_path}...")
        # Run the Python script
        result = subprocess.run(["python", file_path], capture_output=True, text=True)
        # Print the output
        print(f"Output of {filename}:\n{result.stdout}")
        if result.stderr:
            print(f"Errors in {filename}:\n{result.stderr}")
