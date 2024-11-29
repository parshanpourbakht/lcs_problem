import re

def extract_size_and_time_from_block(block):
    """
    Extracts Size and Time from a single SLURM output block.
    
    Args:
        block (str): A block of SLURM output.
    
    Returns:
        tuple: (Size, Time in seconds) or None if not found.
    """
    size = None
    time_seconds = None

    # Regex to find "Size <value>"
    size_match = re.search(r"size (\d+)", block)
    if size_match:
        size = int(size_match.group(1))

    # Regex to find "Time (seconds): <value>"
    time_match = re.search(r"Time \(seconds\): ([\d\.]+)", block)
    if time_match:
        time_seconds = float(time_match.group(1))

    return size, time_seconds

def process_large_slurm_file(input_file, output_file):
    """
    Processes a large SLURM output file with multiple blocks to extract Size and Time.
    
    Args:
        input_file (str): Path to the SLURM output file.
        output_file (str): Path to save the extracted results.
    """
    results = []
    current_block = []

    with open(input_file, 'r') as file:
        for line in file:
            if line.startswith("--- Contents of slurm-") and current_block:
                # Process the current block
                block_content = "".join(current_block)
                size, time_seconds = extract_size_and_time_from_block(block_content)
                if size is not None and time_seconds is not None:
                    results.append((size, time_seconds))
                current_block = []  # Reset for the next block
            
            # Add line to the current block
            current_block.append(line)

        # Process the final block
        if current_block:
            block_content = "".join(current_block)
            size, time_seconds = extract_size_and_time_from_block(block_content)
            if size is not None and time_seconds is not None:
                results.append((size, time_seconds))

    # Save results to the output file
    with open(output_file, 'w') as f:
        f.write("Size,Time (seconds)\n")
        for result in results:
            f.write(f"{result[0]},{result[1]}\n")
    
    print(f"Extracted results saved to {output_file}")

# Example usage
process_large_slurm_file("distributed_output.out", "extracted_results.txt")
