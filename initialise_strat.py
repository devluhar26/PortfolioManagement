import os
import subprocess
import ast

# Specify the folder containing the Python files
folder_path = "test_strategies"

# Store results from all scripts
results = {}

# Iterate over all files in the folder
for filename in os.listdir(folder_path):
    # Check if the file is a Python script
    if filename.endswith(".py"):
        file_path = os.path.join(folder_path, filename)
        print(f"Running {file_path}...")
        result = subprocess.run(
            ["python", file_path], capture_output=True, text=True
        )
        # Check if the script ran successfully
        if result.returncode == 0:
            try:
                # Parse the output as a Python object
                output_array = ast.literal_eval(result.stdout.strip())
                results[filename] = output_array
                print(f"Captured output from {filename}: {output_array}")
                file=open("memory/"+filename[:-3]+".txt","w")
                file.write(str(output_array))
                file.close()


                #error handling
            except:
                print(f"Error parsing output from {filename}")
        else:
            print(f"Script {filename} failed with errors:\n{result.stderr}")

# Display all results
print("\nResults from all scripts:")
for script, output in results.items():
    print(f"{script}: {output}")
