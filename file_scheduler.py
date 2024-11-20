import os
import subprocess
import ast

# Store results from all scripts
def timer():
    return 0

def run_file(filename):
        file_path = os.path.join("test_strategies", filename)
        print(f"Running {file_path}...")
        result = subprocess.run(
            ["python", file_path], capture_output=True, text=True
        )
        # Check if the script ran successfully
        if result.returncode == 0:
            try:
                # Parse the output as a Python object
                output_array = ast.literal_eval(result.stdout.strip())
                print(f"Captured output from {filename}: {output_array}")
                file=open("memory/"+filename[:-3]+".txt","w")
                file.write(str(output_array))
                file.close()


                #error handling
            except:
                print(f"Error parsing output from {filename}")
        else:
            print(f"Script {filename} failed with errors:\n{result.stderr}")