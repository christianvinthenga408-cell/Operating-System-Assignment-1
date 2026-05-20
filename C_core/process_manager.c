#include "eduos.h"

typedef struct {
    int pid;
    int arrival;
    int burst;
    int priority;
} Process;
void run_process_manager() {
    printf("===== Process Manager =====\n");

    Process processes[5] = {
        {1, 0, 5, 3},
        {2, 1, 3, 1},
        {3, 2, 8, 4},
        {4, 3, 6, 2},
        {5, 4, 3, 5}
    };

    printf("PID\tArrival\tBurst\tPriority\n");

    for(int i = 0; i < 5; i++) {
        printf("%d\t%d\t%d\t%d\n",
               processes[i].pid,
               processes[i].arrival,
               processes[i].burst,
               processes[i].priority);
    }

    FILE *file = fopen("pcb_snapshot.json", "w");

    if(file != NULL) {
        fprintf(file, "[\n");

        for(int i = 0; i < 5; i++) {
            fprintf(file,
                "  {\"pid\": %d, \"arrival\": %d, \"burst\": %d, \"priority\": %d}",
                processes[i].pid,
                processes[i].arrival,
                processes[i].burst,
                processes[i].priority
            );

            if(i < 4)
                fprintf(file, ",");

            fprintf(file, "\n");
        }
        fprintf(file, "]\n");
        fclose(file);

        printf("\nPCB snapshot saved to pcb_snapshot.json\n");
    }
    else {
        printf("Error creating pcb_snapshot.json\n");
    }
}