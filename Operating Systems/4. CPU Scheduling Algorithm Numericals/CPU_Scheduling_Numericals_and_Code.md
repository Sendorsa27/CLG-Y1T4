# CPU Scheduling - Numericals & Code Reference

## 1. Core Terminology & Formulas

| Term | Full Form | Definition |
|------|-----------|------------|
| AT | Arrival Time | When the process enters the ready queue |
| BT | Burst Time | Total CPU time needed by the process |
| CT | Completion Time | When the process finishes execution |
| TAT | Turnaround Time | Total time spent in the system (waiting + running) |
| WT | Waiting Time | Time spent waiting in the ready queue |

### Key Formulas

```
TAT = CT - AT
WT  = TAT - BT  →  WT = CT - AT - BT
```

**Average TAT** = Sum of all TAT / number of processes
**Average WT** = Sum of all WT / number of processes

---

## 2. Assumptions (Stated in Class)

- **Priority scheduling**: Higher number = higher priority
- **Tie-breaking** (same priority): earlier arrival time first
- **Tie-breaking** (same priority): earlier arrival time first
- **Tie-breaking** (same priority + same arrival): smaller PID first
- **FCFS** is **non-preemptive**
- **SJF (non-preemptive)**: assumes all processes are already present at time 0; picks the one with the smallest BT first
- **Round Robin**: time quantum = 2 (typical, but check the question)
- **Round Robin** uses a **queue (FIFO)** data structure to manage the ready processes

---

### Gantt Chart

A visual representation of process scheduling that shows the **execution order** and **timeline** of each process on the CPU. It helps track which process runs at what time and is used to compute CT, TAT, and WT.

**Example:**
```
|  P1  |   P2   |   P3   |
0------4-------7-------9
```

---

## 2.5 Process Creation

A process is represented by a **class/struct** that holds all attributes needed for scheduling calculations:

| Attribute | Description |
|-----------|-------------|
| PID | Process ID (identifier) |
| AT | Arrival Time — when the process enters the ready queue |
| BT | Burst Time — total CPU time required |
| CT | Completion Time — when the process finishes |
| TAT | Turnaround Time — CT - AT |
| WT | Waiting Time — TAT - BT |

- A **constructor** instantiates and initializes these attributes for each process.
- All scheduling algorithms build on this same process structure (some add extra fields like `Priority` or `remainingBT`).

---

## 3. FCFS - First Come First Serve

### Concept
- Non-preemptive: once a process starts, it runs to completion
- Solve using a **Gantt chart**, then compute TAT and WT

### Solved Example 1

**Processes:** P1 (AT=0, BT=4), P2 (AT=1, BT=3), P3 (AT=2, BT=2)

**Gantt Chart:**
```
|  P1  |   P2   |   P3   |
0------4-------7-------9
```

| Process | AT | BT | CT | TAT (CT-AT) | WT (TAT-BT) |
|---------|----|----|----|-------------|-------------|
| P1 | 0 | 4 | 4 | 4 | 0 |
| P2 | 1 | 3 | 7 | 6 | 3 |
| P3 | 2 | 2 | 9 | 7 | 5 |
| **Avg** | - | - | - | **5.67** | **2.67** |

### Solved Example 2

**Processes:** P1 (AT=0, BT=5), P2 (AT=2, BT=4), P3 (AT=3, BT=1)

**Gantt Chart:**
```
|  P1  |   P2   | P3 |
0------5-------9----10
```

| Process | AT | BT | CT | TAT | WT |
|---------|----|----|----|-----|----|
| P1 | 0 | 5 | 5 | 5 | 0 |
| P2 | 2 | 4 | 9 | 7 | 3 |
| P3 | 3 | 1 | 10 | 7 | 6 |
| **Avg** | - | - | - | **6.33** | **3.0** |

---

## 4. Priority Scheduling

### Assumption
- Higher priority number = higher priority (e.g., priority 5 > priority 3)

### Non-Preemptive Example

**Processes:** P1 (AT=0, BT=5, Pri=3), P2 (AT=4, BT=4, Pri=1), P3 (AT=2, BT=3, Pri=2)

**Gantt Chart:**
```
|  P1  |   P3   |   P2   |
0------5-------8-------12
```
- At time 0: P1 arrives (only option), runs to completion (BT=5)
- At time 5: P2 and P3 have arrived. P3 has higher priority (2 > 1), runs next (BT=3)
- At time 8: P2 runs to completion (BT=4)

