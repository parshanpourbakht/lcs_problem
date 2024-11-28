import os
import time
import subprocess
import glob


# Compile the C++ code
subprocess.run(["make"], shell=False)

output_dir = "sbatch_files"
os.makedirs(output_dir, exist_ok=True)

STUDENT_ID = "vba16"
ASSIGNMENT_FOLDER = "project"

assert STUDENT_ID and ASSIGNMENT_FOLDER, "Please fill in the STUDENT_ID and ASSIGNMENT_FOLDER variables."

commands = [
    f"/home/{STUDENT_ID}/{ASSIGNMENT_FOLDER}/lcs_serial",
    f"/home/{STUDENT_ID}/{ASSIGNMENT_FOLDER}/lcs_parallel"
]

# chmod the commands
for command in commands:
    subprocess.run(["chmod", "u+x", command], check=True)

mpi_processes = [1, 2, 4, 8]
nodes = [1]
iterations = 3

lcs_serial_params = "--str1 ABCDEFGHIJKLMNOPQRSTUVWXYZ --str2 ZYXWVUTSRQPONMLKJIHGFEDCBA"
heat_transfer_params = "--iCX 0.15 --iCY 0.1 --tSteps 1000 --gSize 4000 --mTemp 600"


max_jobs_per_batch = 4
max_total_cpus = 8

output_dir = "sbatch_files"
os.makedirs(output_dir, exist_ok=True)

def generate_sbatch_content(program, num_processes, num_nodes, iteration, params):
    return f"""#!/bin/bash
#SBATCH --nodes={num_nodes}
#SBATCH --ntasks={num_processes}
#SBATCH --cpus-per-task=1
#SBATCH --time=10:00
#SBATCH --mem=10G
#SBATCH --partition=slow

echo "Running {program.split('/')[-1]} with {num_processes} MPI processes on {num_nodes} nodes: Iteration {iteration}"
srun {program} {params}
"""

sbatch_files = []
cpu_requests = []
for program in commands:
    program_name = program.split('/')[-1]
    params = curve_area_params if "curve_area" in program_name else heat_transfer_params
    
    for num_processes in mpi_processes:
        for num_nodes in nodes:
            # Skip invalid combinations
            if num_processes < num_nodes:
                continue
            
            for iteration in range(1, iterations + 1):
                filename = f"test_{program_name}_n{num_processes}_nodes{num_nodes}_iter{iteration}.sbatch"
                filepath = os.path.join(output_dir, filename)
                
                sbatch_content = generate_sbatch_content(
                    program, num_processes, num_nodes, iteration, params
                )
                
                with open(filepath, 'w') as sbatch_file:
                    sbatch_file.write(sbatch_content)
                
                sbatch_files.append(filepath)
                cpu_requests.append(num_processes)

print(f"Generated {len(sbatch_files)} sbatch files in directory: {output_dir}")

def submit_sbatch(file):
    try:
        subprocess.run(["sbatch", file], check=True)
        print(f"Submitted: {file}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to submit: {file} with error: {e}")

def check_user_jobs(user_id):
    try:
        result = subprocess.run(["squeue", "-u", user_id], stdout = subprocess.PIPE, universal_newlines = True)
        return len(result.stdout.strip().split("\n")) > 1
    except subprocess.CalledProcessError as e:
        print(f"Error checking jobs: {e}")
        return False

i = 0
while i < len(sbatch_files):
    current_batch_jobs = 0
    current_batch_cpus = 0
    
    while current_batch_jobs < max_jobs_per_batch and i < len(sbatch_files):
        job_cpus = cpu_requests[i]
        
        if current_batch_cpus + job_cpus <= max_total_cpus:
            submit_sbatch(sbatch_files[i])
            current_batch_jobs += 1
            current_batch_cpus += job_cpus
            i += 1
        else:
            # over limit
            break

    print(f"Submitted {current_batch_jobs} jobs using {current_batch_cpus} CPUs.")
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    while check_user_jobs(STUDENT_ID):
        print("Waiting for jobs to finish... checking again in 5 seconds.")
        time.sleep(5)

    print("No jobs left. Proceeding to the next batch.")

def combine_slurm_outputs(output_filename="combined_output.out"):
    # Get all slurm output files (slurm-*.out)
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
    
    print(f"Combined all slurm output files into {output_filename}")


combine_slurm_outputs("combined_output.out")