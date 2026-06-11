# Concurrency Problems & Synchronization — Notes

## 1. Multi-threaded Merge Sort (Java)

### Key Concepts
- Implementation using **ExecutorService**, **Callable** and **Future**
- Recursive splitting of array into two halves, each sorted by a separate thread
- Thread pool size: even number recommended (e.g., 4 threads) to match the divide-and-conquer structure
- Avoid creating too many → causes context switching overhead; avoid too few → no parallelism benefit

### Structure
1. **MergeSortTask** — implements `Callable<int[]>`
   - Constructor receives: `int[] arr`, `ExecutorService executor`
2. **call() method logic:**
   | Condition | Action |
   |---|---|
   | `arr.length <= 1` | Return array (already sorted) |
   | `arr.length <= 2` | Use `Arrays.copyOf()` + `Arrays.sort()` — no thread creation for small arrays |
   | Otherwise | Split into left/right halves → create two MergeSortTasks → submit to ExecutorService → retrieve results via `Future.get()` → merge sorted halves |
3. **merge() method** — standard merge of two sorted arrays using three pointers (i, j, k)

### Flow (Executor pattern — repeated in every concurrent task)
```
create callable → create task object → submit via executor → get result from future → shutdown executor (in main, not inside task)
```

### Input & Expected Output
- **Input:** `arr = {8, 3, 5, 1, 9, 2, 7, 4}`
- **Expected Output:** `[1, 2, 3, 4, 5, 7, 8, 9]`

### Key Java APIs Used
| API | Role |
|---|---|
| `ExecutorService` | Thread pool manager — prevents thread creation overhead per recursive call |
| `Callable<int[]>` | Task that **returns** a result (unlike Runnable which is void) |
| `Future<int[]>` | Placeholder for the result — retrieved synchronously via `.get()` |
| `Executors.newFixedThreadPool(n)` | Creates a reusable pool of exactly *n* threads |
| `Arrays.copyOfRange(arr, from, to)` | Splits array into left/right halves for recursive calls |

### Important Design Decisions
| Decision | Reason |
|---|---|
| Use `Callable<int[]>` not `Runnable` | Task must return a sorted `int[]` result |
| Use `Future.get()` | Sorting is asynchronous — `.get()` blocks until result is ready |
| Base case at `arr.length <= 2` | Avoids thread creation overhead for trivially small arrays |
| Thread pool size = 4 (not unlimited) | Reuses threads; prevents resource exhaustion from deep recursion |

### Complete Code

```java
import java.util.Arrays;
import java.util.concurrent.*;

class MergeSortTask implements Callable<int[]> {

    int[] arr;
    ExecutorService executor;

    MergeSortTask(int[] arr, ExecutorService executor) {
        this.arr = arr;
        this.executor = executor;
    }

    @Override
    public int[] call() throws Exception {

        // Base case: sort directly to avoid excessive thread creation
        if (arr.length <= 1) {
            return arr;
        }
        if (arr.length <= 2) {
            int[] copy = Arrays.copyOf(arr, arr.length);
            Arrays.sort(copy);
            return copy;
        }

        // Divide
        int mid = arr.length / 2;
        int[] left = Arrays.copyOfRange(arr, 0, mid);
        int[] right = Arrays.copyOfRange(arr, mid, arr.length);

        // Conquer (in parallel)
        MergeSortTask leftTask = new MergeSortTask(left, executor);
        MergeSortTask rightTask = new MergeSortTask(right, executor);

        Future<int[]> leftFuture = executor.submit(leftTask);
        Future<int[]> rightFuture = executor.submit(rightTask);

        // Combine (wait for both halves)
        int[] sortedLeft = leftFuture.get();
        int[] sortedRight = rightFuture.get();

        return merge(sortedLeft, sortedRight);
    }

    private static int[] merge(int[] left, int[] right) {
        int[] result = new int[left.length + right.length];
        int i = 0, j = 0, k = 0;

        while (i < left.length && j < right.length) {
            if (left[i] <= right[j]) {
                result[k++] = left[i++];
            } else {
                result[k++] = right[j++];
            }
        }
        while (i < left.length) result[k++] = left[i++];
        while (j < right.length) result[k++] = right[j++];

        return result;
    }
}

public class Main {
    public static void main(String[] args) throws Exception {
        int[] arr = {8, 3, 5, 1, 9, 2, 7, 4};
        ExecutorService executor = Executors.newFixedThreadPool(4);
        MergeSortTask mainTask = new MergeSortTask(arr, executor);
        Future<int[]> finalFuture = executor.submit(mainTask);
        int[] sortedArray = finalFuture.get();
        System.out.println(Arrays.toString(sortedArray));
        executor.shutdown();
    }
}
```

