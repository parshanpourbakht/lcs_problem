#include <iostream>
#include <iomanip>
#include <vector>
#include "cxxopts.h"
#include "get_time.h"
#include "optional"
#include <thread>
#include <mutex>
#include <condition_variable>

#define DEFAULT_NUMBER_OF_THREADS 1
#define DEFAULT_FIRST_STRING "AAACD"
#define DEFAULT_SECOND_STRING "ABA"


using MemoizedTable = std::vector<std::vector<int>>;

//Set the initial values of the table to 0 and included an extra row and column for the base case
MemoizedTable initialize_table(int numRows, int numCols){
  return MemoizedTable(numRows + 1, std::vector<int>(numCols + 1, 0)); 
}

// Worker function to calculate the LCS values for a given diagonal
void wavefront_worker(MemoizedTable& lcsTable, const std::string& str1, const std::string& str2, int numRows, int numCols, int diag) {
  // Calculate the row and column bounds for the current diagonal
  int rowStart = std::max(1, diag - numCols);
  int rowEnd = std::min(numRows, diag - 1);

  // Calculate the LCS values for the current diagonal
  for (int row = rowStart; row <= rowEnd; ++row){
    int col = diag - row;
    // If characters match, increment the LCS length from the diagonal
    if (str1[row - 1] == str2[col - 1]) {
      lcsTable[row][col] = lcsTable[row - 1][col - 1] + 1;
    } else {
      // If no match, take the maximum value from the top or left
      lcsTable[row][col] = std::max(lcsTable[row - 1][col], lcsTable[row][col - 1]);
    }
  }
}

// Function to backtrack and reconstruct the LCS string
std::string backtrack_lcs(const MemoizedTable& lcsTable, const std::string& str1, const std::string& str2, int numRows, int numCols) {

  std::string lcs;
  int row = numRows, col = numCols;

  while (row > 0 && col > 0) {
    if (str1[row - 1] == str2[col - 1]) {
      lcs += str1[row - 1]; // If characters match, add to lcs string
      row--;
      col--;
    } else if (lcsTable[row - 1][col] >= lcsTable[row][col - 1]) {
      row--; // Move up if the top value is larger or equal
    } else {
      col--; // Otherwise move left
    }
  }

  // Reverse the LCS as it was built backwards
  std::reverse(lcs.begin(), lcs.end());
  return lcs;
}

std::string lcs_parallel(const std::string& str1, const std::string& str2, int numRows, int numCols, double& serialTime, uint threadSize) {

  timer threadTimer;
  threadTimer.start();

  std::mutex mtx;
  std::condition_variable cv;
  int completedDiag = 1;
  MemoizedTable lcsTable = initialize_table(numRows, numCols);


  // Calculate the LCS values for each diagonal
  auto threadWorker = [&](int threadId){
    // Calculate the diagonals for the current thread
    for (int diag = threadId +2; diag <= numRows + numCols; diag += threadSize){
      {
        // Wait until the previous diagonal has been completed
        std::unique_lock<std::mutex> lock(mtx);
        cv.wait(lock, [&]() {return completedDiag >= diag - 1;});
      }
      
      // Call the worker function to calculate the LCS values for the current diagonal
      wavefront_worker(lcsTable, str1, str2, numRows, numCols, diag); 
      {
        // Update the completed diagonal and notify other threads
        std::lock_guard<std::mutex> guard(mtx);
        completedDiag = diag;
      }
      cv.notify_all();
    }
  };


  // Create threads and run the worker function
  std::vector<std::thread> threads;
  for (int i = 0; i < threadSize; i++){
    threads.emplace_back(threadWorker, i);
  }

  // Join the threads
  for (auto& thread : threads){
    thread.join();
  }


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
  
  uint n_threads = cl_options["nThreads"].as<uint>();
  std::string str1 = cl_options["str1"].as<std::string>();
  std::string str2 = cl_options["str2"].as<std::string>();


  size_t numRows = str1.length();
  size_t numCols = str2.length(); 

  double serialTime = 0; 

  auto lcsValue = lcs_parallel(str1, str2, numRows, numCols, serialTime, n_threads);

  // Terminal Outputs
  std::cout << "Parallel Implementation" << std::endl; 
  std::cout << "------------------------" << std::endl; 
  std::cout << std::setw(5) << std::left << "Number of Threads: " << n_threads << std::endl;
  std::cout << std::setw(5) << std::left << "str1: " << str1 << std::endl;
  std::cout << std::setw(5) << std::left << "str2: " << str2 << std::endl;
  std::cout << std::setw(6) << std::left << "LCS: " << lcsValue << std::endl;
  std::cout << std::setw(5) << std::left << "Time (seconds): " << serialTime << std::endl;


  return 0;
}

