#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include "cxxopts.h"
#include "get_time.h"

#include <mpi.h>

#define DEFAULT_FIRST_STRING "AAACD"
#define DEFAULT_SECOND_STRING "ABA"

using MemoizedTable = std::vector<std::vector<int> >;

MemoizedTable 
initialize_table(int numRows, 
                 int numCols){

  return MemoizedTable(numRows + 1, std::vector<int>(numCols + 1, 0)); 
}

void 
lcs(const std::string &str1, 
         const std::string &str2, 
         int startRow, 
         int endRow, 
         MemoizedTable &lcsTable) {

  int numRows = str1.size();
  int numCols = str2.size();
    
  for (int row = startRow; row < endRow; ++row) {
    for (int col = 1; col <= numCols; ++col) {
      if (str1[row - 1] == str2[col - 1]) {
        lcsTable[row][col] = lcsTable[row - 1][col - 1] + 1;
      } else {
        lcsTable[row][col] = std::max(lcsTable[row - 1][col], lcsTable[row][col - 1]);
      }
    }
  }
}

std::string 
backtrack_lcs(const std::string &str1, 
              const std::string &str2, 
              const MemoizedTable &lcsTable) {

  int row = str1.size();
  int col = str2.size();
  std::string lcs;

  while (row > 0 && col > 0) {
    if (str1[row - 1] == str2[col - 1]) {
      lcs.push_back(str1[row - 1]);
      row--;
      col--;
    } else if (lcsTable[row - 1][col] > lcsTable[row][col - 1]) {
      row--;
    } else {
      col--;
    }
  }

  std::reverse(lcs.begin(), lcs.end());
  return lcs;
}

void 
lcs_distributed(const std::string& str1, 
                const std::string& str2, 
                int numRows, 
                int numCols, 
                int rank, 
                int size) {

  // Init of LCS table                  
  MemoizedTable lcsTable = initialize_table(numRows, numCols);

  // Decomposition of rows for each process
  int processRows = (numRows + size - 1) / size;
  int startRow = rank * processRows + 1; 
  int endRow = std::min((rank + 1) * processRows + 1, numRows + 1);

  // Synchronize with the last row of the previous process
  if (rank > 0) {
    MPI_Recv(lcsTable[startRow - 1].data(), numCols + 1, MPI_INT, rank - 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
  }

  // Compute segment of the LCS table
  lcs(str1, str2, startRow, endRow, lcsTable);

  // Send the last row of this segment to the next process
  if (rank < size - 1) {
    MPI_Send(lcsTable[endRow - 1].data(), numCols + 1, MPI_INT, rank + 1, 0, MPI_COMM_WORLD);
  }

  // Gather the computed segments back to process 0
  if (rank == 0) {
    for (int p = 1; p < size; ++p) {
      int processStartRow = p * processRows + 1;
      int processEndRow = std::min((p + 1) * processRows + 1, numRows + 1);

      for (int row = processStartRow; row < processEndRow; ++row) {
        MPI_Recv(lcsTable[row].data(), numCols + 1, MPI_INT, p, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
      }
    }

    // Calculate the LCS string
    std::string lcs = backtrack_lcs(str1, str2, lcsTable);

    // Print the LCS length and string
    std::cout << "Distributed Implementation" << std::endl; 
    std::cout << "------------------------" << std::endl; 
    std::cout << std::setw(5) << std::left << "Number of Processes: " << size << std::endl;
    std::cout << std::setw(5) << std::left << "str1: " << str1 << std::endl;
    std::cout << std::setw(5) << std::left << "str2: " << str2 << std::endl;
    std::cout << "LCS: " << lcs << std::endl;
  } else {
    for (int row = startRow; row < endRow; ++row) {
      MPI_Send(lcsTable[row].data(), numCols + 1, MPI_INT, 0, 0, MPI_COMM_WORLD);
    }
  }
}

int 
main(int argc, char** argv) {
  MPI_Init(&argc, &argv);

  int rank, size;
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);

  cxxopts::Options options("lcs_calculation",
                           "Calculate longest common string between 2 strings");
  options.add_options(
      "custom",
      {
          {"str1", "First String",         
           cxxopts::value<std::string>()->default_value(DEFAULT_FIRST_STRING)},
          {"str2", "Second String", 
           cxxopts::value<std::string>()->default_value(DEFAULT_SECOND_STRING)}
      });
  
  auto cl_options = options.parse(argc, argv);
  
  std::string str1 = cl_options["str1"].as<std::string>();
  std::string str2 = cl_options["str2"].as<std::string>();

  int numRows = str1.length();
  int numCols = str2.length(); 

  // Initialize and start the timer
  timer threadTimer;
  threadTimer.start();

  lcs_distributed(str1, str2, numRows, numCols, rank, size);
  MPI_Barrier(MPI_COMM_WORLD);

  // Stop the timer and calculate total time
  double totalTime = 0;

  if (rank == 0){
    totalTime = threadTimer.stop();
    // Print the timing information only from rank 0
  
    std::cout << "Time (seconds): " << totalTime << std::endl;
  }

  
  

  MPI_Finalize();
  return 0;
}
