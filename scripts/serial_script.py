import subprocess
import string
import random

# Function to generate random strings of a given size
def generate_random_string(size):
    return ''.join(random.choices(string.ascii_uppercase, k=size))

# Function to run the serial LCS program with specific parameters
def run_lcs_serial(str1, str2):
    # Command to execute the compiled serial C++ program
    command = ["./lcs_serial", f"--str1={str1}", f"--str2={str2}"]

    try:
        # Run the C++ program and capture the output
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        # Extract the time and LCS length from the output
        output = result.stdout
        time_line = next(line for line in output.splitlines() if "Time" in line)
        lcs_line = next(line for line in output.splitlines() if "LCS" in line)
        time_seconds = float(time_line.split(":")[1].strip())
        lcs_length = len(lcs_line.split(":")[1].strip())
        lcs_string = lcs_line.split(":")[1].strip()
        return time_seconds, lcs_length, lcs_string
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        return None, None

# Main function to run benchmarks
def run_benchmarks():
    # Parameters for the benchmark
    string_sizes = [100, 500, 1000, 5000, 10000]  # Different sizes of strings to test
    results = []

    # Run the LCS program for each string size
    for size in string_sizes:
        print(f"Running serial LCS with string size {size}...")
        str1 = generate_random_string(size)
        str2 = generate_random_string(size)
        time_seconds, lcs_length, lcs_string = run_lcs_serial(str1, str2)
        if time_seconds is not None:
            results.append(f"String Size: {size}, Time (s): {time_seconds:.5f}, LCS Length: {lcs_length}, LCS: {lcs_string}")

    # Save results to a text file
    txt_file = "serial_lcs_benchmark_results.txt"
    with open(txt_file, mode="w") as file:
        file.write("\n".join(results))
    
    print(f"Benchmark results saved to {txt_file}")

# Run the script
if __name__ == "__main__":
    run_benchmarks()