---

## 2. Shared Resource

- A shared resource is any data/object accessed by multiple threads simultaneously.
- **Examples:** Bank account balance, movie booking seats, product stock on a shopping website.
- Sharing itself is **not wrong** — it enables lightweight processes and efficient communication.
- Problem arises when access is **not coordinated** among threads.

---

## 3. The Payment Problem (Wallet)

### Scenario
- Wallet balance: **1000 rupees**
- Thread T1 wants to pay **700** (course payment)
- Thread T2 wants to pay **500** (book payment)
- Without synchronization, both can get approved simultaneously → final balance = **–200**

### Answers to the Three Questions

| Question | Answer |
|---|---|
| Can both payments get approved? | **Yes** — without synchronization, both threads read balance = 1000 simultaneously, both pass the check, and both get approved. |
| Can the final balance become negative? | **Yes** — both approve (700 + 500 deducted) → `1000 - 700 - 500 = –200`. |
| Why is this happening? | Because the check-then-deduct sequence in `pay()` is **non-atomic**. Thread A reads balance, gets preempted, Thread B reads same balance, both proceed. This is a **race condition** caused by preemption inside a critical section with no synchronization. |

---

## 4. Critical Section

- A **critical section** is the portion of code where shared data is **accessed or modified**.
- The `pay()` method (check balance → approve → deduct) is the critical section.
- If two threads enter simultaneously, results are guaranteed to be incorrect.

---

## 5. Race Condition

When multiple threads access shared data and the final result depends on the **timing / order** of execution.

### Example — Payment Problem
| Execution Order | Balance After Course (700) | Balance After Book (500) |
|---|---|---|
| Course first | 300 → Book fails | 300 |
| Book first | 500 → Course fails | 500 |

- Output is timing-dependent → a program must work **regardless** of thread order.
- Caused by **preemption** inside a critical section.

---

## 6. Atomic vs Non-Atomic Operations

| Type | Description | Example |
|---|---|---|
| **Atomic** | Happens in one unbreakable step. Preemption doesn't matter. | `a = 5` (single-step write), print statements |
| **Non-Atomic** | Comprises multiple steps. Thread can be preempted at any step. | `balance = balance - amount` → read → subtract → write |

### Why `count++` Is Not Thread-Safe — The CPU-Level Detail

Though written as a single line of high-level code, `count++` is compiled into **three distinct, non-atomic CPU operations**:

1. **Read:** The CPU copies the current value of `count` from main memory into a thread's private register.
2. **Modify:** The CPU increments the register value by 1.
3. **Write:** The CPU copies the updated value from the private register back into main memory.

### The Preemption Problem Walkthrough

The OS scheduler can suspend (preempt) a thread at any microscopic instant, saving its register context and giving the CPU core to another thread:

- **Thread A** reads `count = 10` and gets preempted before it can write back — its register holds `11`.
- **Thread B** runs, reads `count = 10`, increments it, and writes `11` back to main memory.
- **Thread A** resumes and blindly completes its write phase, pushing `11` into memory again.
- **Result:** Two increments occurred, but the value only increased by one. This is known as a **lost update**.

### Lost Update Problem
Two threads read the same value, both increment it → only one update survives.

**Counters Example: adder + subtractor (each loop 10,000 times)**
- Expected final result: **0**
- Actual result: **any random value** (e.g., 110, –87) due to lost updates
- `count++` is **not atomic**: read → increment → write