| Process | AT | BT | Priority | CT | TAT | WT |
|---------|----|----|----------|----|-----|----|
| P1 | 0 | 5 | 3 | 5 | 5 | 0 |
| P2 | 4 | 4 | 1 | 12 | 8 | 4 |
| P3 | 2 | 3 | 2 | 8 | 6 | 3 |

### Preemptive Example

**Processes:** P1 (AT=0, BT=5, Pri=2), P2 (AT=4, BT=4, Pri=1), P3 (AT=2, BT=5, Pri=3), P4 (AT=6, BT=2, Pri=2)

**Gantt Chart:**
```
|  P1  |  P3  |  P1  | P4 |  P2  |
0------2------7-----11--13---17
```

- **t=0**: P1 arrives (only option, Pri=2), runs for 2 units (BT remaining = 3)
- **t=2**: P3 arrives (Pri=3, highest), preempts P1. P3 runs to completion (BT=5)
- **t=7**: P1 (Pri=2) and P4 (Pri=2) tied. Same priority → check arrival. P1 arrived at 0, P4 at 6 → P1 runs (BT remaining = 1)
- **t=11**: P4 runs to completion (BT=2)
- **t=13**: P2 runs to completion (BT=4)

| Process | AT | BT | Priority | CT | TAT | WT |
|---------|----|----|----------|----|-----|----|
| P1 | 0 | 5 | 2 | 11 | 11 | 6 |
| P2 | 4 | 4 | 1 | 17 | 13 | 9 |
| P3 | 2 | 5 | 3 | 7 | 5 | 0 |
| P4 | 6 | 2 | 2 | 13 | 7 | 5 |

---

## 5. Round Robin

### Concept
- Each process gets a **time quantum** (typically 2)
- Works like FCFS within each quantum
- Processes that don't finish **re-enter the queue** (preemptive)

### Solved Example

**Processes:** P1 (AT=0, BT=5), P2 (AT=1, BT=3), P3 (AT=2, BT=1)
**Time Quantum = 2**

**Gantt Chart:**
```
| P1 | P2 | P3 | P1 | P2 | P1 |
0----2----4----5----7----8----9
```

| Step | Process | Runs From | Runs For | Remaining BT |
|------|---------|-----------|----------|-------------|
| 1 | P1 | 0 | 2 | 3 |
| 2 | P2 | 2 | 2 | 1 |
| 3 | P3 | 4 | 1 (finishes) | 0 |
| 4 | P1 | 5 | 2 | 1 |
| 5 | P2 | 7 | 1 (finishes) | 0 |
| 6 | P1 | 8 | 1 (finishes) | 0 |

| Process | AT | BT | CT | TAT | WT |
|---------|----|----|----|-----|----|
| P1 | 0 | 5 | 9 | 9 | 4 |
| P2 | 1 | 3 | 8 | 7 | 4 |
| P3 | 2 | 1 | 5 | 3 | 2 |

### Another Example

**Processes:** P1 (AT=0, BT=7), P2 (AT=2, BT=4), P3 (AT=4, BT=2)
**Time Quantum = 2**

**Gantt Chart:**
```
| P1 | P2 | P3 | P1 | P2 | P1 | P2 |
0----2----4----6----8----10---12---14
```

| Process | AT | BT | CT | TAT | WT |
|---------|----|----|----|-----|----|
| P1 | 0 | 7 | 14 | 14 | 7 |
| P2 | 2 | 4 | 14 | 12 | 8 |
| P3 | 4 | 2 | 8 | 4 | 2 |

---

## 6. Shortest Job First (SJF) - Non-Preemptive

### Concept
- Non-preemptive: selects the process with the **shortest burst time** among those that have arrived
- Runs to completion once started

### Code Approach

```
1. Create Process class: PID, AT, BT, CT, TAT, WT, completed (bool)
2. Sort processes by AT initially
3. completed_count = 0, currentTime = 0
4. While completed_count < n:
     a. Find available process (AT <= currentTime, !completed) with min BT
     b. If none found:
        - CPU is idle, currentTime += 1, continue
     c. If found:
        - CT = currentTime + BT
        - TAT = CT - AT
        - WT = TAT - BT
        - Mark process as completed
        - completed_count += 1
        - currentTime += BT
5. Calculate averages
```

---

## 7. Shortest Remaining Time First (SRTF)

### Concept
- Preemptive version of SJF
- Constantly evaluates: if a new process arrives with shorter remaining time, preempt current process
- Executes processes in **1-unit time slices**

### Code Approach

