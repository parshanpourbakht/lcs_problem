cmake_minimum_required(VERSION 3.10)
project(MyProject)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find MPI
find_package(MPI REQUIRED)

# Specify the include directories
include_directories(include util ${MPI_INCLUDE_PATH})

# Add source files from the solutions and util folders
file(GLOB SOLUTION_SOURCES "solutions/*.cpp")
file(GLOB UTIL_SOURCES "util/*.cpp")

# Combine the sources into one list
set(SOURCES ${SOLUTION_SOURCES} ${UTIL_SOURCES})

# Executables
add_executable(lcs_serial solutions/lcs_serial.cpp)
add_executable(lcs_parallel solutions/lcs_parallel.cpp)
add_executable(lcs_distributed solutions/lcs_distributed.cpp)

# Link MPI for the distributed target
target_link_libraries(lcs_distributed ${MPI_LIBRARIES})

# Custom targets for Python scripts
add_custom_target(
    serial_script
    COMMAND python3 ${CMAKE_SOURCE_DIR}/scripts/serial_script.py
    COMMENT "Running Python script for Serial LCS algorithm"
)

add_custom_target(
    parallel_script
    COMMAND python3 ${CMAKE_SOURCE_DIR}/scripts/parallel_script.py
    COMMENT "Running Python script for Parallel LCS algorithm"
)

add_custom_target(
    distributed_script
    COMMAND python3 ${CMAKE_SOURCE_DIR}/scripts/distributed_script.py
    COMMENT "Running Python script for Distributed LCS algorithm"
)
