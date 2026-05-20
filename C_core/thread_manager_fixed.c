#include "eduos.h"

int fixed_counter = 0;
pthread_mutex_t counter_lock;

void* fixed_increment(void* arg)
{
    for(int i = 0; i < 100000; i++)
    {
        pthread_mutex_lock(&counter_lock);
        fixed_counter++;
        pthread_mutex_unlock(&counter_lock);
    }
    return NULL;
}

void run_thread_manager_fixed()
{
    printf("\n===== Thread Manager (Fixed with Mutex) =====\n");

    pthread_t t1, t2;
    fixed_counter = 0;
    pthread_mutex_init(&counter_lock, NULL);
    pthread_create(&t1, NULL, fixed_increment, NULL);
    pthread_create(&t2, NULL, fixed_increment, NULL);

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    pthread_mutex_destroy(&counter_lock);
    printf("Final counter = %d\n", fixed_counter);
}