---

## 7. The Need for Synchronization

Ensures threads in a critical section coordinate their reads/writes so that concurrency problems do not occur.

### Problems Indicate Synchronization Needed When:
1. Two or more threads share a critical section
2. Non-atomic operations mutate shared data
3. Preemption is possible at any point
4. Output depends on thread timing/order

---

## 8. Properties of a Good Synchronization Solution

| Property | Meaning |
|---|---|
| **Mutual Exclusion** | Only one thread enters the critical section at a time |
| **Progress** | Critical section must not stay empty while threads wait — any waiting thread gets in |
| **Bounded Waiting** | Every thread eventually gets a chance; no starvation |
| **No Busy Waiting** (desired) | Thread should sleep/wait rather than loop checking repeatedly (busy loop wastes CPU) |

---

## 9. The `synchronized` Keyword (Java)

Every Java object has an **automatic internal lock** (mutex lock).

### Level 1 — Synchronized Method
```java
public synchronized void pay(String name, int amount) {
    // Entire method becomes critical section
}
```
- One object → one lock. When T1 enters, T2 **waits** (not busy-loop checks).
- On T1's exit, the lock is released and T2 acquires it.

### Level 2 — Synchronized Block (more granular)
```java
public void methodName() {
    // Not part of critical section
    synchronized(this) {
        // Only this block is the critical section
    }
}
```
- **Preferred** in practice: makes only the sensitive portion critical → keeps concurrency for other parts.

### ⚠️ Important Rule
Locks are per-object. Using **two different objects** → two independent locks → **no synchronization**. Must share a single object.

---

## 10. Payment Problem — Wallet (Template & Solution)

### Template (with TODOs)

```java
class Wallet {
    int balance = 1000;
    void pay(String paymentName, int amount) {

        // check if wallet has enough balance

            // print payment approved message

            // deduct amount from balance

            // print payment completed message

        // otherwise

            // print payment failed message
    }
}

class PaymentTask implements Runnable {

    Wallet wallet;
    String paymentName;
    int amount;

    PaymentTask(Wallet wallet, String paymentName, int amount) {
        // initialize wallet, paymentName, amount
    }

    public void run() {
        // call pay method using wallet object
    }
}

public class Main {

    public static void main(String[] args) throws InterruptedException {
        // create one shared Wallet object
        // create Course payment thread
        // create Book payment thread
        // start both threads
        // wait for both to finish (join)
        // print final wallet balance
    }
}
```

### Solution

```java
class Wallet {
    int balance = 1000;
    synchronized void pay(String paymentName, int amount) {
        if(balance >= amount){
            System.out.println(paymentName + " has been approved");
            balance = balance - amount;
            System.out.println(paymentName + " has been completed");
        } else {
            System.out.println(paymentName + " has failed");
        }
    }
}

class PaymentTask implements Runnable {

    Wallet wallet;
    String paymentName;
    int amount;

    PaymentTask(Wallet wallet, String paymentName, int amount) {
        this.wallet = wallet;
        this.paymentName = paymentName;
        this.amount = amount;
    }

    public void run() {
        wallet.pay(paymentName, amount);
    }
}

public class Main {

    public static void main(String[] args) throws InterruptedException {
        Wallet wallet = new Wallet();

        Thread coursePayment = new Thread(new PaymentTask(wallet, "Course", 700));
        Thread bookPayment   = new Thread(new PaymentTask(wallet, "Book", 500));

        coursePayment.start();
        bookPayment.start();

        coursePayment.join();
        bookPayment.join();

        System.out.println("Final Balance: " + wallet.balance);
    }
}
```

---

## 11. Fixing the Problems With `synchronized`

| Problem | Fix |
|---|---|
| Unsafe wallet payment → double approvals | Add `synchronized` to `pay()` method or critical block. Course-approved, Book-fails → final balance = 300 (consistent every run). |
| Adder-Subtractor → random values | Synchronize the entire `value++` / `value--` operation or use synchronized blocks around the critical section. Final value = 0 consistently. |

---

