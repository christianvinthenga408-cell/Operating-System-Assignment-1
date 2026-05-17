# ----------------------------------
# PROCESS CLASS
# ----------------------------------
class Process:
    def __init__(self, pid, arrival, burst, priority):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.priority = priority
        self.remaining = burst

ids = ["P1", "P2", "P3", "P4", "P5", "P6", "P7"]
processes = [
    Process(ids[0], 0, 5, 3),
    Process(ids[1], 1, 3, 1),
    Process(ids[2], 2, 8, 4),
    Process(ids[3], 3, 6, 2),
    Process(ids[4], 4, 3, 5),
    Process(ids[5], 5, 7, 3),
    Process(ids[6], 6, 2, 1),
]

def fcfs(process_list):
    print()
    print("===== FCFS Scheduling =====")

    plist = []

    for p in process_list:
        plist.append(Process(p.pid, p.arrival, p.burst, p.priority))

    plist.sort(key=lambda x: x.arrival)

    time = 0

    for p in plist:
        if time < p.arrival:
            time = p.arrival

        print(f"{p.pid} runs from {time} to {time + p.burst}")
        time += p.burst

def sjf(process_list):
    print()
    print("===== SJF Scheduling =====")
    plist = []

    for p in process_list:
        plist.append(Process(p.pid, p.arrival, p.burst, p.priority))

    completed = []
    time = 0

    while len(completed) < len(plist):

        ready = []

        for p in plist:
            if p.arrival <= time and p not in completed:
                ready.append(p)

        if len(ready) > 0:
            ready.sort(key=lambda x: x.burst)

            current = ready[0]
            print(f"{current.pid}, runs from {time} to {time + current.burst}")

            time += current.burst
            completed.append(current)

        else:
            time += 1

def priority_scheduling(process_list):
    print()
    print("===== Priority Scheduling =====")

    plist = []

    for p in process_list:
        plist.append(Process(p.pid, p.arrival, p.burst, p.priority))

    completed = []
    time = 0

    while len(completed) < len(plist):

        ready = []
        for p in plist:
            if p.arrival <= time and p not in completed:
                ready.append(p)

        if len(ready) > 0:
            ready.sort(key=lambda x: x.priority)

            current = ready[0]
            print(f"{current.pid} runs from {time} to {time + current.burst}, With Priority of {current.priority}")

            time += current.burst
            completed.append(current)

        else:
            time += 1

def priority_with_ageing(process_list):
    print()
    print("===== Priority Scheduling with Ageing =====")

    plist = []

    for p in process_list:
        plist.append(Process(p.pid, p.arrival, p.burst, p.priority))

    completed = []
    time = 0
    waiting = {}

    for p in plist:
        waiting[p.pid] = 0

    while len(completed) < len(plist):

        ready = []
        for p in plist:
            if p.arrival <= time and p not in completed:
                ready.append(p)

        if len(ready) > 0:

            for p in ready:
                waiting[p.pid] += 1

                if waiting[p.pid] % 3 == 0:
                    if p.priority > 1:
                        p.priority -= 1
                        print(f" {p.pid} aged -> New Priority = {p.priority}")

            ready.sort(key=lambda x: x.priority)
            current = ready[0]

            print(f"{current.pid} runs from {time}, to {time + current.burst},Priority = {current.priority}")

            time += current.burst
            completed.append(current)

        else:
            time += 1

def round_robin(process_list, quantum):
    print()
    print("===== Round Robin Scheduling =====")
    print(f"Time Quantum = {quantum}")

    plist = []

    for p in process_list:
        plist.append(Process(p.pid, p.arrival, p.burst, p.priority))

    plist.sort(key=lambda x: x.arrival)

    queue = []
    time = 0
    index = 0

    while True:

        # Add arrived processes
        while index < len(plist) and plist[index].arrival <= time:
            queue.append(plist[index])
            index += 1
        if len(queue) == 0:
            if index == len(plist):
                break
            time += 1
            continue

        current = queue.pop(0)

        run_time = min(quantum, current.remaining)

        print(f" {current.pid}, runs from , {time}, to , {time + run_time}")

        time += run_time
        current.remaining -= run_time

        while index < len(plist) and plist[index].arrival <= time:
            queue.append(plist[index])
            index += 1

        if current.remaining > 0:
            queue.append(current)

fcfs(processes)
sjf(processes)
priority_scheduling(processes)
priority_with_ageing(processes)
round_robin(processes, 2)