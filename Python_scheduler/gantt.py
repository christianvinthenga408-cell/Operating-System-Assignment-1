import os
import csv
import json
import copy
import argparse
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from tabulate import tabulate

os.makedirs("../Documents/screenshots", exist_ok=True)

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
            process_list.append(
                Process(int(row["pid"]),int(row["arrival"]),int(row["burst"]),int(row["priority"])))

    return process_list

def load_json(filename):
    process_list = []

    with open(filename, "r") as file:
        data = json.load(file)

    for row in data:
        process_list.append(Process(int(row["pid"]),int(row["arrival"]),int(row["burst"]),int(row["priority"])))

    return process_list

def finalize(process_list):
    for p in process_list:
        p.turnaround = p.completion - p.arrival
        p.waiting = p.turnaround - p.burst

def get_summary(process_list):
    n = len(process_list)

    avg_wt = sum(p.waiting for p in process_list) / n
    avg_tat = sum(p.turnaround for p in process_list) / n
    finish = max(p.completion for p in process_list)
    total_burst = sum(p.burst for p in process_list)

    cpu = (total_burst / finish) * 100

    return avg_wt, avg_tat, cpu

def fcfs(original):
    plist = copy.deepcopy(original)

    plist.sort(key=lambda x: (x.arrival, x.pid))

    gantt = []
    time = 0

    for p in plist:

        if time < p.arrival:
            gantt.append(("Idle", time, p.arrival - time))
            time = p.arrival

        gantt.append((f"P{p.pid}", time, p.burst))

        p.response = time - p.arrival
        time += p.burst
        p.completion = time

    finalize(plist)
    return plist, gantt

def sjf(original):
    plist = copy.deepcopy(original)

    completed = []
    gantt = []
    time = 0

    while len(completed) < len(plist):

        ready = [
            p for p in plist
            if p.arrival <= time
            and p not in completed
        ]

        if ready:
            ready.sort(key=lambda x:(x.burst, x.arrival, x.pid))
            p = ready[0]

            gantt.append((f"P{p.pid}", time, p.burst))

            p.response = time - p.arrival
            time += p.burst
            p.completion = time

            completed.append(p)

        else:
            gantt.append(("Idle", time, 1))
            time += 1

    finalize(plist)
    return plist, gantt

def priority_sched(original):
    plist = copy.deepcopy(original)

    completed = []
    gantt = []
    time = 0

    while len(completed) < len(plist):

        ready = [
            p for p in plist
            if p.arrival <= time
            and p not in completed
        ]

        if ready:
            ready.sort(key=lambda x:(x.priority, x.arrival, x.pid))

            p = ready[0]

            gantt.append((f"P{p.pid}", time, p.burst))

            p.response = time - p.arrival
            time += p.burst
            p.completion = time

            completed.append(p)

        else:
            gantt.append(("Idle", time, 1))
            time += 1

    finalize(plist)
    return plist, gantt

def priority_ageing(original):
    plist = copy.deepcopy(original)

    completed = []
    gantt = []
    time = 0
    wait = {}

    for p in plist:
        wait[p.pid] = 0

    while len(completed) < len(plist):

        ready = [
            p for p in plist
            if p.arrival <= time
            and p not in completed
        ]

        if ready:

            for p in ready:
                wait[p.pid] += 1

                if wait[p.pid] % 3 == 0:
                    if p.priority > 1:
                        p.priority -= 1

            ready.sort(key=lambda x:(x.priority, x.arrival, x.pid))

            p = ready[0]

            gantt.append((f"P{p.pid}", time, p.burst))

            p.response = time - p.arrival
            time += p.burst
            p.completion = time
            completed.append(p)

        else:
            gantt.append(("Idle", time, 1))
            time += 1

    finalize(plist)
    return plist, gantt

def round_robin(original, quantum=2):
    plist = copy.deepcopy(original)

    plist.sort(key=lambda x: x.arrival)

    queue = []
    gantt = []

    time = 0
    index = 0

    while True:

        while index < len(plist) and plist[index].arrival <= time:
            queue.append(plist[index])
            index += 1

        if not queue:
            if index == len(plist):
                break

            gantt.append(("Idle", time, 1))
            time += 1
            continue

        p = queue.pop(0)

        if p.response == -1:
            p.response = time - p.arrival

        run = min(quantum,p.remaining)
        gantt.append((f"P{p.pid}", time, run))

        time += run
        p.remaining -= run

        while index < len(plist) and plist[index].arrival <= time:
            queue.append(plist[index])
            index += 1

        if p.remaining > 0:
            queue.append(p)
        else:
            p.completion = time

    finalize(plist)
    return plist, gantt

def draw_gantt(gantt, title, filename):
    plt.figure(figsize=(10, 2))

    colors = {"Idle": "gray",
        "P1": "skyblue",
        "P2": "lightgreen",
        "P3": "salmon",
        "P4": "gold",
        "P5": "plum",
        "P6": "orange",
        "P7": "cyan",
        "P8": "pink",
        "P9": "khaki",
        "P10": "lightcoral"
    }
    y = 10

    for label, start, duration in gantt:

        color = colors.get(label, "lightblue")
        plt.broken_barh([(start, duration)],(y, 8),facecolors=color,edgecolors="black")

        plt.text(start + duration / 2,y + 4,label,ha="center",va="center")

    max_time = max(start + dur for _, start, dur in gantt)

    plt.xticks(range(0, max_time + 1))
    plt.yticks([])
    plt.title(title)
    plt.xlabel("Time")
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(f"../Documents/screenshots/{filename}.png")

    plt.close()

