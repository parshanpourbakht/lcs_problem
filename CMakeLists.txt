cmake_minimum_required(VERSION 3.10)
project(MyProject)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Specify the include directories
include_directories(include util)

# Add source files from the solutions and util folders
file(GLOB SOLUTION_SOURCES "solutions/*.cpp")
file(GLOB UTIL_SOURCES "util/*.cpp")

# Combine the sources into one list
set(SOURCES ${SOLUTION_SOURCES} ${UTIL_SOURCES})

# Executables
add_executable(lcs_parallel solutions/lcs_parallel.cpp)
add_executable(lcs_parallel_mpi solutions/lcs_parallel_mpi.cpp)
add_executable(lcs_serial solutions/lcs_serial.cpp)