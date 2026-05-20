#include "eduos.h"

typedef struct {
    int pid;
    int burst_time;
} SharedData;

void run_ipc_module()
{
    printf("\n===== IPC Module =====\n");

    HANDLE hMapFile;
    HANDLE hMutex;
    SharedData *data;

    hMapFile = CreateFileMapping(
        INVALID_HANDLE_VALUE,
        NULL,
        PAGE_READWRITE,
        0,
        sizeof(SharedData),
        "MySharedMemory"
    );

    data = (SharedData*) MapViewOfFile(
        hMapFile,
        FILE_MAP_ALL_ACCESS,
        0,
        0,
        sizeof(SharedData)
    );

    hMutex = CreateMutex(NULL, FALSE, "MyMutex");

    WaitForSingleObject(hMutex, INFINITE);

    data->pid = 101;
    data->burst_time = 5;

    printf("Shared Memory Written:\n");
    printf("PID = %d\n", data->pid);
    printf("Burst Time = %d\n", data->burst_time);

    ReleaseMutex(hMutex);

    WaitForSingleObject(hMutex, INFINITE);

    printf("Shared Memory Read:\n");
    printf("PID = %d\n", data->pid);
    printf("Burst Time = %d\n", data->burst_time);

    ReleaseMutex(hMutex);

    HANDLE readPipe, writePipe;
    SECURITY_ATTRIBUTES sa;

    char buffer[100];
    DWORD bytesRead, bytesWritten;

    sa.nLength = sizeof(SECURITY_ATTRIBUTES);
    sa.lpSecurityDescriptor = NULL;
    sa.bInheritHandle = TRUE;

    CreatePipe(&readPipe, &writePipe, &sa, 0);

    char message[] = "202,8";

    WriteFile(
        writePipe,
        message,
        strlen(message) + 1,
        &bytesWritten,
        NULL
    );

    ReadFile(
        readPipe,
        buffer,
        sizeof(buffer),
        &bytesRead,
        NULL
    );

    int pcb_pid, pcb_burst;

    sscanf(buffer, "%d,%d", &pcb_pid, &pcb_burst);

    printf("\nPipe Data Received:\n");
    printf("PID = %d\n", pcb_pid);
    printf("Burst Time = %d\n", pcb_burst);

    CloseHandle(readPipe);
    CloseHandle(writePipe);
    UnmapViewOfFile(data);
    CloseHandle(hMapFile);
    CloseHandle(hMutex);

    printf("IPC module finished\n");
}