#include <iostream>
#include <iomanip>

#include <vector>

#include "cxxopts.h"
#include "get_time.h"
#include "optional"

#define DEFAULT_NUMBER_OF_THREADS 1
#define DEFAULT_FIRST_STRING "AAACD"
#define DEFAULT_SECOND_STRING "ABA"

using MemoizedTable = std::vector<std::vector<std::optional<int>>>;

MemoizedTable
initialize_table(int numRows, 
                 int numCols){

  MemoizedTable memoizedTable(numRows + 1, std::vector<std::optional<int>>(numCols + 1));

  // Setting the elements in first column to value 0
  for(auto& row : memoizedTable) {
    row[0] = 0; 
  }

  // Setting the elements in the first row to value 0
  std::fill(memoizedTable[0].begin(), memoizedTable[0].end(), 0);

  return memoizedTable; 
}

void 
calculate_lcs_table(MemoizedTable& lcsTable, 
                    const std::string& str1, 
                    const std::string& str2, 
                    int numRows, 
                    int numCols) {
                      
  for (int row = 1; row <= numRows; row++) {
    for (int col = 1; col <= numCols; col++) {
      if (str1[row - 1] == str2[col - 1]) {
        // If characters match, increment the LCS length from the diagonal
        lcsTable[row][col] = lcsTable[row - 1][col - 1] ? lcsTable[row - 1][col - 1].value() + 1 : 1;
      } else {
        // If no match, take the maximum value from the top or left
        auto top = lcsTable[row - 1][col] ? lcsTable[row - 1][col].value() : 0;
        auto left = lcsTable[row][col - 1] ? lcsTable[row][col - 1].value() : 0;
        lcsTable[row][col] = std::max(top, left);
      }
    }
  }
}

// Function to backtrack and reconstruct the LCS string
std::string 
backtrack_lcs(const MemoizedTable& lcsTable, 
              const std::string& str1, 
              const std::string& str2, 
              int numRows, 
              int numCols) {

  std::string lcs;
  int row = numRows, col = numCols;

  while (row > 0 && col > 0) {
    if (str1[row - 1] == str2[col - 1]) {
      lcs += str1[row - 1]; // If characters match, add to lcs string
      row--;
      col--;
    } else if (lcsTable[row - 1][col].value_or(0) >= lcsTable[row][col - 1].value_or(0)) {
      row--; // Move up if the top value is larger or equal
    } else {
      col--; // Otherwise move left
    }
  }

  // Reverse the LCS as it was built backwards
  std::reverse(lcs.begin(), lcs.end());
  return lcs;
}

std::string 
lcs_serial(const std::string& str1, 
           const std::string& str2, 
           int numRows, 
           int numCols,
           double& serialTime) {

  timer threadTimer;
  threadTimer.start();

  // Init the Table
  MemoizedTable lcsTable = initialize_table(numRows, numCols);

  // Fill the memoization table
  calculate_lcs_table(lcsTable, str1, str2, numRows, numCols);

  // Backtrack to find the LCS string
  std::string lcs = backtrack_lcs(lcsTable, str1, str2, numRows, numCols);

  serialTime = threadTimer.stop();

  return lcs;
}

int 
main(int argc, char *argv[]) {
  cxxopts::Options options("lcs_calculation",
                           "Calculate longest common string between 2 strings");
  options.add_options(
      "custom",
      {
          {"nThreads", "Number of threads", 
           cxxopts::value<uint>()->default_value(std::to_string(DEFAULT_NUMBER_OF_THREADS))},
          {"str1", "First String",         
           cxxopts::value<std::string>()->default_value(DEFAULT_FIRST_STRING)},
          {"str2", "Second String", 
           cxxopts::value<std::string>()->default_value(DEFAULT_SECOND_STRING)}
      });
  
  auto cl_options = options.parse(argc, argv);
  
  std::string str1 = cl_options["str1"].as<std::string>();
  std::string str2 = cl_options["str2"].as<std::string>();

  size_t numRows = str1.length();
  size_t numCols = str2.length(); 

  double serialTime = 0; 

  auto lcsValue = lcs_serial(str1, str2, numRows, numCols, serialTime);

  // Terminal Outputs
  std::cout << "Serial Implementation" << std::endl; 
  std::cout << "------------------------" << std::endl; 
  std::cout << std::setw(5) << std::left << "str1: " << str1 << std::endl;
  std::cout << std::setw(5) << std::left << "str2: " << str2 << std::endl;
  std::cout << std::setw(6) << std::left << "LCS: " << lcsValue << std::endl;
  std::cout << std::setw(5) << std::left << "Time (seconds): " << serialTime << std::endl;


  return 0;
}

