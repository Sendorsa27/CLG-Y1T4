# CPU Scheduling Algorithms -- Class Notes

## 1. Core Process Class (used across all algorithms)

**Variables:** `pid`, `at`, `bt`, `ct`, `tat`, `wt`, `rt` (remaining time), `priority`, `completed`

**Constructor:**
- Basic init: `this.pid = id;`, `this.at = at;`, `this.bt = bt;`
- `completed = false` (non-preemptive)
- `rt = bt` (preemptive algorithms)
- `priority` passed in and initialized for Priority scheduling

**Attributes:**

| Attribute | Description |
|-----------|-------------|
| `pid` | Process ID |
| `at` (arrival_time) | When the process arrives |
| `bt` (burst_time) | Total CPU time needed |
| `ct` (completion_time) | When the process finishes |
| `tat` (turnaround_time) = `ct - at` | Total time from arrival to completion |
| `wt` (waiting_time) = `tat - bt` | Time spent waiting in queue |
| `rt` (remaining_time) | For preemptive algorithms (initially = `bt`) |
| `priority` | For priority scheduling (higher number = higher priority) |
| `completed` | Boolean flag for non-preemptive algorithms |

---

## 2. FCFS (First Come First Serve) -- Non-Preemptive

**Concept:** Execute processes in order of arrival.

**Steps:**
1. Instantiate process array, e.g., `processes[0] = new Process(1, 0, 4);`
2. Sort array by `at` (ascending): `Arrays.sort(processes, (a,b) -> a.at - b.at);`
3. Initialize tracking variables: `currentTime = 0`, `totalCT = 0`, `totalTAT = 0`, `totalWT = 0`
4. Iterate through sorted processes: `for (Process p : processes)`
5. If idle (`currentTime < p.at`), fast-forward: `currentTime = p.at`
6. Calculations:
   - `p.ct = currentTime + p.bt`
   - `p.tat = p.ct - p.at`
   - `p.wt = p.tat - p.bt`
   - `currentTime = p.ct`
7. Accumulate metrics: `totalCT += p.ct`, `totalTAT += p.tat`, `totalWT += p.wt`

**Example Table Data:**

| Process | AT | BT | CT | TAT | WT |
|---------|----|----|----|-----|----|
| P1      | 0  | 4  | 4  | 4   | 0  |
| P2      | 1  | 3  | 7  | 6   | 3  |
| P3      | 2  | 2  | 9  | 7   | 5  |
| P4      | 3  | 1  | 10 | 7   | 6  |

**Key Insight:** In FCFS, a process runs to completion once started. Completion time and current time are identical after each process.
**Trace Example:** P1 with AT=2, BT=8 → CT = 2 + 8 = 10.

---

## Introductory Trace Table

Introductory example processes used to illustrate the algorithms:

| Process | AT | BT |
|---------|----|----|
| P1      | 0  | 4  |
| P2      | 1  | 3  |
| P3      | 2  | 2  |
| P4      | 3  | 1  |

---

## 3. SJF (Shortest Job First) -- Non-Preemptive

**Concept:** Execute the process with the smallest burst time among all arrived, incomplete processes.

**Key Additions:**
- `completed` (bool) attribute on each process = `false` initially
- `completed_count = 0`
- `selected = -1`, `min_bt = Integer.MAX_VALUE` at start of each `while` iteration
- No sorting needed

**Steps:**
1. Init processes with `new Process(pid, at, bt)` (no sorting)
2. `while completed_count < n`:
   - Loop through all processes: `for (int i=0; i<n; i++)`
   - Selection conditions: `!p.completed AND p.at <= current_time AND p.bt < min_bt`
   - Match: `min_bt = p.bt`, `selected = i`
   - If `selected == -1` (no process arrived): `current_time++`, continue
   - Execute selected to completion:
     - `p.ct = current_time + p.bt`, `p.tat = p.ct - p.at`, `p.wt = p.tat - p.bt`
     - `current_time += p.bt`
     - `p.completed = true`, `completed_count++`

