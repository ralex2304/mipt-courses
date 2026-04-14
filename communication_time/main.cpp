#include <iostream>
#include <mpi.h>

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);

    int world_rank = 0;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

    int world_size = 0;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    if (world_size < 2) {
        if (world_rank == 0) {
            std::cerr << "Program requires at least 2 procesess" << std::endl;
        }
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    int count = 0;
    int target_rank = (world_rank == 0) ? 1 : 0;
    double start_time, end_time;

    MPI_Barrier(MPI_COMM_WORLD);

    if (world_rank == 0) {
        start_time = MPI_Wtime();

        MPI_Send(&count, 1, MPI_INT, 1, 0, MPI_COMM_WORLD);
        MPI_Recv(&count, 1, MPI_INT, 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);

        end_time = MPI_Wtime();

        double total_time = end_time - start_time;
        std::cout << "Round-trip time: " << total_time << " seconds\n";

    } else if (world_rank == 1) {
        MPI_Recv(&count, 1, MPI_INT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        MPI_Send(&count, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);
    }

    MPI_Finalize();
    return 0;
}
