#include "eduos.h"
#include <stdio.h>

#define THREAD_POOL_SIZE 4
#define MAX_TASKS 10

int task_queue[MAX_TASKS];
int task_count = 0;

pthread_t workers[THREAD_POOL_SIZE];
pthread_mutex_t queue_mutex;
pthread_cond_t queue_cond;

int shutdown_pool = 0;
void* worker(void* arg)
{
    int id = *(int*)arg;
    while (1)
    {
        pthread_mutex_lock(&queue_mutex);
        while (task_count == 0 && !shutdown_pool)
        {
            pthread_cond_wait(&queue_cond, &queue_mutex);
        }
        if (shutdown_pool && task_count == 0)
        {
            pthread_mutex_unlock(&queue_mutex);
            printf("Worker %d exiting\n", id);
            break;
        }

        int task = task_queue[0];
        for (int i = 0; i < task_count - 1; i++)
        {
            task_queue[i] = task_queue[i + 1];
        }
        task_count--;
        pthread_mutex_unlock(&queue_mutex);
        printf("Worker %d processing task %d\n", id, task);
        Sleep(1000);
    }
    return NULL;
}
void add_task(int task)
{
    pthread_mutex_lock(&queue_mutex);
    if (task_count < MAX_TASKS)
    {
        task_queue[task_count] = task;
        task_count++;
        printf("Added task %d\n", task);
        pthread_cond_signal(&queue_cond);
    }
    pthread_mutex_unlock(&queue_mutex);
}

void run_thread_manager()
{
    printf("\n===== Thread Manager =====\n");
    int ids[THREAD_POOL_SIZE];

    pthread_mutex_init(&queue_mutex, NULL);
    pthread_cond_init(&queue_cond, NULL);

    for (int i = 0; i < THREAD_POOL_SIZE; i++)
    {
        ids[i] = i + 1;

        pthread_create(
            &workers[i],
            NULL,
            worker,
            &ids[i]
        );
    }
    for (int i = 1; i <= 8; i++)
    {
        add_task(i);
        Sleep(500);
    }
    pthread_mutex_lock(&queue_mutex);
    shutdown_pool = 1;
    pthread_mutex_unlock(&queue_mutex);
    pthread_cond_broadcast(&queue_cond);

    for (int i = 0; i < THREAD_POOL_SIZE; i++)
    {
        pthread_join(workers[i], NULL);
    }
    pthread_mutex_destroy(&queue_mutex);
    pthread_cond_destroy(&queue_cond);
    printf("Thread manager finished\n");
}