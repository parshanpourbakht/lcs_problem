#include <iostream>
#include <vector>
#include <array>
#include "cxxopts.h"
#include "optional"

#define DEFAULT_FIRST_STRING "AAACD"
#define DEFAULT_SECOND_STRING "ABA"

using MemoizedTable = std::vector<std::vector<std::optional<int>>>;

MemoizedTable
initialize_table(int n, int m){
  MemoizedTable memoizedTable(n + 1, std::vector<std::optional<int>>(m + 1));

  //Setting the elements in first column to value 0
  for(auto& row : memoizedTable) {
    row[0] = 0; 
  }

  //Setting the elements in the first row to value 0
  std::fill(memoizedTable[0].begin(), memoizedTable[0].end(), 0);

  return memoizedTable; 
}

std::optional<int> 
lcs_serial(MemoizedTable& lcsTable, 
                             std::string str1, 
                             std::string str2, 
                             int n, 
                             int m){

  for(int i = 1; i <= n; i++){
    for(int j = 1; j <= m; j++){
      if(str1[i-1] == str2[j-1]){
        //Checking if lcsTable[i - 1][j - 1] has a value or not
        lcsTable[i][j] = lcsTable[i - 1][j - 1] ? lcsTable[i - 1][j - 1].value() + 1 : 1;
      }
      else{
        //Checking if the top and left values of <i, j> are set with a value if not they are set to 0
        auto top = lcsTable[i - 1][j] ? lcsTable[i - 1][j].value() : 0; 
        auto left = lcsTable[i - 1][j] ? lcsTable[i][j - 1].value() : 0; 

        lcsTable[i][j] = std::max(top, left);
      }
    }
  }

  return lcsTable[n][m];
}

int 
main(int argc, char *argv[]) {
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

  size_t n = str1.length();
  size_t m = str2.length(); 

  MemoizedTable lcsTable = initialize_table(n, m);
  auto lcsValue = lcs_serial(lcsTable, str1, str2, n, m);

  //Terminal Ouputs
  std::cout << "str1: " << str1 << std::endl;
  std::cout << "str2: " << str2 << std::endl;
  std::cout << "LCS: " << *lcsValue << std::endl;

  return 0;
}
