#include "eduos.h"

int main()
{
    printf("===== EDUOS SIMULATION =====\n");

    run_process_manager();
    run_thread_manager();
    run_thread_manager_race();
    run_thread_manager_fixed();
    run_thread_pool();
    run_ipc_module();

    printf("\n===== Simulation Finished =====\n");
    return 0;
}