## 12. Busy Waiting vs. Mutex Locks

### Busy Waiting
- **Mechanism:** A thread repeatedly runs a loop checking a condition to see if a critical section is free.
- **Downside:** Wastes massive amounts of CPU clock cycles spinning in a loop doing no real work, heavily reducing system efficiency.

### Mutex Lock (Mutual Exclusion Lock)
- **Mechanism:** A strict, abstract key-based synchronization mechanism.
- **The Flow:**
  1. A thread must successfully acquire the unique key before entering the critical section.
  2. If the key is held by another thread, the arriving thread is put to sleep by the OS and placed into a waiting queue.
  3. When the holding thread finishes, it releases the key.
  4. The OS wakes up a waiting thread from the queue.
- **Advantage:** Eliminates CPU-wasting loops — threads sleep efficiently while waiting.

---

## 13. Exam Practice Problem — Movie Ticket Booking

### Problem Statement
- Theater has **1000 tickets**.
- Multiple **booking agents** (threads) try to book tickets simultaneously.
- Each agent wants to book **1 ticket at a time**.
- Without synchronization, two agents may sell the same ticket — double booking occurs.
- **Solution:** Use a `synchronized` block around ticket booking logic to ensure atomicity.

### Template (with TODOs)

```java
class TicketCounter {
    int tickets = 1000;

    void bookTicket(String agentName) {
        // check if tickets > 0
            // book ticket: decrement tickets, print booking message
        // otherwise
            // print no tickets available message
    }
}

class BookingAgent implements Runnable {
    TicketCounter counter;
    String agentName;

    BookingAgent(TicketCounter counter, String agentName) {
        // initialize fields
    }

    public void run() {
        // call bookTicket on counter
    }
}

public class Main {
    public static void main(String[] args) throws InterruptedException {
        // create shared TicketCounter
        // create 3 BookingAgent threads (agents A, B, C)
        // start all threads
        // join all threads
        // print remaining tickets
    }
}
```

### Solution

```java
class TicketCounter {
    int tickets = 1000;

    void bookTicket(String agentName) {
        synchronized(this) {
            if (tickets > 0) {
                System.out.println(agentName + " booked ticket. Remaining: " + (tickets - 1));
                tickets--;
            } else {
                System.out.println("Sorry " + agentName + ", no tickets available");
            }
        }
    }
}

class BookingAgent implements Runnable {
    TicketCounter counter;
    String agentName;

    BookingAgent(TicketCounter counter, String agentName) {
        this.counter = counter;
        this.agentName = agentName;
    }

    public void run() {
        counter.bookTicket(agentName);
    }
}

public class Main {
    public static void main(String[] args) throws InterruptedException {
        TicketCounter ticketCounter = new TicketCounter();

        Thread agentA = new Thread(new BookingAgent(ticketCounter, "Agent A"));
        Thread agentB = new Thread(new BookingAgent(ticketCounter, "Agent B"));
        Thread agentC = new Thread(new BookingAgent(ticketCounter, "Agent C"));

        agentA.start();
        agentB.start();
        agentC.start();

        agentA.join();
        agentB.join();
        agentC.join();

        System.out.println("Tickets remaining: " + ticketCounter.tickets);
    }
}
```

### Answers to Key Questions

| Question | Answer |
|---|---|
| **Why is synchronization needed here?** | Multiple agents (threads) access and modify the shared `tickets` variable simultaneously. Without sync, two agents could read the same remaining ticket count and both book it — double booking. |
| **What is the critical section?** | The check-then-decrement of `tickets`: reading `tickets`, checking if > 0, then decrementing. This sequence is non-atomic and must be protected. |
| **Why `synchronized(this)` inside `bookTicket()` instead of `synchronized` on the method?** | Using a synchronized block inside the method is more granular — it only protects the sensitive portion. If we synced the whole method, any other logic added later would also be blocked unnecessarily. |
| **What happens if `synchronized(this)` is removed?** | Thread A reads `tickets = 5`, gets preempted. Thread B reads `tickets = 5` too, both decrement to 4 from the same check — one ticket is double-sold. Output becomes unpredictable. |
| **Why do we use the same object (`TicketCounter`) across all threads?** | Synchronization works by locking an object's intrinsic monitor. All three agents share one `TicketCounter` instance → one lock → mutual exclusion is enforced correctly across all threads. |
| **What would happen with multiple TicketCounter instances?** | Each new `TicketCounter` has its own independent lock → threads contend for different locks → no synchronization between them → double booking still possible. |