```
1. Create Process class: PID, AT, BT, remainingBT, CT, TAT, WT
2. Sort processes by AT initially
3. completed_count = 0, currentTime = 0
4. While completed_count < n:
     a. Find available process (!completed, remainingBT > 0) with min remainingBT
     b. If none found:
        - CPU is idle, currentTime += 1, continue
     c. If found:
        - Execute for 1 unit: remainingBT -= 1, currentTime += 1
        - If remainingBT == 0:
            - CT = currentTime
            - TAT = CT - AT
            - WT = TAT - BT
            - Mark as completed
            - completed_count += 1
5. Calculate averages
```

---

## 8. Code Approaches

### FCFS - Code Approach

```
1. Create a Process class with: PID, AT, BT, CT, TAT, WT
2. Sort processes by AT (already sorted if input is ordered)
3. Build Gantt chart:
   - current_time = 0
   - For each process (in order):
     - CT = current_time + BT
     - TAT = CT - AT
     - WT = TAT - BT
     - current_time = CT
4. Calculate averages
```

### Priority Scheduling - Code Approach (Preemptive)

```
1. Create Process class: PID, AT, BT, remainingBT, Priority, CT, TAT, WT
2. Sort processes by AT initially
3. completed_count = 0, currentTime = 0
4. While completed_count < n:
   a. Find available process (!completed) with highest priority
   b. Tie-breaking: if same priority, select one with earlier AT
   c. Execute for 1 unit: remainingBT -= 1, currentTime += 1
   d. If remainingBT == 0:
        - CT = currentTime
        - TAT = CT - AT
        - WT = TAT - BT
        - Mark as completed
        - completed_count += 1
5. Calculate averages
```

### Round Robin - Code Approach

```
1. Create Process class: PID, AT, BT, remainingBT, CT, TAT, WT
2. Sort processes by AT
3. Create a Queue for ready processes
4. current_time = 0, completed = 0, index = 0 (for processes array)
5. While completed < n:
   a. While index < n AND processes[index].AT <= current_time:
        queue.add(processes[index])
        index++
   b. If queue is empty:
        current_time++  (CPU idle, wait for next arrival)
        continue
   c. Process = queue.dequeue()
   d. execution = min(Process.remainingBT, timeQuantum)
   e. Process.remainingBT -= execution
   f. current_time += execution
   g. If Process.remainingBT == 0:
        Process.CT = current_time
        completed++
   h. Else:
        queue.add(Process)  (re-enter queue)
6. Calculate TAT = CT - AT, WT = TAT - BT for all processes
7. Calculate averages
```

---

## 6.5 Additional Solved Examples (Harder Cases)

### FCFS - CPU Idle Time Case

**Processes:** P1 (AT=0, BT=5), P2 (AT=4, BT=3), P3 (AT=10, BT=2)

**Key insight:** P2 arrives at t=4 and runs at t=5 immediately. P3 arrives at t=10, but CPU is idle at t=8 (nothing to run), then runs P3 at t=10.

**Gantt Chart:**
```
|  P1  |   P2   |   idle   | P3 |
0------5-------8---------10----12
```

| Process | AT | BT | CT | TAT | WT |
|---------|----|----|----|-----|----|
| P1 | 0 | 5 | 5 | 5 | 0 |
| P2 | 4 | 3 | 8 | 4 | 1 |
| P3 | 10 | 2 | 12 | 2 | 0 |

**Note:** P3 WT = 2 - 10 - 2 ... wait. TAT = 12 - 10 = 2. WT = 2 - 2 = 0.
P3 waits 0 time because it runs immediately when it arrives! The CPU is idle from 8 to 10, which means the **CPU has idle time**.

**CPU Idle time** = 3 (from t=8 to t=11... actually CPU runs P3 from 10 to 12)
Idle = [8 to 10] = 2 units of idle time.

---

### Round Robin - Large Time Quantum (becomes FCFS-like)

**Processes:** P1 (AT=0, BT=4), P2 (AT=1, BT=3), P3 (AT=2, BT=5)
**Time Quantum = 6** (larger than max BT)

**Gantt Chart:**
```
|   P1    |    P2     |    P3     |
0---------4----------7----------12
```

Since quantum = 6 > all BT values, each process runs once to completion → **Round Robin with large Q behaves like FCFS**.

| Process | AT | BT | CT | TAT | WT |
|---------|----|----|----|-----|----|
| P1 | 0 | 4 | 4 | 4 | 0 |
| P2 | 1 | 3 | 7 | 6 | 3 |
| P3 | 2 | 5 | 12 | 10 | 5 |

---

### Priority Scheduling - All Same Priority

**Processes:** P1 (AT=0, BT=5, Pri=3), P2 (AT=1, BT=3, Pri=3), P3 (AT=2, BT=2, Pri=3)

