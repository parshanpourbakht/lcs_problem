#include <iostream>
#include "cxxopts.h"

#define DEFAULT_FIRST_STRING "AAACD"
#define DEFAULT_SECOND_STRING "ABACD"



int main(int argc, char *argv[]) {
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
  
  uint n_threads = cl_options["nThreads"].as<uint>();
  std::string first_string = cl_options["str1"].as<std::string>();
  std::string second_string = cl_options["str2"].as<std::string>();

  std::cout << "First String: " << first_string << std::endl;
  std::cout << "Second String: " << second_string << std::endl;

  int n = first_string.length();
  int m = second_string.length(); 





  return 0;
}