### Contrast: Without vs With Synchronization

| Aspect | Without `synchronized` | With `synchronized` |
|---|---|---|
| Ticket count | Can go **negative** (double-selling) | Never goes below 0 |
| Predictability | Unpredictable, timing-dependent | Consistent every run |
| Root cause | Race condition on decrement | Mutual exclusion enforced |

---

---

## 14. Race Condition — Adder & Subtractor (Full Worked Example)

### Problem Statement
You are given a shared `Count` object with an initial value of **0**.

- **Adder thread**: increases `count.value` **10,000 times**
- **Subtractor thread**: decreases `count.value` **10,000 times**
- Both threads work on the **same** `Count` object

### Expected Output
Final value should be: **0** (because +10,000 − 10,000 = 0)

### Observed Output
Running the program multiple times produces **random values** (e.g., 110, −87, 324) instead of 0.

---

### Template (with TODOs)

```java
class Count {
    int value = 0;
}

class Adder implements Runnable {
    Count count;

    Adder(Count count) {
        // write code to store the shared Count object
    }

    public void run() {
        // write code to add 1 to count.value 10000 times
    }
}

class Subtractor implements Runnable {
    Count count;

    Subtractor(Count count) {
        // write code to store the shared Count object
    }

    public void run() {
        // write code to subtract 1 from count.value 10000 times
    }
}

public class Main {
    public static void main(String[] args) throws InterruptedException {
        // write code to create Count object
        Count count;

        // write code to create Adder thread
        Thread adderThread;

        // write code to create Subtractor thread
        Thread subtractorThread;

        // write code to start both threads

        // write code to wait for both threads to finish

        // write code to print final value
    }
}
```

---

### Solution

```java
class Count {
    int value = 0;
}

class Adder implements Runnable {
    Count count;

    Adder(Count count) {
        this.count = count;
    }

    public void run() {
        for (int i = 1; i <= 10000; i++) {
            count.value++;
        }
    }
}

class Subtractor implements Runnable {
    Count count;

    Subtractor(Count count) {
        this.count = count;
    }

    public void run() {
        for (int i = 1; i <= 10000; i++) {
            count.value--;
        }
    }
}

public class Main {
    public static void main(String[] args) throws InterruptedException {
        Count count = new Count();
        Thread adderThread = new Thread(new Adder(count));
        Thread subtractorThread = new Thread(new Subtractor(count));

        adderThread.start();
        subtractorThread.start();

        adderThread.join();
        subtractorThread.join();

        System.out.println("Final value: " + count.value);
    }
}
```

---

### Answers to Key Questions

| Question | Answer |
|---|---|
| **Is the final value always 0?** | **No.** It is a random non-zero value each run. |
| **If not, why does the value change?** | Because of a **race condition** — multiple threads access and modify shared data concurrently without coordination, leading to lost updates. |
| **Which variable is shared between both threads?** | `count.value` (the `Count` object shared via constructor by both `Adder` and `Subtractor`) |
| **Which lines are causing the race condition?** | `count.value++` in `Adder.run()` and `count.value--` in `Subtractor.run()` |
| **Why are `count.value++` and `count.value--` not atomic?** | Each compiles to three CPU-level steps: **read** (load from memory → register), **modify** (increment/decrement in register), **write** (store back to memory). Preemption can occur between any of these steps. |
| **How can we make this code thread-safe?** | Use `synchronized` on the method or critical block, or use `java.util.concurrent.atomic.AtomicInteger`: <br>`AtomicInteger value = new AtomicInteger(0);`<br>`value.incrementAndGet();` / `value.decrementAndGet();` — these are atomic at the hardware level. |

