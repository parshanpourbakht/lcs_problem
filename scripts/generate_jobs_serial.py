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

output_dir = "sbatch_files"
os.makedirs(output_dir, exist_ok=True)

USER_ID = ""

assert USER_ID, "Please fill in the USER_ID variable."

commands = [
    f"/home/{USER_ID}/lcs_problem/scripts/lcs_serial"
]

max_jobs_per_batch = 4
iterations = 4
string_sizes = [8000, 12000, 14000, 16000, 18000]  # Updated string sizes

# Function to generate SBATCH content for serial execution
def generate_sbatch_content(iteration, command, str1, str2, string_size):
    return f"""#!/bin/bash
#SBATCH --cpus-per-task=1
#SBATCH --time=10:00
#SBATCH --mem=5G
#SBATCH --partition=slow

echo "Running {command.split('/')[-1]} Size {string_size}: Iteration {iteration}"
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
            filename = f"test_iter_{iteration}_size_{string_size}_{command.split('/')[-1]}.sbatch"
            filepath = os.path.join(output_dir, filename)
            sbatch_content = generate_sbatch_content(iteration, command, str1, str2, string_size)

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
i = 0
while i < len(sbatch_files):
    current_batch_jobs = 0

    while current_batch_jobs < max_jobs_per_batch and i < len(sbatch_files):
        submit_sbatch(sbatch_files[i])
        current_batch_jobs += 1
        i += 1

    print(f"Submitted {current_batch_jobs} jobs.")
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    while check_user_jobs(USER_ID):
        print("Waiting for jobs to finish... checking again in 5 seconds.")
        time.sleep(5)

    print("No jobs left. Proceeding to the next batch.")

# Combine SLURM output files
def combine_slurm_outputs(output_filename="serial_output.out"):
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

# Function to delete all SLURM output files
def delete_slurm_outputs():
    slurm_files = glob.glob("slurm-*.out")
    for slurm_file in slurm_files:
        try:
            os.remove(slurm_file)
            print(f"Deleted: {slurm_file}")
        except OSError as e:
            print(f"Error deleting {slurm_file}: {e}")


combine_slurm_outputs("serial_output.out")
delete_slurm_outputs()
