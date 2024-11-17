#compiler setup
CXX = g++
CXXFLAGS = -std=c++14 -O3 -pthread $(MACRO)

PARALLEL= lcs_parallel_mpi lcs_parallel lcs_serial
ALL= $(PARALLEL)


all : $(ALL)

% : %.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

.PHONY : clean

clean :
	rm -f *.o *.obj $(ALL)