---

### Solution 2: Synchronized Methods on Count Class

```java
class Count {
    int value = 0;
    
    synchronized void increment(){
        value++;
    }
    
    synchronized void decrement(){
        value--;
    }
}

class Adder implements Runnable {
    Count count;

    Adder(Count count) {
        this.count = count;
    }

    public void run() {
        for (int i = 1; i <= 10000; i++) {
            count.increment();
        }
    }
}

class Subtractor implements Runnable {
    Count count;

    Subtractor(Count count) {
        this.count = count;
    }

    public void run() {
        for (int i = 1; i <= 10000; i++) {
            count.decrement();
        }
    }
}

public class Main {
    public static void main(String[] args) throws InterruptedException {
        Count count = new Count();
        Thread adderThread = new Thread(new Adder(count));
        Thread subtractorThread = new Thread(new Subtractor(count));

        adderThread.start();
        subtractorThread.start();

        adderThread.join();
        subtractorThread.join();

        System.out.println("Final value: " + count.value);
    }
}
```

### Comparison of Two Solutions

| Approach | How It Works | When to Prefer |
|---|---|---|
| `synchronized(count)` block around the operation | Locks shared object directly; multiple threads contend for same lock | When you only need to protect specific lines, not the whole method |
| Synchronized methods (`increment` / `decrement`) | Each call acquires the `Count` object's intrinsic lock | When operations should always be synchronized together — encapsulates synchronization in the class |

---

## 15. Wallet Payment With `synchronized` — Full Q&A Analysis

### Scenario (recap)
- Shared Wallet with initial balance: **1000**
- Thread 1: Course payment tries to deduct **700**
- Thread 2: Book payment tries to deduct **500**
- Total requested: **1200** > available **1000**

### Expected Behavior
Both payments should **not** be fully successful. Only one payment completes; the other fails due to insufficient balance. Final balance is either **300** (Course first) or **500** (Book first).

### Corrected Code (with `synchronized`)

```java
class Wallet {
    int balance = 1000;

    synchronized void pay(String paymentName, int amount) {
        if (balance >= amount) {
            System.out.println(paymentName + " has been approved");
            balance = balance - amount;
            System.out.println(paymentName + " has been completed");
        } else {
            System.out.println(paymentName + " has failed");
        }
    }
}

class PaymentTask implements Runnable {
    Wallet wallet;
    String paymentName;
    int amount;

    PaymentTask(Wallet wallet, String paymentName, int amount) {
        this.wallet = wallet;
        this.paymentName = paymentName;
        this.amount = amount;
    }

    public void run() {
        wallet.pay(paymentName, amount);
    }
}

public class Main {
    public static void main(String[] args) throws InterruptedException {
        Wallet wallet = new Wallet();

        Thread coursePayment = new Thread(new PaymentTask(wallet, "Course", 700));
        Thread bookPayment   = new Thread(new PaymentTask(wallet, "Book", 500));

        coursePayment.start();
        bookPayment.start();

        coursePayment.join();
        bookPayment.join();

        System.out.println("Final Balance: " + wallet.balance);
    }
}
```

### Answers to Key Questions

| Question | Answer |
|---|---|
| **Why is the final balance always safe?** | `synchronized` ensures the check-then-deduct sequence in `pay()` is **atomic** — no other thread can read or modify `balance` while one thread is inside `pay()`. The balance never goes negative. One payment gets approved, the other fails. |
| **What does `synchronized` do in the `pay()` method?** | It turns the entire method body into a **critical section**. Only one thread can execute `pay()` on a given `Wallet` object at any time. Other threads attempting to call `pay()` on the same object are blocked (put to sleep) until the lock is released. |
| **Which object's lock is used here?** | The **`Wallet` object's** intrinsic lock (monitor). Since both `PaymentTask` instances share the same `wallet` reference, they contend for the same lock. |
| **Why can only one thread execute `pay()` at a time?** | Because `synchronized` acquires the `Wallet` object's intrinsic mutex lock before entering the method and releases it upon exit (even if an exception occurs). The JVM prevents another thread from acquiring the same lock simultaneously, enforcing mutual exclusion. |
| **What is the critical section in this code?** | The entire body of `pay()` — specifically the sequence: (1) read `balance`, (2) compare with `amount`, (3) deduct if sufficient. Without synchronization, preemption between steps 1 and 3 causes the race condition. `synchronized` makes this full sequence indivisible. |
| **What would happen if `synchronized` was removed?** | Both threads could enter `pay()` simultaneously. Both read `balance = 1000`, both pass the check, both get approved → balance becomes `-200`. This is a **race condition** with a final balance that can go negative. Output becomes unpredictable and timing-dependent. |