**All same priority → falls back to AT tie-breaking → behaves like FCFS**

**Gantt Chart:**
```
|  P1  |   P2   |   P3   |
0------5-------8-------10
```

| Process | AT | BT | Priority | CT | TAT | WT |
|---------|----|----|----------|----|-----|----|
| P1 | 0 | 5 | 3 | 5 | 5 | 0 |
| P2 | 1 | 3 | 3 | 8 | 7 | 4 |
| P3 | 2 | 2 | 3 | 10 | 8 | 6 |

---

### Round Robin - Quantum = 1

**Processes:** P1 (AT=0, BT=4), P2 (AT=1, BT=3), P3 (AT=2, BT=5)
**Time Quantum = 1**

**Gantt Chart:**
```
|P1|P2|P3|P1|P2|P3|P1|P2|P3|P1|P3|P3|P3|
0--1--2--3--4--5--6--7--8--9--10-11-12-13-14
```

Step-by-step:
| Step | Queue (before) | Runs | Remaining BT after |
|------|---------------|------|---|
| 1 | [P1] | P1(1 unit) | P1=3 |
| 2 | [P2] | P2(1 unit) | P2=2 |
| 3 | [P3] | P3(1 unit) | P3=4 |
| 4 | [P1] | P1(1 unit) | P1=2 |
| 5 | [P2] | P2(1 unit) | P2=1 |
| 6 | [P3] | P3(1 unit) | P3=3 |
| 7 | [P1] | P1(1 unit) | P1=1 |
| 8 | [P2] | P2(1 unit) | P2=0 ✓ |
| 9 | [P3] | P3(1 unit) | P3=2 |
| 10 | [P1] | P1(1 unit) | P1=0 ✓ |
| 11 | [P3] | P3(1 unit) | P3=1 |
| 12 | [P3] | P3(1 unit) | P3=0 ✓ |

| Process | AT | BT | CT | TAT | WT |
|---------|----|----|----|-----|----|
| P1 | 0 | 4 | 9 | 9 | 5 |
| P2 | 1 | 3 | 8 | 7 | 4 |
| P3 | 2 | 5 | 14 | 12 | 7 |

---

## 7. Practice Numericals (Try These!)

### FCFS Problems

**Q1:** Solve for the following processes using FCFS. Calculate Average TAT and Average WT.

| Process | AT | BT |
|---------|----|----|
| P1 | 0 | 3 |
| P2 | 1 | 5 |
| P3 | 2 | 2 |
| P4 | 3 | 4 |
| P5 | 4 | 1 |

<details>
<summary><strong>Click for Answer</strong></summary>

**Gantt Chart:**
```
| P1 |  P2  | P3 |  P4  | P5 |
0----3------8-----10----14---15
```

| Process | AT | BT | CT | TAT | WT |
|---------|----|----|----|-----|----|
| P1 | 0 | 3 | 3 | 3 | 0 |
| P2 | 1 | 5 | 8 | 7 | 2 |
| P3 | 2 | 2 | 10 | 8 | 6 |
| P4 | 3 | 4 | 14 | 11 | 7 |
| P5 | 4 | 1 | 15 | 11 | 10 |

**Average TAT = (3+7+8+11+11)/5 = 40/5 = 8.0**
**Average WT = (0+2+6+7+10)/5 = 25/5 = 5.0**
</details>

---

**Q2:** Solve using FCFS. Watch for CPU idle time.

| Process | AT | BT |
|---------|----|----|
| P1 | 0 | 3 |
| P2 | 5 | 4 |
| P3 | 6 | 2 |

<details>
<summary><strong>Click for Answer</strong></summary>

**Gantt Chart:**
```
| P1 | idle | P2 | P3 |
0----3------5-----9----11
```
Idle = t=3 to t=5 = 2 units

| Process | AT | BT | CT | TAT | WT |
|---------|----|----|----|-----|----|
| P1 | 0 | 3 | 3 | 3 | 0 |
| P2 | 5 | 4 | 9 | 4 | 0 |
| P3 | 6 | 2 | 11 | 5 | 3 |

**Average TAT = 4.0** | **Average WT = 1.0**
</details>

---

**Q3 (Exam Level):** Solve using FCFS.

| Process | AT | BT |
|---------|----|----|
| P1 | 0 | 8 |
| P2 | 3 | 4 |
| P3 | 4 | 6 |
| P4 | 5 | 5 |
| P5 | 7 | 3 |

<details>
<summary><strong>Click for Answer</strong></summary>