# ==========================================
# TIMELINE ANIMATION
# Saves animated GIF
# ==========================================
def animate_gantt(gantt, title, filename):
    fig, ax = plt.subplots(figsize=(10, 2))

    colors = {
        "Idle": "gray",
        "P1": "skyblue",
        "P2": "lightgreen",
        "P3": "salmon",
        "P4": "gold",
        "P5": "plum",
        "P6": "orange",
        "P7": "cyan",
        "P8": "pink",
        "P9": "khaki",
        "P10": "lightcoral"
    }

    max_time = max(
        start + dur
        for _, start, dur in gantt
    )

    def update(frame):
        ax.clear()

        for label, start, duration in gantt:

            # only show completed timeline
            if start < frame:
                visible_duration = min(
                    duration,
                    frame - start
                )

                ax.broken_barh(
                    [(start, visible_duration)],
                    (10, 8),
                    facecolors=colors.get(
                        label,
                        "lightblue"
                    ),
                    edgecolors="black"
                )

                ax.text(
                    start + visible_duration / 2,
                    14,
                    label,
                    ha="center",
                    va="center",
                    fontsize=8
                )

        ax.set_xlim(0, max_time)
        ax.set_ylim(5, 20)

        ax.set_xticks(
            range(0, max_time + 1)
        )

        ax.set_yticks([])

        ax.set_title(
            title + " Animation"
        )

        ax.set_xlabel("Time")

        ax.grid(True)
        return ax.patches

    anim = FuncAnimation(
        fig,
        update,
        frames=max_time + 1,
        interval=700,
        repeat=False
    )

    anim.save(f"../Documents/screenshots/{filename}.gif",writer="pillow")

    plt.close()

def comparison_chart(names, values, label, filename):
    plt.figure(figsize=(6, 4))
    plt.bar(names, values)

    plt.ylabel(label)
    plt.title(label)
    plt.tight_layout()
    plt.savefig(f"../Documents/screenshots/{filename}.png")

    plt.close()

parser = argparse.ArgumentParser()
parser.add_argument("--file")

args = parser.parse_args()

if not args.file:
    print("Use --file")
    exit()

if args.file.endswith(".csv"):
    processes = load_csv(args.file)
else:
    processes = load_json(args.file)

fcfs_data, fcfs_gantt = fcfs(processes)
sjf_data, sjf_gantt = sjf(processes)
priority_data, priority_gantt = priority_sched(processes)
age_data, age_gantt = priority_ageing(processes)
rr_data, rr_gantt = round_robin(processes, 2)

draw_gantt(fcfs_gantt, "FCFS", "fcfs_gantt")
draw_gantt(sjf_gantt, "SJF", "sjf_gantt")
draw_gantt(priority_gantt, "Priority", "priority_gantt")
draw_gantt(age_gantt,"Priority with Ageing","priority_ageing_gantt")
draw_gantt(rr_gantt,"Round Robin","round_robin_gantt")

animate_gantt(fcfs_gantt,"FCFS","fcfs_animation")
animate_gantt(sjf_gantt,"SJF","sjf_animation")
animate_gantt(priority_gantt,"Priority","priority_animation")
animate_gantt(age_gantt,"Priority with Ageing","priority_ageing_animation")
animate_gantt(rr_gantt,"Round Robin","round_robin_animation")

fcfs_wt, fcfs_tat, fcfs_cpu = get_summary(fcfs_data)
sjf_wt, sjf_tat, sjf_cpu = get_summary(sjf_data)
pri_wt, pri_tat, pri_cpu = get_summary(priority_data)
age_wt, age_tat, age_cpu = get_summary(age_data)
rr_wt, rr_tat, rr_cpu = get_summary(rr_data)

alg_names = ["FCFS","SJF","Priority","Priority+Age","RR"]
comparison_chart(
    alg_names,
    [fcfs_wt, sjf_wt, pri_wt, age_wt, rr_wt],
    "Average Waiting Time",
    "compare_wt"
)
comparison_chart(
    alg_names,
    [fcfs_tat, sjf_tat, pri_tat, age_tat, rr_tat],
    "Average Turnaround Time",
    "compare_tat"
)
comparison_chart(
    alg_names,
    [fcfs_cpu, sjf_cpu, pri_cpu, age_cpu, rr_cpu],
    "CPU Utilization (%)",
    "compare_cpu"
)
table = [
    ["FCFS", fcfs_wt, fcfs_tat, fcfs_cpu],
    ["SJF", sjf_wt, sjf_tat, sjf_cpu],
    ["Priority", pri_wt, pri_tat, pri_cpu],
    ["Priority+Age", age_wt, age_tat, age_cpu],
    ["RR", rr_wt, rr_tat, rr_cpu]
]
print()
print(tabulate(table,headers=["Algorithm","Avg WT","Avg TAT","CPU %"],tablefmt="grid"))
print("\nSaved images in Documents/screenshots/")