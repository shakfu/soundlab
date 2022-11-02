RUNTIME=../include/vult/runtime

./vultc -ccode filter.vult -o filter
g++ filter.cpp ${RUNTIME}/vultin.cpp main.cpp -I. -I${RUNTIME} -o demo
rm -f filter.cpp filter.h filter.tables.h
