#include "eduos.h"
#include <stdio.h>

#define THREAD_POOL_SIZE 4
#define MAX_TASKS 10

int pool_task_queue[MAX_TASKS];
int pool_task_count = 0;
pthread_t pool_workers[THREAD_POOL_SIZE];
pthread_mutex_t pool_queue_mutex;
pthread_cond_t pool_queue_cond;

int pool_shutdown = 0;

void* pool_worker(void* arg)
{
    int id = *(int*)arg;

    while (1)
    {
        pthread_mutex_lock(&pool_queue_mutex);
        while (pool_task_count == 0 && !pool_shutdown)
        {
            pthread_cond_wait(
                &pool_queue_cond,
                &pool_queue_mutex
            );
        }
        if (pool_shutdown && pool_task_count == 0)
        {
            pthread_mutex_unlock(&pool_queue_mutex);
            printf("Pool Worker %d exiting\n", id);
            break;
        }
        int task = pool_task_queue[0];

        for (int i = 0; i < pool_task_count - 1; i++)
        {
            pool_task_queue[i] = pool_task_queue[i + 1];
        }
        pool_task_count--;
        pthread_mutex_unlock(&pool_queue_mutex);
        printf("Pool Worker %d processing task %d\n", id, task);
        Sleep(1000);
    }
    return NULL;
}

void add_pool_task(int task)
{
    pthread_mutex_lock(&pool_queue_mutex);
    if (pool_task_count < MAX_TASKS)
    {
        pool_task_queue[pool_task_count] = task;
        pool_task_count++;
        printf("Added task %d\n", task);
        pthread_cond_signal(&pool_queue_cond);
    }
    pthread_mutex_unlock(&pool_queue_mutex);
}

void run_thread_pool()
{
    printf("\n===== Thread Pool =====\n");
    int ids[THREAD_POOL_SIZE];
    pthread_mutex_init(&pool_queue_mutex, NULL);
    pthread_cond_init(&pool_queue_cond, NULL);

    for (int i = 0; i < THREAD_POOL_SIZE; i++)
    {
        ids[i] = i + 1;
        pthread_create( &pool_workers[i],NULL,pool_worker, &ids[i]
        );
    }

    for (int i = 1; i <= 8; i++)
    {
        add_pool_task(i);
        Sleep(500);
    }

    pthread_mutex_lock(&pool_queue_mutex);
    pool_shutdown = 1;
    pthread_mutex_unlock(&pool_queue_mutex);
    pthread_cond_broadcast(&pool_queue_cond);

    for (int i = 0; i < THREAD_POOL_SIZE; i++)
    {
        pthread_join(pool_workers[i], NULL);
    }

    pthread_mutex_destroy(&pool_queue_mutex);
    pthread_cond_destroy(&pool_queue_cond);
    printf("Thread pool finished\n");
}