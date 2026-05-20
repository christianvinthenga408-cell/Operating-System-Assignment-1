CC = gcc

all:
	gcc main_sim.c process_manager.c thread_manager.c thread_manager_race.c thread_manager_fixed.c thread_pool.c ipc_module.c -o eduos -pthread

clean:
	del *.exe
	del *.o