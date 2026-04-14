#include <iostream>
#include <vector>
#include <cmath>
#include <fstream>
#include <mpi.h>

void collect_data(int rank, int size, int M, int local_M, double T, double h, std::vector<double>& u_old);

double f(double x, double t) {
    return 0.0;
}

double phi(double x) {
    return exp(-100.0 * (x - 0.2) * (x - 0.2));
}

double psi(double t) {
    return 0.0;
}

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);

    int rank = 0;
    int size = 0;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    double L = 1.0;
    double T = 1.0;
    int M = 1000;
    int K = 2000;

    double h = L / M;
    double tau = T / K;

    // CFL condition
    if (rank == 0 && (tau / h) > 1.0) {
        std::cerr << "Unstability is possible (tau/h > 1)" << std::endl;
    }

    int local_M = M / size;
    if (rank == size - 1) {
        local_M += M % size;
    }

    int global_offset = rank * (M / size);

    std::vector<double> u_old(local_M + 1, 0.0);
    std::vector<double> u_new(local_M + 1, 0.0);

    for (int m = 1; m <= local_M; ++m)
        u_old[m] = phi((global_offset + m) * h);

    for (int k = 0; k < K; ++k) {
        double current_time = k * tau;

        double send_val = u_old[local_M];
        double recv_val = 0.0;

        MPI_Request req_send = {};
        MPI_Request req_recv = {};

        if (rank < size - 1)
            MPI_Isend(&send_val, 1, MPI_DOUBLE, rank + 1, 0, MPI_COMM_WORLD, &req_send);

        if (rank > 0)
            MPI_Irecv(&recv_val, 1, MPI_DOUBLE, rank - 1, 0, MPI_COMM_WORLD, &req_recv);

        if (rank > 0)        MPI_Wait(&req_recv, MPI_STATUS_IGNORE);
        if (rank < size - 1) MPI_Wait(&req_send, MPI_STATUS_IGNORE);

        if (rank == 0)
            u_old[0] = psi(current_time);
        else
            u_old[0] = recv_val;

        for (int m = 1; m <= local_M; ++m) {
            double x = (global_offset + m) * h;

            u_new[m] = u_old[m] - (tau / h) * (u_old[m] - u_old[m - 1]) + tau * f(x, current_time);
        }

        u_old = u_new;
    }

    collect_data(rank, size, M, local_M, T, h, u_old);

    MPI_Finalize();
    return 0;
}

void collect_data(int rank, int size, int M, int local_M, double T, double h, std::vector<double>& u_old) {
    std::vector<int> recvcounts(size);
    std::vector<int> displs(size);

    MPI_Gather(&local_M, 1, MPI_INT, recvcounts.data(), 1, MPI_INT, 0, MPI_COMM_WORLD);

    std::vector<double> global_u;

    if (rank == 0) {
        displs[0] = 0;
        for (int i = 1; i < size; ++i) {
            displs[i] = displs[i - 1] + recvcounts[i - 1];
        }

        global_u.resize(M);
    }

    // u_old[1] to skip unneded element
    MPI_Gatherv(&u_old[1], local_M, MPI_DOUBLE,
                global_u.data(), recvcounts.data(), displs.data(), MPI_DOUBLE,
                0, MPI_COMM_WORLD);

    if (rank == 0) {
        std::ofstream out("result.csv");
        if (out.is_open()) {
            out << "x,u\n";

            out << 0.0 << "," << psi(T) << "\n";

            for (int i = 0; i < M; ++i) {
                double x = (i + 1) * h;
                out << x << "," << global_u[i] << "\n";
            }

            out.close();
            std::cout << "Data saved to result.csv" << std::endl;
        } else {
            std::cerr << "Can't open file result.csv" << std::endl;
        }
    }

}
