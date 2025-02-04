# LCS Problem

**Overview**

This project implements the Longest Common Subsequence (LCS) algorithm using various parallelization techniques:

- **Sequential LCS:** A serial implementation for reference.
- **Parallel LCS (Threads):** A parallel implementation using standard C++ threads.
- **Parallel LCS (MPI):** A parallel implementation using the Message Passing Interface (MPI) for distributed computing.

**Requirements**

- **C++ Compiler:** A C++ compiler like GCC or Clang.
- **MPI Library:** For the MPI-based implementation, you'll need an MPI library like OpenMPI or MPICH.
- **CMake:** A build system to configure and build the project.


**Building the Project**

1. **Clone the Repository**
   ```bash
   git clone https://github.com/parshanpourbakht/lcs_problem.git
   
2. **Create a build directory**
   ```bash
   mkdir build
   cd build

3. **Configure the project with CMake**
   ```bash
   cmake ../lcs_problem
   
4. **Build the project**
   ```bash
   make
   
5. **Run Executables**
   ```bash
   ./lcs_serial --str1 <first string> --str2 <second string>
   ./lcs_parallel --nThreads <number of threads> --str1 <first string> --str2 <second string>
   mpirun -n <number of processes> ./lcs_distributed --str1 <first string> --str2 <second string>

6. **Run Scripts**
   ```bash
   cd ../lcs_problem/scripts
   cmake ../
   make
   edit generate_jobs_*.py files and set the "USER_ID" variable at the top to your slurm user ID 
   python3 generate_jobs_serial.py
   python3 generate_jobs_parallel.py
   python3 generate_jobs_distributed.py
   
   
