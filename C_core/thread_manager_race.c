#include "eduos.h"

int race_counter = 0;

void* race_increment(void* arg)
{
    for(int i = 0; i < 100000; i++)
    {
        race_counter++;
    }
    return NULL;
}
void run_thread_manager_race()
{
    printf("\n===== Thread Manager (Race Condition) =====\n");

    pthread_t t1, t2;

    race_counter = 0;
    pthread_create(&t1, NULL, race_increment, NULL);
    pthread_create(&t2, NULL, race_increment, NULL);

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    printf("Final counter = %d\n", race_counter);
}