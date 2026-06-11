# Concurrency 1 & 2 — Complete Study Notes

*Compiled from Scaler Academy Concurrency lectures, class notes, and quiz materials.*

---

## Table of Contents

1. [Foundations: Program, Process & Thread](#1-foundations-program-process--thread)
2. [Java OOP Basics](#2-java-oop-basics)
3. [Runnable Interface & Creating Threads](#3-runnable-interface--creating-threads)
4. [start() vs run() — Crucial Difference](#4-start-vs-run--crucial-difference)
5. [Thread Lifecycle](#5-thread-lifecycle)
6. [Concurrency vs Parallelism](#6-concurrency-vs-parallelism)
7. [Main Thread & Default Execution](#7-main-thread--default-execution)
8. [Why Multiple Threads?](#8-why-multiple-threads)
9. [Process Control Block (PCB)](#9-process-control-block-pcb)
10. [Shared vs Private Architectural Spaces](#10-shared-vs-private-architectural-spaces)
11. [Thread Pools & ThreadPoolExecutor](#11-thread-pools--threadpoolexecutor)
12. [Important Concepts to Remember](#12-important-concepts-to-remember)
13. [Quiz Questions, Answers & Explanations](#13-quiz-questions-answers--explanations)
14. [Exam Notes](#14-exam-notes)

---

## 1. Foundations: Program, Process & Thread

### Program vs Process

| Concept | Definition |
|---------|------------|
| **Program** | Static set of instructions stored on disk. Does **not** execute on its own. |
| **Process** | A program in **active execution** (a "running container") managed by the OS. |

A process owns:
- Program code
- Unique variables / data
- Allocated memory space
- Open file descriptors
- Execution state
- Uses a **Process Control Block (PCB)** to store its entire context
- Requires a heavy **context switch** when the CPU scheduler switches between processes

### Thread

- The **smallest independent unit** of code execution residing inside a process container.
- A process does **not** run code line-by-line directly — threads are where code actually executes.

### Process vs Thread Comparison

| Feature | Process | Thread |
|---------|---------|--------|
| Definition | A running program instance (dynamic entity) | Smallest unit *within* a process |
| Memory | Owns its own memory space | Shares process memory space (heap, data) |
| Creation | Heavy (new resources/memory allocation) | Lightweight (shares resources) |
| Execution | Container — does NOT execute code itself | Actual worker — does the real work |
| Communication | IPC (complex) | Direct sharing (easy) |

### Analogy: Spotify/Chrome Process

- **Process** = Container with resources (settings, cache, network, files)
- **Threads** = Workers handling subtasks
  - Thread 1: Play song / Load website
  - Thread 2: Update progress bar / UI response
  - Thread 3: Download album / File download
  - Thread 4: Network handling

---

## 2. Java OOP Basics

### Abstract Class

- Defines common parent with shared attributes/methods
- Can have: attributes, constructors, concrete methods, **and** abstract methods
- Cannot be instantiated (`new AbstractClass()` is invalid)
- Used for common parent classes sharing properties

```java
abstract class Device {
    String brand;

    Device(String brand) {
        this.brand = brand;
    }

    void showBrand() {
        System.out.println("Brand: " + brand);
    }

    abstract void turnOn();
}
```

### Interface

- Defines common capability/behavior a class must implement
- Contains method **prototypes only** (no bodies)
- Methods are implicitly `public abstract` unless marked `default`/`static`
- Used to define a contract that implementing classes must follow

```java
interface Chargeable {
    void charge();
}
```

### Implementation Pattern

```java
class Phone extends Device implements Chargeable {
    Phone(String brand) {
        super(brand);
    }

    @Override
    void turnOn() {
        System.out.println("Phone is turning on.");
    }

    @Override
    public void charge() {
        System.out.println("Phone is charging.");
    }
}
```

### Keywords

| Keyword | Meaning |
|---------|---------|
| `extends` | "is a type of" — inheritance from class (IS-A relationship) |
| `implements` | "promises to provide capability" — interface contract |

### Usage in Main

```java
public static void main(String[] args) {
    Phone phone = new Phone("Samsung");
    phone.showBrand();
    phone.turnOn();
    phone.charge();
}
```

## 3. Runnable Interface & Creating Threads

### Runnable

- A built-in Java interface (`java.lang.Runnable`)
- Functional interface with exactly one method: `public void run()`
- Encapsulates the raw core task logic (the work to be done)
- Used with `Thread` constructor: `new Thread(runnableTask)`

```java
class Task implements Runnable {
    @Override
    public void run() {
        System.out.println("Task is running");
    }
}
```

### Creating Threads — Step-by-Step Pattern

```java
// 1. Create a Runnable task
class MyTask implements Runnable {
    @Override
    public void run() {
        // Work to do
    }
}

// 2. Create an object of the task
MyTask task = new MyTask();

// 3. Create a thread with the task
Thread t = new Thread(task, "ThreadName");

// 4. Start the thread (NOT run())
t.start();
```

### Multi-threading Example: System Tasks

```java
class MonitorTask implements Runnable {
    private String taskName;
    
    @Override
    public void run() {
        System.out.println(taskName + " running in " + Thread.currentThread().getName());
    }
}

public class SystemTasks {
    public static void main(String[] args) {
        Thread cpuThread = new Thread(new MonitorTask("CPU"), "CPU");
        Thread memThread = new Thread(new MonitorTask("Memory"), "Memory");
        Thread diskThread = new Thread(new MonitorTask("Disk"), "Disk");

        cpuThread.start();
        memThread.start();
        diskThread.start();
    }
}
```

- Output order **varies** — OS scheduler decides execution order.
- Threads may run on different cores or time-slice on a single core.
- **Creation ≠ Starting**: `new Thread()` only creates; `start()` begins execution.
- New threads are named: `thread-0`, `thread-1`, etc.

### Multi-threading Example: Complete System Monitor

```java
class CpuTask implements Runnable {
    @Override
    public void run() {
        System.out.println("CPU check started by " + Thread.currentThread().getName());
        System.out.println("Checking CPU usage");
        System.out.println("CPU check completed");
    }
}

class MemoryTask implements Runnable {
    @Override
    public void run() {
        System.out.println("Memory check started by " + Thread.currentThread().getName());
        System.out.println("Checking RAM usage");
        System.out.println("Memory check completed");
    }
}

class DiskTask implements Runnable {
    @Override
    public void run() {
        System.out.println("Disk check started by " + Thread.currentThread().getName());
        System.out.println("Checking disk usage");
        System.out.println("Disk check completed");
    }
}

public class SystemMonitor {
    public static void main(String[] args) {
        System.out.println("System Monitor process started");
        System.out.println("Main thread: " + Thread.currentThread().getName());

        Thread cpuThread = new Thread(new CpuTask());
        Thread memThread = new Thread(new MemoryTask());
        Thread diskThread = new Thread(new DiskTask());

        cpuThread.start();
        memThread.start();
        diskThread.start();

        System.out.println("System Monitor main thread continues");
    }
}
```

**Expected Output (order may vary):**
```
System Monitor process started
Main thread: main
CPU check started by Thread-0
Checking CPU usage
CPU check completed
Memory check started by Thread-1
Checking RAM usage
Memory check completed
Disk check started by Thread-2
Checking disk usage
Disk check completed
System Monitor main thread continues
```

**Key Points:**
- One Java program = one process (the JVM)
- Inside that process, multiple threads are created (`Thread-0`, `Thread-1`, `Thread-2`)
- Each thread runs a different task concurrently
- The scheduler decides the output order — it is non-deterministic

---

## 4. start() vs run() — Crucial Difference

| Method | Behavior | Execution Context |
|--------|----------|-------------------|
| `t.start()` | Creates **new thread**, then calls `run()` | New thread (e.g., thread-0) |
| `task.run()` / `t.run()` | Normal method call, **no new thread** | Current thread (main) |

- Calling `.start()` is what formally commands the JVM and OS to provision an independent native execution thread.
- Calling `.run()` directly does **not** spin up a new thread. It simply executes sequentially as a normal, synchronous method call on top of whichever thread called it (usually the main thread).

### Complete Code Example: run() vs start()

```java
class MyTask implements Runnable {
    @Override
    public void run() {
        System.out.println("Task running inside: " + Thread.currentThread().getName());
    }
}

public class RunVsStartDemo {
    public static void main(String[] args) {
        MyTask task = new MyTask();
        Thread t = new Thread(task);

        // Calling run() directly — normal method call, runs in the current (main) thread
        System.out.println("Calling run() directly:");
        t.run();  // executes run() as a regular method on the main thread

        // Creating a fresh thread and calling start() — creates a new independent thread
        Thread t2 = new Thread(task);
        System.out.println("Calling start():");
        t2.start();  // JVM creates a new thread and calls run() inside it
    }
}
```

**Output:**
```
Calling run() directly:
Task running inside: main
Calling start():
Task running inside: Thread-0
```

**Key Takeaways:**

| Scenario | Method Called | New Thread Created? | Thread Name in Output |
|----------|--------------|---------------------|----------------------|
| `t.run()` | Direct method call | ❌ No | `main` (current thread) |
| `t.start()` | JVM-level start | ✅ Yes | `Thread-0` (new thread) |

**Why this happens:** `.start()` tells the JVM to create a new native thread and then invoke `run()` inside it. `.run()` is just a regular method — Java does nothing special with it.

---

## 5. Thread Lifecycle

```
[NEW] --(new keyword)--> [RUNNABLE] --(start())--> [RUNNING]
                                                             |
                                                      [BLOCKED/WAITING]
                                                             |
                                                           [TERMINATED]
```

| State | Trigger | Description |
|-------|---------|-------------|
| **NEW** | `new Thread()` | Object created, not started — thread is stuck here until `.start()` is invoked |
| **RUNNABLE** | `start()` called → scheduler picks thread | Ready to run (waiting for OS scheduler to assign CPU) |
| **RUNNING** | Scheduler picks thread | Actually executing on CPU |
| **BLOCKED/WAITING** | IO op, `wait()`, `sleep()` | Temporarily paused |
| **TERMINATED** | `run()` completes / error | Finished execution permanently |

---

## 6. Concurrency vs Parallelism

| Aspect | Concurrency | Parallelism |
|--------|-------------|-------------|
| Definition | Multiple tasks making interleaved progress (not necessarily simultaneously) | Multiple tasks physically running at the exact same instant |
| Mechanism | Single CPU core switches rapidly between tasks using time-slicing | Requires **multiple CPU cores** for true simultaneous execution |
| Analogy | One person cooking multiple dishes (pause/resume, play/pause) | Multiple people cooking different dishes together |
| Hardware | Works on single-core | Requires multi-core |

### Progress on Single-Core CPU

- All N threads are **making progress** (partially completed).
- Only **1 thread actually runs** at any instant.
- The OS creates the illusion of simultaneous execution by rapidly context-switching between tasks.

### Core Limits Summary

- **Single-core CPU**: Only 1 thread can run at any instant
- **4-core CPU**: Up to 4 threads can run simultaneously at any instant

---

## 7. Main Thread & Default Execution

Every Java program begins by automatically creating the **Main Thread**.

**Execution Flow:**
```
Class file (disk) → java Main command → OS creates Java process → JVM starts main thread → enters public static void main(String[] args)
```

- The main thread can finish while other background child threads continue executing concurrently.
- All code in `main()` runs inside the main thread unless other threads are created.

### Getting Current Thread Name

```java
System.out.println(Thread.currentThread().getName());
// Output: "main"
```

---

## 8. Why Multiple Threads?

### Single-threaded Problems

- All tasks run **sequentially** (line by line)
- Slow operations block the entire program
- UI freezes during long tasks

### Multi-threading Benefits

- Increased responsiveness
- Background work continues independently
- Better CPU utilization
- Concurrent multitasking
- UI stays active during file downloads / network calls

---

## 9. Process Control Block (PCB)

A PCB is loaded into RAM and stores critical state info during context switching.

| Field | Description |
|-------|-------------|
| Process ID | Unique identifier |
| Program Counter | Address of next instruction to execute |
| Registers | Temporary fast memory (e.g., R1, R2 in machine code `add R1, R2`) |
| Stack Pointer | Points to top of stack during execution |
| Process State | Current status of process/thread |
| Memory Info | Allocated memory space |
| IO/File Info | Open files, resources |
| Scheduling Info | Priority, queue pointers |

---

## 10. Process vs Thread — What is Shared and What is Private

### Shared (Accessible by all internal threads)

- **Code** — compiled program text (text segment)
- **Heap Memory** — dynamic memory allocation where shared objects reside
- **Files & Resources** — system I/O streams, network sockets, open file descriptors, signals

### Private (Isolated to each specific thread)

- **Program Counter (PC)** — tracks the current instruction address being executed
- **Registers** — dedicated CPU register states for immediate data manipulation
- **Stack** — private memory holding localized method frames and primitive variable states
- **State** — individual condition contexts (Running, Ready, Waiting)

No two *processes* share data → requires **IPC** for communication.

---

## 11. Thread Pools & ThreadPoolExecutor

### What is a Thread Pool?

A collection of pre-created threads that can be reused to execute tasks. Reduces the overhead of creating new threads for every task, enabling efficient resource management and faster task execution.

### ThreadPoolExecutor Parameters Reference

| Parameter | Description |
|-----------|-------------|
| `corePoolSize` | Minimum threads kept alive in pool |
| `maximumPoolSize` | Maximum threads allowed in pool |
| `keepAliveTime` | Time idle threads are retained beyond corePoolSize |
| `unit` | Time unit for keepAliveTime (e.g., `TimeUnit.SECONDS`) |
| `workQueue` | Queue holding pending tasks (e.g., `ArrayBlockingQueue`, `LinkedBlockingDeque`) |
| `threadFactory` | Factory for creating new threads |
| `handler` | Rejection policy when queue and maxPoolSize are full (`CallerRunsPolicy`, etc.) |

### How It Works

1. Thread is requested
2. If `currentWorkers < corePoolSize` → create a new thread
3. If `corePoolSize <= currentWorkers < maximumPoolSize`:
   - Check if queue has pending tasks
     - Yes: enqueue task
     - No: create thread (if allowed)
4. If `currentWorkers == maxPoolSize` and queue is full → use rejection handler

---

## 12. Important Concepts to Remember

1. **Program ≠ Process**: Program is just instructions; process is a running program
2. **Process is a container**; thread does the actual work
3. **Main thread starts automatically** in every Java program
4. **`new Thread()` creates only** → `start()` starts it
5. **`run()` is a normal method** → doesn't create new execution path
6. **Threads share heap memory** within same process
7. **Order of thread output is non-deterministic** — scheduler decides
8. **Process PCB loaded into RAM**, threads are created inside that process
9. **CPU scheduling happens at thread level** (not just process level)

---

## 13. Quiz Questions, Answers & Explanations

### Quiz 1 — OOP Foundations
**In this code, what do `extends Device` and `implements Chargeable` mean?**
```java
class Phone extends Device implements Chargeable { ... }
```
- ✅ **Correct Answer:** A. Phone is a type of Device, and Phone promises to provide the methods required by Chargeable
- 📖 **Explanation:** `extends` represents an **IS-A relationship** (inheritance), making `Phone` a specialized subclass of `Device`. `implements` means the class signs a behavioral contract with an interface, promising to define all its abstract methods.

---

### Quiz 3 — Processes & Threads
**Which statement is correct?**
- ✅ **Correct Answer:** B. A process can contain multiple threads
- 📖 **Explanation:** A process acts as the overall running container that owns system resources. Inside that single process, one or more threads can exist to execute code while sharing those same resources.

---

### Quiz 4 — Main Thread
**Which thread starts execution of `main()` in Java?**
- ✅ **Correct Answer:** A. Main thread
- 📖 **Explanation:** Every Java program automatically spins up the main thread first. This specialized entry thread executes your `public static void main(String[] args)` block.

---

### Quiz 5 — Runnable
**In Java, Runnable represents:**
- ✅ **Correct Answer:** A. A task that can be executed by a thread
- 📖 **Explanation:** `Runnable` encapsulates the raw core task logic (`void run();`). The `Thread` instance itself is simply the computational engine that holds and runs that specific task.

---

### Quiz 6 — start()
**Which line starts a new thread?**
- ✅ **Correct Answer:** B. `t1.start()`
- 📖 **Explanation:** Calling `.start()` formally commands the JVM and OS to provision an independent native execution thread.

---

### Quiz 7 — run() Direct Call
**What happens if we call `run()` directly?**
- ✅ **Correct Answer:** D. The task runs like a normal method in the current thread
- 📖 **Explanation:** Calling `.run()` directly does **not** spin up a new thread. It simply executes sequentially as a normal, synchronous method call on whatever thread called it (usually the main thread).

---

### Quiz 11 — Thread Lifecycle
**After creating a `Thread` object but before calling `start()`, the thread is:**
- ✅ **Correct Answer:** A. NEW
- 📖 **Explanation:** A thread enters the **NEW** lifecycle state the exact moment its object is allocated in memory via the `new` keyword. It stays in this state until you explicitly invoke `.start()`, which moves it to the Runnable pool.

---

### Quiz 2 (Runnable Interface Set) — Which method must be implemented?
**Which method must be implemented when a class implements `Runnable`?**
- ✅ **Correct Answer:** B. `run()`
- 📖 **Explanation:** The `Runnable` interface is a built-in functional interface in Java containing exactly one abstract method: `public void run();`. A class implementing Runnable must provide a concrete implementation for `run()`.

---

### Quiz 3 (Runnable Interface Set) — What is Runnable?
**`Runnable` is:**
- ✅ **Correct Answer:** A. A built-in Java interface
- 📖 **Explanation:** `Runnable` is a native, pre-defined interface provided by the Java programming language (`java.lang.Runnable`). It separates task logic (the work to be done) from the execution vehicle (the Thread object running it).

---

### Quiz 1 (OS Scheduling Set) — Single-core concurrency
**On a single-core CPU, why do multiple applications appear to run together?**
- ✅ **Correct Answer:** C. The OS rapidly switches the CPU between applications
- 📖 **Explanation:** On a single core, only one execution instruction can occupy the physical CPU at any instant. The OS creates the illusion of simultaneous execution (concurrency) by utilizing rapid time-slicing and context switching between running tasks at incredibly high speeds.

---

### Quiz 2 (OS Scheduling Set) — Context switching
**Context switching means:**
- ✅ **Correct Answer:** B. Saving the current state of one task and switching CPU to another task
- 📖 **Explanation:** A context switch is the low-level OS operation where the CPU stops executing a current task, saves its volatile state information (registers, program counter, stack pointer) into its PCB, and loads the previously saved execution state of a different task so it can resume.

---

### Quiz 1 (Thread Fundamentals Set) — Unit of execution
**What is the actual unit that executes code?**
- ✅ **Correct Answer:** D. Thread
- 📖 **Explanation:** While a process acts as an overall resource-owning container, it does not execute code directly line-by-line. The thread is the absolute smallest, native unit of execution that physically processes instructions on the CPU.

---

### Quiz 2 (Thread Fundamentals Set) — Shared resources
**Threads of the same process usually share:**
- ✅ **Correct Answer:** A. Heap memory
- 📖 **Explanation:** Sibling threads within the same parent process share the process's joint address space, including the compiled code segment, open files, and the Heap memory pool where dynamic runtime objects reside. Each thread maintains its own private, isolated stack and program counter.

---

## 14. OS Concepts — Questions 1–100

### Syllabus Covered:
- Introduction to Operating Systems
- Process Management: Processes, Context Switch
- CPU Scheduling Algorithms
- CPU Scheduling Algorithms - Numericals
- Revisiting OOPS, Interfaces and Abstract Classes

---

**Q1.** A student runs a Java program that prints output on the screen. Which Operating System services may be involved?
A. Program execution  
B. I/O management  
C. File system management  
D. CPU scheduling  
**Correct Answers:** A, B, D

**Q2.** Which statements correctly describe an Operating System?
A. It acts as an interface between user programs and hardware  
B. It manages resources like CPU, memory, and files  
C. It is only used for writing Java code  
D. It helps run multiple programs efficiently  
**Correct Answers:** A, B, D

**Q3.** A program wants to create a new file and write data into it. Why does it need OS support?
A. File access is controlled by the OS  
B. Direct hardware access is usually protected  
C. The OS provides file-related services  
D. The program must manually rotate the disk  
**Correct Answers:** A, B, C

**Q4.** Which are examples of Operating System responsibilities?
A. Memory allocation  
B. CPU scheduling  
C. Error detection  
D. Writing problem statements for exams  
**Correct Answers:** A, B, C

**Q5.** Which statements about system calls are TRUE?
A. They allow programs to request OS services  
B. They help user programs access protected resources safely  
C. They are only used for printing comments  
D. File operations may require system calls  
**Correct Answers:** A, B, D

**Q6.** A user opens a browser, music player, and code editor together. What helps the system manage these applications?
A. CPU scheduling  
B. Process management  
C. Memory management  
D. Ignoring all background processes  
**Correct Answers:** A, B, C

**Q7.** A student saves a text file from a code editor. Which OS services are most directly involved?
A. File management  
B. I/O management  
C. Program execution  
D. Changing the Java class name automatically  
**Correct Answers:** A, B, C

**Q8.** Which of the following are examples of I/O devices managed by the OS?
A. Keyboard  
B. Mouse  
C. Printer  
D. Variable name inside Java code  
**Correct Answers:** A, B, C

**Q9.** Which statements about file management are TRUE?
A. The OS helps create files  
B. The OS helps delete files  
C. The OS manages directories  
D. The OS permanently prevents all file deletion  
**Correct Answers:** A, B, C

**Q10.** Which OS service is most directly involved when a program crashes due to illegal memory access?
A. Protection and security  
B. Error detection  
C. Process management  
D. Wallpaper management  
**Correct Answers:** A, B, C

**Q11.** Which statements about a Process are TRUE?
A. A process is a program in execution  
B. A process has its own state  
C. A process may have a Process Control Block  
D. A process is only a file stored on disk and never executes  
**Correct Answers:** A, B, C

**Q12.** Which items may be part of a process address space?
A. Code section  
B. Stack  
C. Heap  
D. Printer cable  
**Correct Answers:** A, B, C

**Q13.** Which statements about PCB are TRUE?
A. PCB stores important information about a process  
B. PCB may store process state  
C. PCB may store program counter information  
D. PCB stores the student's attendance percentage  
**Correct Answers:** A, B, C

**Q14.** A process is waiting for CPU time but is not currently executing. Which state is most suitable?
A. Ready  
B. Running  
C. Terminated  
D. New  
**Correct Answer:** A

**Q15.** A process is currently using the CPU. Which state is most suitable?
A. Running  
B. Waiting  
C. Ready  
D. Terminated  
**Correct Answer:** A

**Q16.** Which transitions may happen in a process lifecycle?
A. New to Ready  
B. Ready to Running  
C. Running to Terminated  
D. Terminated to Running automatically without creation  
**Correct Answers:** A, B, C

**Q17.** Which information is important during a context switch?
A. Program Counter  
B. CPU registers  
C. Process state  
D. Desktop wallpaper  
**Correct Answers:** A, B, C

**Q18.** Why does context switching create overhead?
A. CPU state must be saved  
B. Another process state must be restored  
C. Useful CPU execution time is spent in switching  
D. It permanently deletes the process  
**Correct Answers:** A, B, C

**Q19.** Which statements about a scheduler are TRUE?
A. It helps decide which ready process gets CPU  
B. It affects waiting time  
C. It affects response time  
D. It always executes processes alphabetically  
**Correct Answers:** A, B, C

**Q20.** Which statements correctly describe context switching on a single-core CPU?
A. Only one process runs at an exact instant  
B. The CPU may switch quickly between processes  
C. It can create an illusion of multitasking  
D. All processes execute truly parallel at the exact same instant  
**Correct Answers:** A, B, C

**Q21.** Which statements about FCFS Scheduling are TRUE?
A. Processes are executed in arrival order  
B. It is non-preemptive  
C. A long process can delay shorter processes  
D. It always gives the minimum average waiting time  
**Correct Answers:** A, B, C

**Q22.** Which statements about SJF Scheduling are TRUE?
A. It gives preference to shorter burst time processes  
B. It may reduce average waiting time  
C. Burst time estimation is important  
D. It always ignores burst time  
**Correct Answers:** A, B, C

**Q23.** Which statements about SRTF Scheduling are TRUE?
A. It is the preemptive version of SJF  
B. A newly arrived shorter job may preempt the running job  
C. Remaining burst time is considered  
D. Once a process starts, it can never be stopped  
**Correct Answers:** A, B, C

**Q24.** Which statements about Priority Scheduling are TRUE?
A. Processes are selected based on priority  
B. It may be preemptive or non-preemptive  
C. Starvation may occur in priority scheduling  
D. Priority values are never used in scheduling  
**Correct Answers:** A, B, C

**Q25.** Which statements about Round Robin Scheduling are TRUE?
A. It uses a time quantum  
B. It is preemptive  
C. It is commonly used for time-sharing systems  
D. It always behaves exactly like SJF  
**Correct Answers:** A, B, C

**Q26.** Which scheduling metric is calculated as CT − AT?
A. Turnaround Time  
B. Waiting Time  
C. Burst Time  
D. Response Time  
**Correct Answer:** A

**Q27.** Which scheduling metric is calculated as TAT − BT?
A. Waiting Time  
B. Completion Time  
C. Arrival Time  
D. Priority  
**Correct Answer:** A

**Q28.** Which statements about Burst Time are TRUE?
A. It represents CPU execution time required by a process  
B. It is important in SJF  
C. It is always equal to arrival time  
D. It may affect scheduling decisions  
**Correct Answers:** A, B, D

**Q29.** Which statements about Arrival Time are TRUE?
A. It tells when a process enters the ready queue  
B. It helps decide scheduling order  
C. It is always equal for all processes  
D. It is used while calculating turnaround time  
**Correct Answers:** A, B, D

**Q30.** Which statements about Completion Time are TRUE?
A. It tells when a process finishes execution  
B. It is used to calculate Turnaround Time  
C. It is always equal to Burst Time  
D. It may differ based on scheduling algorithm  
**Correct Answers:** A, B, D

**Q31.** Using FCFS Scheduling:
Process | AT | BT
P1 | 0 | 3
P2 | 1 | 4
P3 | 2 | 2
Which statements are TRUE?
A. Execution order is P1 → P2 → P3  
B. Completion Time of P1 is 3  
C. Completion Time of P3 is 9  
D. Waiting Time of P2 is 0  
**Correct Answers:** A, B, C

**Q32.** Using FCFS Scheduling:
Process | AT | BT
P1 | 0 | 5
P2 | 2 | 3
P3 | 4 | 1
Which statements are TRUE?
A. P1 completes at time 5  
B. P2 completes at time 8  
C. P3 completes at time 9  
D. Average Turnaround Time is 3  
**Correct Answers:** A, B, C

**Q33.** Using Non-Preemptive SJF Scheduling:
Process | AT | BT
P1 | 0 | 4
P2 | 1 | 2
P3 | 2 | 1
Which statements are TRUE?
A. P1 executes first  
B. P3 executes before P2  
C. Execution order is P1 → P3 → P2  
D. Completion Time of P2 is 7  
**Correct Answers:** A, B, C, D

**Q34.** Using Non-Preemptive SJF Scheduling:
Process | AT | BT
P1 | 0 | 6
P2 | 2 | 3
P3 | 3 | 2
P4 | 5 | 1
Which statements are TRUE?
A. P1 executes first  
B. After P1, P4 executes next  
C. Execution order is P1 → P4 → P3 → P2  
D. Completion Time of P2 is 12  
**Correct Answers:** A, B, C, D

**Q35.** Using SRTF Scheduling:
Process | AT | BT
P1 | 0 | 5
P2 | 1 | 2
P3 | 2 | 1
Which statements are TRUE?
A. P2 preempts P1 at time 1  
B. P3 preempts P2 at time 2  
C. P3 completes at time 3  
D. P1 completes before P2  
**Correct Answer:** A

**Q36.** Using SRTF Scheduling:
Process | AT | BT
P1 | 0 | 7
P2 | 2 | 4
P3 | 4 | 1
Which statements are TRUE?
A. P2 preempts P1 at time 2  
B. P3 executes before P2 completes  
C. P3 completes at time 5  
D. P1 completes first  
**Correct Answers:** A, B, C

**Q37.** Using Non-Preemptive Priority Scheduling (Higher number = Higher Priority)
Process | AT | BT | Priority
P1 | 0 | 4 | 2
P2 | 1 | 3 | 5
P3 | 2 | 2 | 3
Which statements are TRUE?
A. P1 executes first  
B. P2 executes after P1  
C. P3 executes before P2  
D. Completion Time of P3 is 9  
**Correct Answers:** A, B, D

**Q38.** Using Preemptive Priority Scheduling (Higher number = Higher Priority)
Process | AT | BT | Priority
P1 | 0 | 6 | 2
P2 | 1 | 3 | 4
P3 | 2 | 2 | 5
Which statements are TRUE?
A. P2 preempts P1  
B. P3 preempts P2  
C. P3 completes before P2  
D. P1 completes at time 11  
**Correct Answers:** A, B, C, D

**Q39.** Using Round Robin Scheduling (Time Quantum = 2)
Process | AT | BT
P1 | 0 | 4
P2 | 1 | 3
P3 | 2 | 2
Which statements are TRUE?
A. P1 executes more than once  
B. P3 completes in its first turn  
C. P2 gets CPU before P1 completes  
D. Context switching occurs  
**Correct Answers:** A, B, C, D

**Q40.** Using Round Robin Scheduling (Time Quantum = 3)
Process | AT | BT
P1 | 0 | 5
P2 | 1 | 4
Which statements are TRUE?
A. P1 first runs from 0 to 3  
B. P2 gets CPU before P1 completes  
C. P1 completes at time 8  
D. P2 completes at time 9  
**Correct Answers:** A, B, C, D

**Q41.** A class Animal has a method sound(). Class Dog extends Animal and overrides sound(). Which statements are TRUE?
A. Method overriding is shown  
B. Runtime polymorphism may be shown  
C. Dog can provide its own version of sound()  
D. This is an example of process scheduling  
**Correct Answers:** A, B, C

**Q42.** Which statements about Encapsulation are TRUE?
A. Data can be hidden using private variables  
B. Public methods may provide controlled access  
C. Encapsulation improves data protection  
D. Encapsulation means every variable must be public  
**Correct Answers:** A, B, C

**Q43.** A class Learner has a private variable marks and a public method getMarks(). Which OOPS concept is mainly shown here?
A. Encapsulation  
B. Controlled access to data  
C. Direct public exposure of all data  
D. CPU scheduling  
**Correct Answers:** A, B

**Q44.** Which statements about Inheritance are TRUE?
A. A child class can reuse parent class properties  
B. Inheritance supports code reuse  
C. Java supports multiple inheritance using classes  
D. extends keyword is used for class inheritance  
**Correct Answers:** A, B, D

**Q45.** Which statements about Abstract Classes are TRUE?
A. They can have abstract methods  
B. They can have normal methods  
C. They can have constructors  
D. They can always be directly instantiated  
**Correct Answers:** A, B, C

**Q46.** Which statements about Interfaces are TRUE?
A. They define a contract for classes  
B. A class uses implements to implement an interface  
C. Interface references can point to implementing class objects  
D. Interfaces are used only for CPU scheduling  
**Correct Answers:** A, B, C

**Q47.** A class Payment implements Payable. The interface Payable has a method pay(). Which statements are TRUE?
A. Payment must define pay()  
B. Payable can be used as a reference type  
C. This supports abstraction  
D. Payment cannot have any other method  
**Correct Answers:** A, B, C

**Q48.** Which statements about Polymorphism are TRUE?
A. Same method call can behave differently for different objects  
B. Parent reference can point to child object  
C. It supports flexible code design  
D. It means a class cannot have methods  
**Correct Answers:** A, B, C

**Q49.** An abstract class Course has one normal method showCourse() and one abstract method startClass(). Class JavaCourse extends Course. Which statements are TRUE?
A. JavaCourse must implement startClass() unless it is also abstract  
B. showCourse() can be reused by JavaCourse  
C. Course can be directly instantiated using new Course()  
D. Abstract classes can contain both normal and abstract methods  
**Correct Answers:** A, B, D

**Q50.** A class Shape has an abstract method area(). Circle and Rectangle extend Shape and define area(). Which statements are TRUE?
A. Shape is an abstract class  
B. Circle and Rectangle provide implementation of area()  
C. Shape reference can store Circle object  
D. Abstract classes cannot be used as reference types  
**Correct Answers:** A, B, C

**Q51.** Which statements about Dispatcher are TRUE?
A. Dispatcher gives CPU control to selected process  
B. Dispatcher performs context switching  
C. Dispatcher works with the scheduler  
D. Dispatcher permanently stores files on disk  
**Correct Answers:** A, B, C

**Q52.** Which statements about Non-Preemptive Scheduling are TRUE?
A. Running process keeps CPU until completion or waiting state  
B. FCFS is non-preemptive  
C. SJF may be non-preemptive  
D. CPU can interrupt the process anytime forcibly in pure non-preemptive scheduling  
**Correct Answers:** A, B, C

**Q53.** Which statements about Preemptive Scheduling are TRUE?
A. Running process may be interrupted  
B. Round Robin is preemptive  
C. SRTF is preemptive  
D. Preemptive scheduling never causes context switching  
**Correct Answers:** A, B, C

**Q54.** Which statements about Turnaround Time are TRUE?
A. It includes waiting time  
B. It includes execution time  
C. Lower turnaround time is generally desirable  
D. Turnaround Time always equals Burst Time  
**Correct Answers:** A, B, C

**Q55.** Which statements about Waiting Time are TRUE?
A. It represents time spent waiting for CPU  
B. It depends on scheduling algorithm  
C. Lower waiting time improves efficiency  
D. Waiting Time always equals Arrival Time  
**Correct Answers:** A, B, C

**Q56.** Using FCFS Scheduling:
Process | AT | BT
P1 | 0 | 2
P2 | 2 | 5
P3 | 4 | 1
Which statements are TRUE?
A. P1 completes at time 2  
B. P2 completes at time 7  
C. P3 completes at time 8  
D. P3 executes before P2  
**Correct Answers:** A, B, C

**Q57.** Using Non-Preemptive SJF Scheduling:
Process | AT | BT
P1 | 0 | 8
P2 | 1 | 3
P3 | 2 | 2
Which statements are TRUE?
A. P1 executes first  
B. P3 executes before P2  
C. Execution order is P1 → P3 → P2  
D. P2 completes at time 13  
**Correct Answers:** A, B, C, D

**Q58.** Using SRTF Scheduling:
Process | AT | BT
P1 | 0 | 4
P2 | 1 | 1
P3 | 2 | 2
Which statements are TRUE?
A. P2 preempts P1  
B. P2 completes at time 2  
C. P3 executes before P1 completes  
D. P1 completes first  
**Correct Answers:** A, B, C

**Q59.** Using Preemptive Priority Scheduling (Higher number = Higher Priority)
Process | AT | BT | Priority
P1 | 0 | 5 | 2
P2 | 2 | 2 | 6
Which statements are TRUE?
A. P2 preempts P1  
B. P2 completes before P1  
C. P1 runs continuously till completion  
D. Higher priority affects CPU allocation  
**Correct Answers:** A, B, D

**Q60.** Using Round Robin Scheduling (Time Quantum = 2)
Process | AT | BT
P1 | 0 | 3
P2 | 1 | 4
Which statements are TRUE?
A. P1 executes more than once  
B. P2 gets CPU before P1 completes  
C. Context switching occurs  
D. P1 completes in first quantum  
**Correct Answers:** A, B, C

**Q61.** A user clicks on an application icon and the application starts loading. Which OS activities may happen?
A. Loading the program into memory  
B. Creating a process  
C. Allocating required resources  
D. Manually changing the source code  
**Correct Answers:** A, B, C

**Q62.** Which statements about Resource Allocation are TRUE?
A. OS decides how CPU is shared among processes  
B. OS manages memory allocation  
C. OS may manage access to I/O devices  
D. OS gives every process unlimited resources  
**Correct Answers:** A, B, C

**Q63.** Which statements about Protection in an OS are TRUE?
A. It prevents one process from harming another process  
B. It controls access to system resources  
C. It allows every program to directly modify kernel data  
D. It improves system reliability  
**Correct Answers:** A, B, D

**Q64.** Which statements about the Command Line Interface are TRUE?
A. Users interact by typing commands  
B. It is one type of user interface provided by an OS  
C. It always requires clicking icons only  
D. It can be used to run programs  
**Correct Answers:** A, B, D

**Q65.** Which statements about Graphical User Interface are TRUE?
A. It allows interaction using windows and icons  
B. It is easier for many beginners to use  
C. It is not related to OS interaction at all  
D. It may internally trigger OS services  
**Correct Answers:** A, B, D

**Q66.** A process is created but has not yet been admitted to the ready queue. Which state best describes it?
A. New  
B. Running  
C. Waiting  
D. Terminated  
**Correct Answer:** A

**Q67.** A process has completed execution and released its resources. Which state best describes it?
A. Terminated  
B. Ready  
C. Running  
D. Waiting  
**Correct Answer:** A

**Q68.** Which statements about Process State are TRUE?
A. It helps the OS track what a process is doing  
B. It may change during execution  
C. It is stored as part of process-related information  
D. It always remains Running from start to finish  
**Correct Answers:** A, B, C

**Q69.** Which statements about Long-Term Scheduler are TRUE?
A. It controls admission of processes into the system  
B. It affects degree of multiprogramming  
C. It always selects the next process for immediate CPU execution  
D. It may decide which jobs enter the ready queue  
**Correct Answers:** A, B, D

**Q70.** Which statements about Short-Term Scheduler are TRUE?
A. It selects a process from the ready queue  
B. It decides which process gets CPU next  
C. It runs frequently  
D. It only manages files and folders  
**Correct Answers:** A, B, C

**Q71.** Which statements about Medium-Term Scheduler are TRUE?
A. It may swap processes out of memory  
B. It may reduce degree of multiprogramming temporarily  
C. It is related to process management  
D. It always performs Java method overriding  
**Correct Answers:** A, B, C

**Q72.** Which statements about CPU Burst are TRUE?
A. It is the time a process needs on CPU  
B. It is used in scheduling numericals  
C. It is always zero for every process  
D. It may vary from process to process  
**Correct Answers:** A, B, D

**Q73.** Which statements about I/O Burst are TRUE?
A. It is the time a process spends doing I/O activity  
B. A process may alternate between CPU burst and I/O burst  
C. It is unrelated to process execution  
D. Waiting for I/O may move a process out of Running state  
**Correct Answers:** A, B, D

**Q74.** Which statements about Response Time are TRUE?
A. It measures time from arrival to first CPU allocation  
B. It is important in interactive systems  
C. Lower response time is usually better  
D. It always equals completion time  
**Correct Answers:** A, B, C

**Q75.** Which statements about Gantt Charts in CPU Scheduling are TRUE?
A. They show execution order of processes  
B. They help calculate completion time  
C. They show time intervals for CPU allocation  
D. They are used only for inheritance diagrams  
**Correct Answers:** A, B, C

**Q76.** Using FCFS Scheduling:
Process | AT | BT
P1 | 0 | 4
P2 | 4 | 3
P3 | 5 | 2
Which statements are TRUE?
A. P1 completes at time 4  
B. P2 completes at time 7  
C. P3 completes at time 9  
D. P3 executes before P2  
**Correct Answers:** A, B, C

**Q77.** Using FCFS Scheduling:
Process | AT | BT
P1 | 2 | 3
P2 | 5 | 2
P3 | 6 | 1
Which statements are TRUE?
A. CPU remains idle from time 0 to 2  
B. P1 completes at time 5  
C. P2 completes at time 7  
D. P3 completes before P2  
**Correct Answers:** A, B, C

**Q78.** Using Non-Preemptive SJF Scheduling:
Process | AT | BT
P1 | 0 | 2
P2 | 1 | 6
P3 | 2 | 3
P4 | 3 | 1
Which statements are TRUE?
A. P1 executes first  
B. P4 executes immediately after P1  
C. Execution order is P1 → P4 → P3 → P2  
D. P2 completes at time 12  
**Correct Answers:** A, D

**Q79.** Using Non-Preemptive SJF Scheduling:
Process | AT | BT
P1 | 1 | 4
P2 | 2 | 2
P3 | 3 | 1
Which statements are TRUE?
A. CPU is idle from time 0 to 1  
B. P1 executes first  
C. P3 executes before P2  
D. Completion Time of P2 is 8  
**Correct Answers:** A, B, C, D

**Q80.** Using SRTF Scheduling:
Process | AT | BT
P1 | 0 | 5
P2 | 1 | 4
P3 | 2 | 1
Which statements are TRUE?
A. P1 is not preempted by P2 at time 1  
B. P3 preempts P1 at time 2  
C. P3 completes at time 3  
D. P2 completes before P1  
**Correct Answers:** A, B, C

**Q81.** Using SRTF Scheduling:
Process | AT | BT
P1 | 0 | 9
P2 | 3 | 2
P3 | 4 | 1
Which statements are TRUE?
A. P2 preempts P1 at time 3  
B. P3 preempts P2 at time 4  
C. P3 completes at time 5  
D. P1 completes before P2  
**Correct Answers:** A, B, C

**Q82.** Using Non-Preemptive Priority Scheduling (Higher number = Higher Priority)
Process | AT | BT | Priority
P1 | 0 | 3 | 1
P2 | 1 | 4 | 3
P3 | 2 | 2 | 5
Which statements are TRUE?
A. P1 executes first  
B. P3 executes after P1  
C. P2 executes after P3  
D. Completion Time of P2 is 9  
**Correct Answers:** A, B, C, D

**Q83.** Using Preemptive Priority Scheduling (Higher number = Higher Priority)
Process | AT | BT | Priority
P1 | 0 | 4 | 3
P2 | 1 | 5 | 2
P3 | 2 | 1 | 6
Which statements are TRUE?
A. P2 does not preempt P1 at time 1  
B. P3 preempts P1 at time 2  
C. P3 completes at time 3  
D. P1 completes before P3  
**Correct Answers:** A, B, C

**Q84.** Using Round Robin Scheduling (Time Quantum = 1)
Process | AT | BT
P1 | 0 | 2
P2 | 0 | 2
P3 | 0 | 1
Which statements are TRUE?
A. Each process gets CPU in turns  
B. P3 can complete in one CPU turn  
C. Time quantum is 1 unit  
D. Round Robin is non-preemptive here  
**Correct Answers:** A, B, C

**Q85.** Using Round Robin Scheduling (Time Quantum = 4)
Process | AT | BT
P1 | 0 | 3
P2 | 1 | 6
P3 | 2 | 2
Which statements are TRUE?
A. P1 completes in its first turn  
B. P2 does not complete in its first turn  
C. P3 completes in its first turn  
D. P2 needs another turn after its first quantum  
**Correct Answers:** A, B, C, D

**Q86.** Which statements about Class and Object are TRUE?
A. A class is a blueprint  
B. An object is an instance of a class  
C. Objects can have state and behavior  
D. A class and object always mean the same thing  
**Correct Answers:** A, B, C

**Q87.** Which statements about Constructor Overloading are TRUE?
A. A class may have multiple constructors  
B. Constructor parameter lists must differ  
C. It helps initialize objects in different ways  
D. Constructor overloading requires inheritance  
**Correct Answers:** A, B, C

**Q88.** Which statements about final methods in Java are TRUE?
A. A final method cannot be overridden  
B. A final method can still be called  
C. final methods are related to controlling inheritance behavior  
D. final methods must always be abstract  
**Correct Answers:** A, B, C

**Q89.** Which statements about super in method overriding are TRUE?
A. It can call the parent version of an overridden method  
B. It can be useful when child method wants to reuse parent behavior  
C. It refers to the current class object only  
D. It can access parent constructor using super()  
**Correct Answers:** A, B, D

**Q90.** Which statements about Interface Implementation are TRUE?
A. A concrete class implementing an interface must define its abstract methods  
B. The implements keyword is used  
C. One class can implement more than one interface  
D. Implementing an interface prevents object creation of the class  
**Correct Answers:** A, B, C

**Q91.** Which statements about Abstract Class References are TRUE?
A. An abstract class reference can point to a child object  
B. Abstract class references support polymorphism  
C. Abstract class objects can always be created directly  
D. Child overridden methods may run through parent reference  
**Correct Answers:** A, B, D

**Q92.** Which statements about Interface References are TRUE?
A. Interface reference can point to implementing class object  
B. Interface reference helps write flexible code  
C. Interface reference can call methods declared in interface  
D. Interface reference always stores only primitive values  
**Correct Answers:** A, B, C

**Q93.** A class Account keeps balance private and provides deposit() and getBalance(). Which statements are TRUE?
A. Encapsulation is shown  
B. Direct access to balance is restricted  
C. Public methods provide controlled access  
D. This is an example of Round Robin scheduling  
**Correct Answers:** A, B, C

**Q94.** A parent class Employee has method work(). Developer and Designer extend Employee and override work(). Which statements are TRUE?
A. Inheritance is shown  
B. Method overriding is shown  
C. Polymorphism can be achieved  
D. Employee cannot be used as a reference type  
**Correct Answers:** A, B, C

**Q95.** Which statements about Default Access Modifier are TRUE?
A. It is also called package-private access  
B. No access modifier keyword is written  
C. It allows access within the same package  
D. It allows access from all packages like public  
**Correct Answers:** A, B, C

**Q96.** Which statements about private members are TRUE?
A. They are accessible inside the same class  
B. They help in data hiding  
C. They can be accessed directly from any unrelated class  
D. They are commonly used in encapsulation  
**Correct Answers:** A, B, D

**Q97.** Which statements about protected members are TRUE?
A. They can be accessed inside the same package  
B. They can be accessed in subclasses under valid inheritance rules  
C. They are more restrictive than private in every situation  
D. They are related to access control  
**Correct Answers:** A, B, D

**Q98.** Which statements about Static Method Overriding are TRUE?
A. Static methods are not overridden like instance methods  
B. Static methods may be hidden in child class  
C. Runtime polymorphism mainly applies to overridden instance methods  
D. Static methods are always abstract  
**Correct Answers:** A, B, C

**Q99.** A class Report has a method print(). Another class DetailedReport extends Report and overrides print(). Which statement is TRUE?
A. DetailedReport can provide a specialized print() behavior  
B. Report must always be an interface  
C. print() cannot be called through a parent reference  
D. This example shows file allocation only  
**Correct Answer:** A

**Q100.** Which statements about choosing between Interface and Abstract Class are TRUE?
A. Use an interface when defining a common contract  
B. Use an abstract class when sharing common state and behavior  
C. A class can implement multiple interfaces  
D. A class can extend multiple classes directly in Java  
**Correct Answers:** A, B, C

---

## 14. Exam Notes

- Mid-semester covers: **Concurrency Class 1** (Introduction to Processes and Threads) + **OOPS paradigms**
- Exam structure:
  | Section | Quantity | Marks Each | Total |
  |---------|----------|------------|-------|
  | MCQs | 18 questions | 2 marks | 36 |
  | Coding Question (Q19) | 1 question | 10 marks | 10 |
  | Theory / Output / Numerical (Q20) | 1 question | 6 marks | 6 |
  | | | | **52 total** |
- No partial marking in exams.
- Practice sheet available in class handbook.
- This class content is **NOT** part of mid-sem; focus on **end-semester**.
- OOP pattern required for coding question (classes + objects for data storage).

---

*All notes compiled from Scaler Academy Concurrency 1 lecture, Companion materials, and quiz screenshots.*