**Gantt Chart:**
```
|  P1  |   P2   |   P3   |   P4   |  P5  |
0-------8--------12-------18-------23----26
```

| Process | AT | BT | CT | TAT | WT |
|---------|----|----|----|-----|----|
| P1 | 0 | 8 | 8 | 8 | 0 |
| P2 | 3 | 4 | 12 | 9 | 5 |
| P3 | 4 | 6 | 18 | 14 | 8 |
| P4 | 5 | 5 | 23 | 18 | 13 |
| P5 | 7 | 3 | 26 | 19 | 16 |

**Average TAT = 13.6** | **Average WT = 8.4**
</details>

---

### Priority Scheduling Problems

**Q4 (Non-Preemptive):** Solve using Priority Scheduling. Higher number = higher priority.

| Process | AT | BT | Priority |
|---------|----|----|----------|
| P1 | 0 | 5 | 2 |
| P2 | 2 | 3 | 4 |
| P3 | 3 | 6 | 1 |
| P4 | 5 | 4 | 3 |

<details>
<summary><strong>Click for Answer</strong></summary>

- t=0: P1 arrives (only option), runs to completion (BT=5)
- t=5: P2, P3, P4 all arrived. Pick highest priority: P2 (Pri=4)
- t=8: P4 (Pri=3) > P3 (Pri=1). P4 runs
- t=12: P3 runs last

**Gantt Chart:**
```
|  P1  |  P2  |   P4   |   P3   |
0------5------8--------12--------18
```

| Process | AT | BT | Pri | CT | TAT | WT |
|---------|----|----|-----|----|-----|----|
| P1 | 0 | 5 | 2 | 5 | 5 | 0 |
| P2 | 2 | 3 | 4 | 8 | 6 | 3 |
| P3 | 3 | 6 | 1 | 18 | 15 | 9 |
| P4 | 5 | 4 | 3 | 12 | 7 | 3 |

**Average TAT = 8.25** | **Average WT = 3.75**
</details>

---

**Q5 (Preemptive):** Solve using Preemptive Priority Scheduling.

| Process | AT | BT | Priority |
|---------|----|----|----------|
| P1 | 0 | 6 | 3 |
| P2 | 2 | 4 | 5 |
| P3 | 4 | 2 | 3 |

<details>
<summary><strong>Click for Answer</strong></summary>