**Example Table Data:**

| Process | AT | BT | CT | TAT | WT | C=T |
|---------|----|----|----|-----|----|-----|
| P1      | 0  | 7  | 7  | 7   | 0  | Yes |
| P2      | 2  | 4  | 12 | 10  | 6  | Yes |
| P3      | 4  | 1  | 8  | 4   | 3  | Yes |
| P4      | 5  | 4  | 16 | 11  | 7  | Yes |

**Key Difference from FCFS:** Linear scan instead of sorting; picks by minimum burst time among arrived processes.

---

## 4. SRTF (Shortest Remaining Time First) -- Preemptive

**Concept:** Like SJF but preemptive -- a new process can interrupt the running one if it has shorter remaining time. Runs **1 unit at a time**.

**Preemption Example:** A process with BT=7 runs for 2 units → remaining BT = 5.

**Changes from SJF:**
- Replace `completed` with `rt` (remaining time), initialized as `this.rt = bt` in constructor
- Condition: `p.rt > 0` replaces `!p.completed`
- Process runs for only **1 unit** each iteration
- Track `min_rt = Integer.MAX_VALUE` inside `while` loop

**Steps:**
1. `rt = bt` for each process
2. `while completed_count < n`:
   - **For-loop to select:** `p.rt > 0 AND p.at <= current_time AND p.rt < min_rt`
   - If `selected == -1`: `current_time++`, continue
   - `p.rt--`, `current_time++`
   - **Check completion:** if `p.rt == 0`:
     - `p.ct = current_time`, `p.tat = p.ct - p.at`, `p.wt = p.tat - p.bt`
     - `completed_count++`

---

## 5. Priority Scheduling -- Preemptive

**Concept:** Execute the process with the highest priority. Tie-break by earliest arrival time.

**Changes from SRTF:**
- Add `priority` attribute alongside `rt`, both passed into and initialized in constructor
- Track `h_p = Integer.MIN_VALUE` (highest priority)
- Selection logic: `p.priority > h_p`
- Tie-breaking `else if p.priority == h_p`: `p.at < processes[selected].at` → `selected = i`
- Optional tie-breaker: burst time if two processes share priority and arrival time
- **Note:** Standard convention is higher number = higher priority, but exam questions may use **lowest number = highest priority**

**Steps:**
1. `h_p = Integer.MIN_VALUE`
2. **For-loop to select:**
   - `p.rt > 0 AND p.at <= current_time AND p.priority > h_p`
   - `else if p.priority == h_p AND selected != -1 AND p.at < processes[selected].at`
   - `h_p = p.priority`, `selected = i`
3. Rest follows SRTF logic (1 unit execution, check completion, etc.)

---

## 6. Round Robin -- Preemptive (Queue-based)

**Concept:** Each process gets a fixed **time quantum (TQ)**. Remaining time is re-queued after TQ expires.

**Key Additions:**
- `remaining_time` (rt = bt) in process class
- Use a **Queue** data structure: `Queue<Process> q = new LinkedList<>();`
- `time_quantum (TQ)` given as input (e.g., `int TQ = 2;`)
- `index = 0` tracker for sorted process array

**Steps:**
1. `rt = bt` for each process
2. Sort processes by `at`, create empty queue, `index = 0`
3. `while completed_count < n`:
   - **Add arrived processes to queue:** `while (index < n && processes[index].at <= currentTime)`: `q.add(processes[index])`, `index++`
   - If queue empty: `currentTime++`, continue
   - `p = q.remove()`
   - `ex_t = Math.min(TQ, p.rt)` -- runs for TQ or remaining time, whichever is less
   - `p.rt -= ex_t`, `currentTime += ex_t`
   - **Re-add arrived processes:** repeat the index loop (new processes may have arrived while p ran)
   - If `p.rt > 0`: `q.add(p)` -- re-queue
   - If `p.rt == 0`: `p.ct = currentTime`, `p.tat = p.ct - p.at`, `p.wt = p.tat - p.bt`, `completed_count++`

