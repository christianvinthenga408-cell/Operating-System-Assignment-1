#ifndef EDUOS_H
#define EDUOS_H

/* Standard libraries */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Threading */
#include <pthread.h>

/* Windows-specific functions */
#include <windows.h>


/* =====================================
   SHARED PCB STRUCTURE
===================================== */
typedef struct
{
    int pid;
    int burst_time;
} PCB;


/* =====================================
   FUNCTION DECLARATIONS
===================================== */

/* Process manager */
void run_process_manager();

/* Basic thread manager */
void run_thread_manager();

/* Race condition demo */
void run_thread_manager_race();

/* Fixed race condition (mutex) */
void run_thread_manager_fixed();

/* Thread pool */
void run_thread_pool();

/* IPC module */
void run_ipc_module();

#endif