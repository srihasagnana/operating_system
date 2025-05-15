def fcfs_cpu_scheduling(processes, burst_times):
    n = len(processes)
    waiting_time = [0]*n
    turnaround_time = [0]*n

    for i in range(1, n):
        waiting_time[i] = burst_times[i-1] + waiting_time[i-1]
    for i in range(n):
        turnaround_time[i] = burst_times[i] + waiting_time[i]

    print("\nProcess\tBurst Time\tWaiting Time\tTurnaround Time")
    for i in range(n):
        print(f"{processes[i]}\t{burst_times[i]}\t\t{waiting_time[i]}\t\t{turnaround_time[i]}")

def bankers_algorithm(available, max_demand, allocation):
    n = len(allocation)    # number of processes
    m = len(available)     # number of resources

    need = [[max_demand[i][j] - allocation[i][j] for j in range(m)] for i in range(n)]

    finish = [False]*n
    safe_sequence = []

    work = available[:]

    while len(safe_sequence) < n:
        allocated_in_this_loop = False
        for i in range(n):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(m)):
                for j in range(m):
                    work[j] += allocation[i][j]
                safe_sequence.append(i)
                finish[i] = True
                allocated_in_this_loop = True
        if not allocated_in_this_loop:
            break

    if len(safe_sequence) == n:
        print("System is in a safe state.")
        print("Safe sequence:", ' -> '.join([f"P{p}" for p in safe_sequence]))
    else:
        print("System is NOT in a safe state.")

def fifo_page_replacement(pages, frame_size):
    frames = []
    page_faults = 0
    for page in pages:
        if page not in frames:
            if len(frames) < frame_size:
                frames.append(page)
            else:
                frames.pop(0)
                frames.append(page)
            page_faults += 1
        print(f"Frames: {frames}")
    print(f"Total page faults: {page_faults}")

def fcfs_disk_scheduling(requests, head):
    seek_sequence = []
    seek_count = 0
    distance = 0
    current_track = head

    for track in requests:
        seek_sequence.append(track)
        distance = abs(track - current_track)
        seek_count += distance
        current_track = track

    print("Seek Sequence:", seek_sequence)
    print("Total seek operations:", seek_count)

def cpu_scheduling_menu():
    print("\nCPU Scheduling - FCFS")
    n = int(input("Enter number of processes: "))
    processes = [f"P{i+1}" for i in range(n)]
    burst_times = list(map(int, input(f"Enter burst times for {n} processes (space separated): ").split()))
    fcfs_cpu_scheduling(processes, burst_times)

def bankers_menu():
    print("\nBanker's Algorithm - Deadlock Avoidance")
    n = int(input("Enter number of processes: "))
    m = int(input("Enter number of resource types: "))
    print("Enter Available Resources (space separated): ")
    available = list(map(int, input().split()))
    print("Enter Max demand matrix:")
    max_demand = [list(map(int, input().split())) for _ in range(n)]
    print("Enter Allocation matrix:")
    allocation = [list(map(int, input().split())) for _ in range(n)]
    bankers_algorithm(available, max_demand, allocation)

def paging_menu():
    print("\nPaging - FIFO Page Replacement")
    pages = list(map(int, input("Enter page reference string (space separated): ").split()))
    frame_size = int(input("Enter number of frames: "))
    fifo_page_replacement(pages, frame_size)

def disk_scheduling_menu():
    print("\nDisk Scheduling - FCFS")
    head = int(input("Enter initial head position: "))
    requests = list(map(int, input("Enter disk queue requests (space separated): ").split()))
    fcfs_disk_scheduling(requests, head)

def main_menu():
    while True:
        print("\nOS Simulation Menu")
        print("1. CPU Scheduling (FCFS)")
        print("2. Banker's Algorithm (Deadlock Avoidance)")
        print("3. Paging (FIFO Page Replacement)")
        print("4. Disk Scheduling (FCFS)")
        print("0. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            cpu_scheduling_menu()
        elif choice == '2':
            bankers_menu()
        elif choice == '3':
            paging_menu()
        elif choice == '4':
            disk_scheduling_menu()
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main_menu()
