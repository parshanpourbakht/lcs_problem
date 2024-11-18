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
   cd lcs_problem
   
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
   ./lcs_distributed --nThreads <number of threads> --str1 <first string> --str2 <second string>

6. **Run Scripts**
   ```bash
   make serial_script
   make parallel_script
   make distributed_script