- t=0: P1 starts (only option, Pri=3)
- t=2: P2 arrives (Pri=5 > P1's Pri=3), **preempts** P1. P1 remaining = 4. P2 runs to completion (BT=4)
- t=6: P3 arrives (Pri=3), P1 (Pri=3, remaining=4). Same priority → P1 arrived earlier (t=0) → P1 runs (remaining=4)
- t=10: P1 finishes (4 units). P3 runs (BT=2)
- t=12: P3 finishes

**Gantt Chart:**
```
|  P1  |   P2   |   P1   |  P3  |
0------2--------6--------10-----12
```

| Process | AT | BT | Pri | CT | TAT | WT |
|---------|----|----|-----|----|-----|----|
| P1 | 0 | 6 | 3 | 10 | 10 | 4 |
| P2 | 2 | 4 | 5 | 6 | 4 | 0 |
| P3 | 4 | 2 | 3 | 12 | 8 | 6 |

**Average TAT = 7.33** | **Average WT = 3.33**
</details>

---

**Q6 (Preemptive):** Solve using Preemptive Priority Scheduling. Multiple preemptions!

| Process | AT | BT | Priority |
|---------|----|----|----------|
| P1 | 0 | 5 | 2 |
| P2 | 1 | 3 | 4 |
| P3 | 3 | 4 | 5 |
| P4 | 5 | 2 | 3 |

<details>
<summary><strong>Click for Answer</strong></summary>

- t=0: P1 starts (Pri=2)
- t=1: P2 arrives (Pri=4 > 2), **preempts P1** (P1 remaining=4). P2 runs
- t=4: P3 arrives (Pri=5 > P2's Pri=4), **preempts P2** (P2 remaining=1). P3 runs to completion (BT=4)
- t=8: P2 (Pri=4, remaining=1) and P4 (Pri=3, remaining=2). P2 has higher priority. P2 runs
- t=9: P2 finishes. P4 runs
- t=11: P4 finishes. P1 (remaining=4) runs
- t=15: P1 finishes

**Gantt Chart:**
```
|  P1  |  P2  |  P3  |  P2  |  P4  |    P1    |
0------1------2------6--------9-------11-------15
```

| Process | AT | BT | Pri | CT | TAT | WT |
|---------|----|----|-----|----|-----|----|
| P1 | 0 | 5 | 2 | 15 | 15 | 10 |
| P2 | 1 | 3 | 4 | 9 | 8 | 5 |
| P3 | 3 | 4 | 5 | 6 | 3 | -1 |
| P4 | 5 | 2 | 3 | 11 | 6 | 4 |

**Check P3:** TAT = 6-3 = 3. WT = 3-4 = -1? No! WT can't be negative. 
WT = TAT - BT = 3 - 4 = -1... **This is wrong!** 

**Fix:** P3 arrived at t=3 and ran from t=6 to t=10. WT = (CT - BT) - AT = (10 - 4) - 3 = 3. 
Actually: WT = CT - AT - BT = 10 - 3 - 4 = 3. 

**Corrected table:**

| Process | AT | BT | Pri | CT | TAT | WT |
|---------|----|----|-----|----|-----|----|
| P1 | 0 | 5 | 2 | 15 | 15 | 10 |
| P2 | 1 | 3 | 4 | 9 | 8 | 5 |
| P3 | 3 | 4 | 5 | 7 | 4 | 0 |
| P4 | 5 | 2 | 3 | 11 | 6 | 4 |

**Average TAT = 6.75** | **Average WT = 4.75**

**Watch out!** CT for P3 = 3 (arrival) + 4 (BT) = 7 (it ran immediately when it arrived at a preemption point).

**Wait — correction:** P3 arrives at t=3, but doesn't run until t=4 (when P2 is preempted). P3 runs from t=4 to t=8. So CT = 8. TAT = 8-3 = 5. WT = 5-4 = 1.

**Final corrected table:**

| Process | AT | BT | Pri | CT | TAT | WT |
|---------|----|----|-----|----|-----|----|
| P1 | 0 | 5 | 2 | 15 | 15 | 10 |
| P2 | 1 | 3 | 4 | 9 | 8 | 5 |
| P3 | 3 | 4 | 5 | 8 | 5 | 1 |
| P4 | 5 | 2 | 3 | 11 | 6 | 4 |

**Average TAT = 8.5** | **Average WT = 5.0**
</details>

---

### Round Robin Problems

**Q7:** Solve using Round Robin. **Time Quantum = 2**

| Process | AT | BT |
|---------|----|----|
| P1 | 0 | 4 |
| P2 | 1 | 3 |
| P3 | 2 | 5 |
| P4 | 3 | 2 |

<details>
<summary><strong>Click for Answer</strong></summary>

**Queue evolution:**
- t=0: Queue=[P1]. Run P1(2). P1 remaining=2. Queue=[]
- t=2: P2,P3,P4 arrive. Queue=[P2,P3,P4]. Run P2(2). P2 remaining=1. Queue=[P3,P4,P2]
- t=4: Run P3(2). P3 remaining=3. Queue=[P4,P2,P3]
- t=6: Run P4(2). P4 finishes. Queue=[P2,P3]
- t=8: Run P2(1). P2 finishes. Queue=[P3]
- t=9: Run P3(2). P3 remaining=1. Queue=[P3]
- t=11: Run P3(1). P3 finishes.

**Gantt Chart:**
```
|  P1  |  P2  |  P3  |  P4  |  P2  |  P3  | P3 |
0------2------4------6------8-------10------12---13
```

| Process | AT | BT | CT | TAT | WT |
|---------|----|----|----|-----|----|
| P1 | 0 | 4 | 2 | 2 | -2 |

**Oops, let me redo CT:**
| Process | AT | BT | CT | TAT | WT |
|---------|----|----|----|-----|----|
| P1 | 0 | 4 | 2 | 2 | -2 |

**That can't be right. Let me recalculate:** P1 runs 0-2, then 2-4. CT = 4. TAT = 4-0 = 4. WT = 4-4 = 0.

| Process | AT | BT | CT | TAT | WT |
|---------|----|----|----|-----|----|
| P1 | 0 | 4 | 4 | 4 | 0 |
| P2 | 1 | 3 | 10 | 9 | 6 |
| P3 | 2 | 5 | 13 | 11 | 6 |
| P4 | 3 | 2 | 8 | 5 | 3 |

**Average TAT = 7.25** | **Average WT = 3.75**
</details>

---

**Q8:** Solve using Round Robin. **Time Quantum = 3**

| Process | AT | BT |
|---------|----|----|
| P1 | 0 | 5 |
| P2 | 1 | 2 |
| P3 | 2 | 4 |
| P4 | 3 | 3 |

<details>
<summary><strong>Click for Answer</strong></summary>

- t=0: Queue=[P1]. Run P1(3). P1 remaining=2. Queue=[]
- t=3: P2,P3,P4 arrived. Queue=[P2,P3,P4]. Run P2(2, finishes). Queue=[P3,P4]
- t=5: Run P3(3). P3 remaining=1. Queue=[P4,P3]
- t=8: Run P4(3, finishes). Queue=[P3]
- t=11: Run P3(1, finishes).

**Gantt Chart:**
```
|  P1  | P2 |  P3  |  P4  | P3 |
0------3-----5--------8-------11---12
```

| Process | AT | BT | CT | TAT | WT |
|---------|----|----|----|-----|----|
| P1 | 0 | 5 | 3 | 3 | -2 |

**Recalculate CT:** P1 runs 0-3, then 3-5 (P2 takes over at t=3).
P1 runs 0-3 (first burst). Then at t=12... wait. P1's remaining=2 is added to queue.

**Correct queue evolution:**
- t=0: Queue=[P1]. Run P1(3). P1 rem=2. Queue=[]
- t=3: Add P2,P3,P4. Queue=[P2,P3,P4]. Run P2(2, finishes). Queue=[P3,P4,P1]
- t=5: Run P3(3). P3 rem=1. Queue=[P4,P1,P3]
- t=8: Run P4(3, finishes). Queue=[P1,P3]
- t=11: Run P1(2, finishes). Queue=[P3]
- t=13: Run P3(1, finishes).

**Correct Gantt Chart:**
```
|  P1  | P2 |  P3  |  P4  |  P1  | P3 |
0------3-----5--------8-------11-----13---14
```

| Process | AT | BT | CT | TAT | WT |
|---------|----|----|----|-----|----|
| P1 | 0 | 5 | 13 | 13 | 8 |
| P2 | 1 | 2 | 5 | 4 | 2 |
| P3 | 2 | 4 | 14 | 12 | 8 |
| P4 | 3 | 3 | 11 | 8 | 5 |

**Average TAT = 9.25** | **Average WT = 5.75**
</details>

---

**Q9 (Exam Level):** Solve using Round Robin. **Time Quantum = 1**

| Process | AT | BT |
|---------|----|----|
| P1 | 0 | 3 |
| P2 | 2 | 5 |
| P3 | 3 | 1 |

<details>
<summary><strong>Click for Answer</strong></summary>

- t=0: Queue=[P1]. Run P1(1). Rem=2. Queue=[]
- t=1: Nothing new. Queue empty → wait.
- t=2: P2 arrives. Queue=[P2]. Run P2(1). Rem=4. Queue=[P2]
- t=3: P3 arrives. Queue=[P3,P2]. Run P3(1, finishes). Queue=[P2]
- t=4: Queue=[P2]. Run P2(1). Rem=3. Queue=[P2]
- t=5: Queue=[P2]. Run P2(1). Rem=2. Queue=[P2]
- t=6: Queue=[P2]. Run P2(1). Rem=1. Queue=[P2]
- t=7: Queue=[P2]. Run P2(1). Rem=0 ✓

**Gantt Chart:**
```
|P1|wait| P2 | P3 | P2 | P2 | P2 | P2 |
0--1-----2-----3-----4-----5-----6-----7-----8
```

| Process | AT | BT | CT | TAT | WT |
|---------|----|----|----|-----|----|
| P1 | 0 | 3 | 1 | 1 | -2 |

**Recalculate CT carefully:**
- P1 runs at t=0. CT of P1 = when P1 finishes. P1 has remaining BT=2, added to queue after t=1. But queue is empty, and next arrival is t=2. P1 runs next at t=2 (before P2).

**Correct approach:**
- t=0: Queue=[P1]. Run P1(1). P1 rem=2. Queue=[]
- t=1: Queue empty. CPU waits.
- t=2: P2 arrives. Queue=[P2]. Run P2(1). P2 rem=4. Queue=[]
- t=3: P3 arrives. Queue=[P3]. Run P3(1, finishes). Queue=[]
- t=4: Queue empty. CPU waits.
- t=5: Nothing. Wait. Actually need to check arrivals. No new arrivals.
- Continue with P2: t=5: Queue=[P2]. Run P2(1). rem=3. Queue=[]
- t=6: Queue=[P2]. Run P2(1). rem=2. Queue=[]
- t=7: Queue=[P2]. Run P2(1). rem=1. Queue=[]
- t=8: Queue=[P2]. Run P2(1). rem=0 ✓

**Gantt Chart:**
```
| P1 |wait| P2 | P3 | wait | P2 | P2 | P2 | P2 |
0----1------2-----3------4------5-----6-----7-----8-----9
```

**This is getting complex with idle time. Let me simplify:**

| Process | AT | BT | CT | TAT | WT |
|---------|----|----|----|-----|----|
| P1 | 0 | 3 | 1 | 1 | -2 |

P1 CT = 1? No! P1 BT=3, ran for 1. Remaining=2, goes to back of queue. It finishes when it gets its next turns.

**P1 CT = 1 + 2 = 3?** No. After P1's first turn (0-1), remaining=2 goes to back of queue. Queue is empty, so next time CPU is ready, P1 gets scheduled again.

Actually t=1: CPU idle until t=2. At t=2, P2 arrives and enters queue. P1 is also back in queue (but was added at t=1). So queue at t=2 = [P1, P2]. Run P1 first!

**Correct:** Queue after P1's first run (t=0→1): P1 rem=2, re-entered queue. Queue=[P1]
t=2: P2 arrives. Queue=[P1, P2]. Run P1(1). rem=1. Queue=[P2, P1]
t=3: P3 arrives. Queue=[P2, P1, P3]. Run P2(1). rem=4. Queue=[P1, P3, P2]
t=4: Queue=[P1, P3, P2]. Run P1(1, finishes). Queue=[P3, P2]
t=5: Queue=[P3, P2]. Run P3(1, finishes). Queue=[P2]
t=6-9: P2 runs 4 more times (rem=4)

**Correct Gantt Chart:**
```
| P1 |wait| P1 |  P2  | P1 | P3 | P2 | P2 | P2 | P2 |
0----1------2-----3------4-----5-----6-----7-----8-----9-----10
```

| Process | AT | BT | CT | TAT | WT |
|---------|----|----|----|-----|----|
| P1 | 0 | 3 | 5 | 5 | 2 |
| P2 | 2 | 5 | 10 | 8 | 3 |
| P3 | 3 | 1 | 6 | 3 | 2 |

**Average TAT = 5.33** | **Average WT = 2.33**
</details>

---

### Combined/Challenge Problems

**Q10:** Given the following processes, solve using **both FCFS and Round Robin (Q=2)**. Compare the results.

| Process | AT | BT |
|---------|----|----|
| P1 | 0 | 6 |
| P2 | 2 | 4 |
| P3 | 4 | 2 |

<details>
<summary><strong>Click for Answer</strong></summary>

**FCFS:**
```
|   P1   |   P2   |  P3  |
0--------6--------10----12
```
| Process | CT | TAT | WT |
|---------|----|-----|----|
| P1 | 6 | 6 | 0 |
| P2 | 10 | 8 | 4 |
| P3 | 12 | 8 | 6 |
**Avg TAT = 7.33** | **Avg WT = 3.33**

**Round Robin (Q=2):**
- t=0: Queue=[P1]. Run P1(2). rem=4. Queue=[]
- t=2: P2 arrives. Queue=[P2]. Run P2(2). rem=2. Queue=[P2]
- t=4: P3 arrives. Queue=[P3,P2]. Run P3(2, finishes). Queue=[P2]
- t=6: Queue=[P2]. Run P2(2, finishes). Queue=[]
- t=8: Queue empty. Run P1(2). rem=2. Queue=[P1]
- t=10: Queue=[P1]. Run P1(2, finishes).

**Gantt Chart:**
```
|  P1  |  P2  |  P3  |  P2  |  P1  | P1 |
0------2------4------6-------8------10---12---14
```
| Process | CT | TAT | WT |
|---------|----|-----|----|
| P1 | 14 | 14 | 8 |
| P2 | 8 | 6 | 2 |
| P3 | 6 | 2 | 0 |
**Avg TAT = 7.33** | **Avg WT = 3.33**

**Observation:** Same averages in this case, but different completion orders!
</details>

---

## 7. Quick Problem-Solving Checklist

For every scheduling numerical:

1. **Draw the Gantt chart first** - this gives you all CT values
2. **Compute TAT** for each process: CT - AT
3. **Compute WT** for each process: TAT - BT
4. **Calculate averages**: sum / n
5. **Double-check** the scheduling rule (preemptive vs non-preemptive, priority order, time quantum)

---

## 8. Exam Tips

- **10+ marks** come from numericals - practice the Gantt chart method
- FCFS and SJF code are most important
- Round Robin code is also important
- Priority scheduling code is less important (follows SJF pattern)
- Always check: higher number = higher priority OR lower number = higher priority
- Time quantum is typically 2 but verify in the question
- For Round Robin, processes that don't finish **go back in the queue**
