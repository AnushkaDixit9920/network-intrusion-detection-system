from collections import deque

# ---------------- Process Class ----------------
class Process:
    def __init__(self, pid, arrival, burst):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst


# ---------------- Input ----------------
def take_input():
    n = int(input("Enter number of processes: "))
    processes = []

    for i in range(n):
        at = int(input(f"Arrival time of P{i+1}: "))
        bt = int(input(f"Burst time of P{i+1}: "))
        processes.append(Process(f"P{i+1}", at, bt))

    return processes


# ---------------- Gantt Chart ----------------
def print_gantt_chart(chart):
    print("\nGantt Chart:")
    for p in chart:
        print(f"| {p} ", end="")
    print("|")


# ---------------- FCFS ----------------
def fcfs(processes):
    processes.sort(key=lambda x: x.arrival)
    time = 0
    waiting_times = []
    turnaround_times = []
    chart = []

    for p in processes:
        if time < p.arrival:
            time = p.arrival

        waiting = time - p.arrival
        turnaround = waiting + p.burst

        waiting_times.append(waiting)
        turnaround_times.append(turnaround)

        chart.append(p.pid)
        time += p.burst

    print_gantt_chart(chart)

    return (sum(waiting_times)/len(processes),
            sum(turnaround_times)/len(processes))


# ---------------- SJF ----------------
def sjf(processes):
    time = 0
    waiting_times = []
    turnaround_times = []
    ready = []
    chart = []

    processes = sorted(processes, key=lambda x: x.arrival)

    while processes or ready:
        while processes and processes[0].arrival <= time:
            ready.append(processes.pop(0))

        if ready:
            ready.sort(key=lambda x: x.burst)
            p = ready.pop(0)

            waiting = time - p.arrival
            turnaround = waiting + p.burst

            waiting_times.append(waiting)
            turnaround_times.append(turnaround)

            chart.append(p.pid)
            time += p.burst
        else:
            time += 1

    print_gantt_chart(chart)

    return (sum(waiting_times)/len(waiting_times),
            sum(turnaround_times)/len(turnaround_times))


# ---------------- Round Robin ----------------
def round_robin(processes, quantum):
    queue = deque(processes)
    time = 0

    remaining = {p.pid: p.burst for p in processes}
    waiting = {p.pid: 0 for p in processes}
    turnaround = {p.pid: 0 for p in processes}
    last_exec = {p.pid: 0 for p in processes}

    chart = []

    while queue:
        p = queue.popleft()

        if time < p.arrival:
            time = p.arrival

        waiting[p.pid] += time - last_exec[p.pid]

        exec_time = min(quantum, remaining[p.pid])
        time += exec_time
        remaining[p.pid] -= exec_time

        chart.append(p.pid)

        last_exec[p.pid] = time

        if remaining[p.pid] > 0:
            queue.append(p)
        else:
            turnaround[p.pid] = time - p.arrival

    print_gantt_chart(chart)

    avg_wait = sum(waiting.values()) / len(processes)
    avg_turn = sum(turnaround.values()) / len(processes)

    return avg_wait, avg_turn


# ---------------- MAIN ----------------
if __name__ == "__main__":
    processes = take_input()

    print("\n--- FCFS ---")
    w, t = fcfs(processes.copy())
    print(f"Average Waiting Time: {round(w,2)}")
    print(f"Average Turnaround Time: {round(t,2)}")

    print("\n--- SJF ---")
    w, t = sjf(processes.copy())
    print(f"Average Waiting Time: {round(w,2)}")
    print(f"Average Turnaround Time: {round(t,2)}")

    quantum = int(input("\nEnter time quantum for Round Robin: "))
    print("\n--- Round Robin ---")
    w, t = round_robin(processes.copy(), quantum)
    print(f"Average Waiting Time: {round(w,2)}")
    print(f"Average Turnaround Time: {round(t,2)}")