**Example Trace Table (TQ = 3):**

| Process | AT | BT | Execution Detail                                  | Finish |
|---------|----|----|---------------------------------------------------|--------|
| P1      | 0  | 8  | runs 3, rem 5 → runs 3, rem 2 → finishes         | 25     |
| P2      | 1  | 4  | runs 3, rem 1 → finishes                          | 17     |
| P3      | 2  | 9  | runs 3, rem 6 → runs 3, rem 3 → finishes          | 28     |
| P4      | 3  | 5  | runs 3, rem 2 → finishes                          | 23     |
| P5      | 4  | 2  | finishes in first cycle (2 < 3)                   | 17     |

**Gantt Chart (CT Timeline):**
`3(P1) → 6(P2) → 9(P3) → 12(P4) → 15(P1) → 17(P5) → 18(P2) → 21(P3) → 23(P4) → 25(P1) → 28(P3)`

---

## Algorithm Comparison Summary

| Algorithm | Nature | Selection Criteria | Queue Used |
|-----------|--------|-------------------|------------|
| FCFS | Non-preemptive | Arrival time (sorted) | No |
| SJF | Non-preemptive | Minimum burst time | No |
| SRTF | Preemptive | Minimum remaining time | No |
| Priority | Preemptive | Highest priority (tie-break: AT) | No |
| Round Robin | Preemptive | FIFO queue (time quantum) | Yes |

---

## Key Algorithms Considerations (Cross-Cutting Concerns)

**Process Selection:** Critical in many algorithms to determine which process should be in the running state. Different algorithms use different selection criteria (arrival time, burst time, remaining time, priority).

**Queue Management:** Many algorithms like Round Robin require effective queue management, including adding and removing processes at appropriate times. Proper queue operations are essential for correct scheduling behavior.

**Time Management:** Ensures the CPU is not idle while tasks are pending and correctly calculates attributes such as completion time, turnaround time, and waiting time. Handles idle CPU periods when no process has arrived yet.

---

## Exam Pattern (from class announcement)

- **Midsem:** 20 questions total
  - **19 MCQs** × 2 marks each (theory, output prediction, numericals)
  - **1 Coding question** × 10 marks (from any scheduling algorithm)
  - Additional theory/output/numericals worth 6 marks
- **Syllabus:** FCFS, SJF (Non-preemptive), Round Robin, Priority scheduling
- **Endsem:** Coding-heavy, focused on concurrency
- **Languages supported:** C++, C, Python, Java
- **Marking:** No partial marking for MCQs/numericals
- **Priority note:** Exam questions may use lowest number = highest priority (opposite of standard convention) — always read the question carefully

---

## Flashcards

| Term | Definition |
|------|------------|
| **Process Array** | An array containing process objects to be sorted based on attributes like arrival time. |
| **Gantt Chart** | A tool used to represent the scheduling timeline of processes in scheduling algorithms. |
| **PID** | Process Identifier, a unique number used to identify a process. |
| **Arrival Time** | The time at which a process arrives and can begin execution. |
| **Burst Time** | The total time required by a process for its execution. |
| **Completion Time** | The moment at which process execution is finished. |
| **Turnaround Time** | The total time taken by a process from arrival to completion. |
| **Waiting Time** | The total time a process spends waiting in the ready queue. |
| **Time Quantum** | A fixed period of time allocated to each process in round-robin scheduling. |
| **FCFS (First-Come, First-Served)** | A non-preemptive scheduling algorithm that serves processes in the order of their arrival. |
| **SJF (Shortest Job First)** | A non-preemptive scheduling algorithm that selects processes with the shortest burst time. |
| **Preemptive Scheduling** | A scheduling method that allows interruption of processes to handle new arrivals. |

---

*Notes compiled from: CPU_scheduling_algorithms_codes_-_Class_Scaler_Academy.txt*
