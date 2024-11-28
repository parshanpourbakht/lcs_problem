import os
import time
import subprocess
import glob
import random
import string

# Function to generate random strings of a given size
def generate_random_string(size):
    return ''.join(random.choices(string.ascii_uppercase, k=size))

# Compile the C++ code
subprocess.run(["make"], check=True)

output_dir = "sbatch_files_serial"
os.makedirs(output_dir, exist_ok=True)

STUDENT_ID = "vba16"
ASSIGNMENT_FOLDER = "build"

assert STUDENT_ID and ASSIGNMENT_FOLDER, "Please fill in the STUDENT_ID and ASSIGNMENT_FOLDER variables."

commands = [
    f"/home/{STUDENT_ID}/{ASSIGNMENT_FOLDER}/lcs_serial"
]

iterations = 4
string_sizes = [8000, 12000, 14000, 18000, 20000]  # Updated string sizes

# Function to generate SBATCH content for serial execution
def generate_sbatch_content(iteration, command, str1, str2):
    return f"""#!/bin/bash
#SBATCH --cpus-per-task=1
#SBATCH --time=10:00
#SBATCH --mem=5G
#SBATCH --partition=slow

echo "Running {command.split('/')[-1]}: Iteration {iteration}"
srun {command} --str1 {str1} --str2 {str2}
"""

sbatch_files = []

# Generate SBATCH files
for string_size in string_sizes:  # Iterate over string sizes
    for iteration in range(1, iterations + 1):
        for command in commands:
            # Generate random strings for each job
            str1 = generate_random_string(string_size)
            str2 = generate_random_string(string_size)

            # Generate file name and content
            filename = f"serial_iter_{iteration}_size_{string_size}_{command.split('/')[-1]}.sbatch"
            filepath = os.path.join(output_dir, filename)
            sbatch_content = generate_sbatch_content(iteration, command, str1, str2)

            # Write SBATCH file
            with open(filepath, 'w') as sbatch_file:
                sbatch_file.write(sbatch_content)

            sbatch_files.append(filepath)

print(f"Generated SBATCH files in directory: {output_dir}")

# Function to submit a single SBATCH file
def submit_sbatch(file):
    try:
        subprocess.run(["sbatch", file], check=True)
        print(f"Submitted: {file}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to submit: {file} with error: {e}")

# Function to check the user's active jobs in SLURM
def check_user_jobs(user_id):
    try:
        result = subprocess.run(["squeue", "-u", user_id], stdout=subprocess.PIPE, universal_newlines=True)
        return len(result.stdout.strip().split("\n")) > 1
    except subprocess.CalledProcessError as e:
        print(f"Error checking jobs: {e}")
        return False

# Submit jobs in batches
for file in sbatch_files:
    submit_sbatch(file)
    print("Submitted:", file)

# Combine SLURM output files
def combine_slurm_outputs(output_filename="combined_output_serial.out"):
    slurm_files = glob.glob("slurm-*.out")

    if not slurm_files:
        print("No slurm output files found.")
        return

    slurm_files.sort(key=lambda x: int(x.split("-")[1].split(".")[0]))

    with open(output_filename, 'w') as combined_file:
        for slurm_file in slurm_files:
            with open(slurm_file, 'r') as sf:
                combined_file.write(f"--- Contents of {slurm_file} ---\n")
                combined_file.write(sf.read())
                combined_file.write("\n\n")

    print(f"Combined all SLURM output files into {output_filename}")

combine_slurm_outputs("combined_output_serial.out")
