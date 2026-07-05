cmake_minimum_required(VERSION 3.13)

find_package(MPI REQUIRED)

add_executable(mpi_app main.cpp)

target_link_libraries(mpi_app PRIVATE MPI::MPI_CXX)

add_custom_target(mpi_run
    mpirun -np 12 $<TARGET_FILE:mpi_app>
    DEPENDS mpi_app
)