### Example Outputs

**Scenario A — Course runs first:**
```
Course has been approved
Course has been completed
Book has failed
Final Balance: 300
```

**Scenario B — Book runs first:**
```
Book has been approved
Book has been completed
Course has failed
Final Balance: 500
```

### Contrast: Without `synchronized`

| Aspect | Without `synchronized` | With `synchronized` |
|---|---|---|
| Final balance | Can be **–200** (both approved) | Always **300** or **500** (only one approved) |
| Predictability | Timing-dependent, unpredictable | Consistent, safe every run |
| Root cause | Race condition + lost update | Mutual exclusion enforced |

---

## Key Takeaways

1. Threads enable concurrency but introduce risks when sharing data without coordination.
2. **Preemption + shared critical section = race condition, lost update, inconsistency.**
3. Every multi-threaded program needs synchronization.
4. `synchronized` (method or block) provides mutex locks for mutual exclusion at no extra code.
5. Prefer synchronized blocks over full-method sync for better concurrency.
6. Always use the **same object** for locking; never multiple independent objects.
7. Future topics: semaphores and additional synchronization mechanisms beyond mutex locks.

---

## Quiz Answers

### Quiz 1: What is a shared resource?
**Answer:** A resource accessed by multiple threads simultaneously
- See Section 2 (Shared Resource) for detailed explanation and examples

### Quiz 2: What is a critical section?
**Answer:** The part of the code that accesses a shared resource
- See Section 4 (Critical Section) for detailed explanation

### Quiz 3: What is a race condition?
**Answer:** A condition where the output depends on thread execution order
- See Section 5 (Race Condition) for detailed explanation with the payment problem example

### Quiz 4: Why is count++ not thread-safe?
**Answer:** Because it consists of three separate, non-atomic operations
- **Read:** CPU copies value from main memory to a private register
- **Modify:** CPU increments the value in the register
- **Write:** CPU copies the updated value back to main memory
- A thread can be preempted between these steps, causing lost updates
- See Section 6 (Atomic vs Non-Atomic Operations) for the full walkthrough with the preemption problem

---

## Glossary of Terms

Term | Meaning
Race Condition | Concurrency issue where the output depends on the timing or order of thread execution.
Synchronization | Technique to ensure that multiple threads access shared resources without conflict.
Critical Section | Part of the program where shared resources are accessed or modified.
Executor Service | Framework in Java to manage and control thread pools effectively.
Thread Pool | Collection of threads that can be reused to perform multiple tasks in parallel.
Future.get() | Method to wait and retrieve the result of a computation once it's done.
Mutex Lock | Lock mechanism allowing only one thread to access a resource at a time; key-based sleep/wake system that eliminates busy-waiting loops.
Atomic Operation | Operation that runs completely independently of any other operations and is executed in a single step.
Preemption | Temporarily stopping a task to allow another to execute, used in multitasking by the OS scheduler.
Shared Resource | An object or variable that multiple threads can access simultaneously.
Synchronization Block | A method to only synchronize specific sections of code rather than entire methods.
Lost Update | Bug where two threads read the same value and both update it, causing one update to be silently ignored.
Busy Waiting | Inefficient pattern where a thread loops checking a condition, wasting CPU cycles instead of sleeping.
Intrinsic Lock (Monitor Lock) | Every Java object has an automatic internal lock; synchronized code uses this lock for mutual exclusion.
