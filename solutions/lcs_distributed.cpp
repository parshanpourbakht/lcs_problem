#include <iostream>
#include <iomanip>
#include <vector>
#include <string>
#include <algorithm>
#include "cxxopts.h"
#include "get_time.h"

#include <mpi.h>

#define DEFAULT_FIRST_STRING "AJBFAFA"
#define DEFAULT_SECOND_STRING "ABA"

using MemoizedTable = std::vector<std::vector<int>>;

MemoizedTable initialize_table(int numRows, int numCols) {
    return MemoizedTable(numRows + 1, std::vector<int>(numCols + 1, 0));
}

void 
wavefront_worker(MemoizedTable& lcsTable, 
                 const std::string& str1, 
                 const std::string& str2, 
                 int numRows, 
                 int numCols, 
                 int diag) {

    int rowStart = std::max(1, diag - numCols);
    int rowEnd = std::min(numRows, diag - 1);

    for (int row = rowStart; row <= rowEnd; ++row) {
        int col = diag - row;
        if (str1[row - 1] == str2[col - 1]) {
            lcsTable[row][col] = lcsTable[row - 1][col - 1] + 1;
        } else {
            lcsTable[row][col] = std::max(lcsTable[row - 1][col], lcsTable[row][col - 1]);
        }
    }
}

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
            lcs += str1[row - 1];
            row--;
            col--;
        } else if (lcsTable[row - 1][col] >= lcsTable[row][col - 1]) {
            row--;
        } else {
            col--;
        }
    }
    std::reverse(lcs.begin(), lcs.end());

    return lcs;
}

std::string 
lcs_distributed(const std::string& str1, 
                const std::string& str2, 
                int numRows, 
                int numCols, 
                double& serialTime, 
                int rank, 
                int size) {

    timer threadTimer;
    threadTimer.start();

    MemoizedTable lcsTable = initialize_table(numRows, numCols);
    int diagStart = rank + 1;
    int diagEnd = numRows + numCols;

    int edgeSize = std::max(numRows, numCols) + 1;
    std::vector<int> sendBuffer(edgeSize, 0), recvBuffer(edgeSize, 0);

    // Process the diagonals in round-robin 
    for (int diag = diagStart; diag <= diagEnd; diag += size) {
        // Receive data from the previous process 
        if (diag > 1 && rank != 0) {
            MPI_Recv(recvBuffer.data(), edgeSize, MPI_INT, rank - 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            // Update the LCS table based on the received data
            for (int i = 1; i <= edgeSize; ++i) {
                if (i <= numRows && diag - i <= numCols && diag - i >= 1) {
                    lcsTable[i][diag - i] = recvBuffer[i - 1];
                }
            }
        }

        // Compute the values for the current diagonal
        wavefront_worker(lcsTable, str1, str2, numRows, numCols, diag);

        // Send data to the next process
        if (rank != size - 1) {
            for (int i = 1; i <= edgeSize; ++i) {
                if (i <= numRows && diag - i <= numCols && diag - i >= 1) {
                    sendBuffer[i - 1] = lcsTable[i][diag - i];
                }
            }
            MPI_Send(sendBuffer.data(), edgeSize, MPI_INT, rank + 1, 0, MPI_COMM_WORLD);
        }
    }

    serialTime = threadTimer.stop();

    // Debugging output prints out table values
    // std::cout << "LCS Rank: " << rank << std::endl;
    // for (int i = 0; i <= numRows; ++i) {
    //     for (int j = 0; j <= numCols; ++j) {
    //         std::cout << lcsTable[i][j] << " ";
    //     }
    //     std::cout << "\n";
    // }

    if (rank == 0) {
        return backtrack_lcs(lcsTable, str1, str2, numRows, numCols);
    }
    return "";
}

int 
main(int argc, 
     char* argv[]) {

    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    cxxopts::Options options("lcs_calculation", "Calculate longest common subsequence between two strings");
    options.add_options(
        "custom",
        {
            {"str1", "First String", cxxopts::value<std::string>()->default_value(DEFAULT_FIRST_STRING)},
            {"str2", "Second String", cxxopts::value<std::string>()->default_value(DEFAULT_SECOND_STRING)}
        });

    auto cl_options = options.parse(argc, argv);
    std::string str1 = cl_options["str1"].as<std::string>();
    std::string str2 = cl_options["str2"].as<std::string>();

    int numRows = str1.length();
    int numCols = str2.length();
    double serialTime = 0;

    std::string lcsValue = lcs_distributed(str1, str2, numRows, numCols, serialTime, rank, size);

    if (rank == 0) {
        std::cout << "Distributed Implementation" << std::endl;
        std::cout << "---------------------------" << std::endl;
        std::cout << "str1: " << str1 << std::endl;
        std::cout << "str2: " << str2 << std::endl;
        std::cout << "LCS: " << lcsValue << std::endl;
        std::cout << "Time (seconds): " << serialTime << std::endl;

    }

    MPI_Finalize();
    return 0;
}
