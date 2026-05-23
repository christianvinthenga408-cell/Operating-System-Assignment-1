import argparse
import random
import csv
import json
import copy

class Process:
    def __init__(self, pid, arrival, burst, prio):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.priority = prio
        self.remaining = burst
        self.completion = 0
        self.turnaround = 0
        self.waiting = 0
        self.response = -1

def load_csv(filename):
    process_list = []

    with open(filename, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            process_list.append(Process(int(row["pid"]),int(row["arrival"]),int(row["burst"]),int(row["priority"])))

    return process_list
def load_json(filename):
    process_list = []

    with open(filename, "r") as file:
        data = json.load(file)

    for row in data:
        process_list.append(Process(int(row["pid"]),int(row["arrival"]),int(row["burst"]),int(row["priority"])))

    return process_list

def generate_random(n, seed):
    random.seed(seed)

    process_list = []

    for i in range(n):
        arrival = random.randint(0, 10)
        burst = random.randint(1, 10)
        prio = random.randint(1, 5)
        processes.append(Process(i + 1,arrival,burst,prio))

    return process_list

def finalize_metrics(process_list):
    for p in process_list:
        p.turnaround = p.completion - p.arrival
        p.waiting = p.turnaround - p.burst

def print_results(name, process_list):
    print("\n==============================")
    print(name)
    print("==============================")

    print("PID  Arr  Burst  Comp  TAT  WT  RT")

    total_wt = 0
    total_tat = 0
    total_rt = 0
    total_burst = 0

    finish_time = max(p.completion for p in process_list)

    for p in sorted(process_list, key=lambda x: x.pid):
        print(f"{p.pid:<4}"f"{p.arrival:<5}"f"{p.burst:<7}"f"{p.completion:<6}"f"{p.turnaround:<5}"f"{p.waiting:<4}"f"{p.response:<4}")

        total_wt += p.waiting
        total_tat += p.turnaround
        total_rt += p.response
        total_burst += p.burst

    n = len(process_list)

    avg_wt = total_wt / n
    avg_tat = total_tat / n
    avg_rt = total_rt / n

    cpu = (total_burst / finish_time) * 100
    throughput = n / finish_time

    print("\n--- Aggregate ---")
    print("Average WT:", round(avg_wt, 2))
    print("Average TAT:", round(avg_tat, 2))
    print("Average RT:", round(avg_rt, 2))
    print("CPU Utilization:", round(cpu, 2), "%")
    print("Throughput:", round(throughput, 2))

def fcfs(original):
    plist = copy.deepcopy(original)

    plist.sort(key=lambda x: (x.arrival, x.pid))

    time = 0

    for p in plist:
        if time < p.arrival:
            time = p.arrival

        p.response = time - p.arrival
        time += p.burst
        p.completion = time

    finalize_metrics(plist)
    print_results("FCFS", plist)

def sjf(original):
    plist = copy.deepcopy(original)

    completed = []
    time = 0

    while len(completed) < len(plist):

        ready = [
            p for p in plist
            if p.arrival <= time and p not in completed
        ]

        if ready:
            ready.sort(key=lambda x:(x.burst, x.arrival, x.pid))
            p = ready[0]

            p.response = time - p.arrival
            time += p.burst
            p.completion = time

            completed.append(p)

        else:
            time += 1

    finalize_metrics(plist)
    print_results("SJF", plist)

def priority(original):
    plist = copy.deepcopy(original)

    completed = []
    time = 0

    while len(completed) < len(plist):
        ready = [
            p for p in plist
            if p.arrival <= time and p not in completed
        ]
        if ready:
            # Lower priority number = higher urgency
            ready.sort(key=lambda x:(x.priority, x.arrival, x.pid))
            p = ready[0]

            p.response = time - p.arrival
            time += p.burst
            p.completion = time

            completed.append(p)

        else:
            time += 1

    finalize_metrics(plist)
    print_results("Priority", plist)

def priority_sched(original):
    plist = copy.deepcopy(original)

    completed = []
    time = 0
    wait = {}

    for p in plist:
        wait[p.pid] = 0

    while len(completed) < len(plist):

        ready = [
            p for p in plist
            if p.arrival <= time and p not in completed
        ]

        if ready:
            for p in ready:
                wait[p.pid] += 1

                if wait[p.pid] % 3 == 0:
                    if p.priority > 1:
                        p.priority -= 1

            ready.sort(key=lambda x:(x.priority, x.arrival, x.pid))
            p = ready[0]

            p.response = time - p.arrival
            time += p.burst
            p.completion = time

            completed.append(p)

        else:
            time += 1

    finalize_metrics(plist)
    print_results("Priority + Ageing", plist)

def round_robin(original, quantum):
    plist = copy.deepcopy(original)

    plist.sort(key=lambda x: x.arrival)

    queue = []
    time = 0
    index = 0

    while True:

        while index < len(plist) and plist[index].arrival <= time:
            queue.append(plist[index])
            index += 1

        if not queue:
            if index == len(plist):
                break

            time += 1
            continue

        p = queue.pop(0)

        if p.response == -1:
            p.response = time - p.arrival

        run = min(quantum, p.remaining)

        time += run
        p.remaining -= run

        while index < len(plist) and plist[index].arrival <= time:
            queue.append(plist[index])
            index += 1

        if p.remaining > 0:
            queue.append(p)
        else:
            p.completion = time

    finalize_metrics(plist)
    print_results(f"Round Robin (Q={quantum})",plist)

parser = argparse.ArgumentParser()

parser.add_argument("--random", type=int)
parser.add_argument("--seed", type=int, default=1)
parser.add_argument("--file")
parser.add_argument("--quantum", type=int, default=2)

args = parser.parse_args()

if args.random:
    processes = generate_random(args.random,args.seed)

elif args.file:
    if args.file.endswith(".csv"):
        processes = load_csv(args.file)
    else:
        processes = load_json(args.file)
else:
    print("Use --random or --file")
    exit()

fcfs(processes)
sjf(processes)
priority(processes)
priority_sched(processes)
round_robin(processes, args.quantum)