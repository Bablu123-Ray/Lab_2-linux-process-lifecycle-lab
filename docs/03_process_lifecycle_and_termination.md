# Section 3: Process Lifecycle, Termination, and Kernel Cleanup

An active Linux process transitions through multiple execution states during its lifecycle until it meets a termination condition.

---

## 1. Process States in the Linux Kernel

When monitored via `ps aux` or `top`, processes display an execution status code:

| State Code | Name | Description |
|---|---|---|
| `R` | **Running / Runnable** | Process is currently executing on a CPU core or sitting in the OS run queue ready to be scheduled. |
| `S` | **Interruptible Sleep** | Process is blocked waiting for an event (e.g., I/O operation, user input, timer expiration via `sleep()`). Wakes up upon receiving signals. |
| `D` | **Uninterruptible Sleep** | Blocked waiting for critical hardware I/O (e.g., disk sector read). Cannot be interrupted even by `kill -9`. |
| `T` | **Stopped / Traced** | Process execution is suspended by a signal (e.g., `SIGTSTP` / `Ctrl+Z`) or an attached debugger (`gdb`). |
| `Z` | **Zombie** | The process has completed execution, but its parent has not yet called `wait()`/`waitpid()` to read its exit status. Retains a tiny task struct entry in the process table. |

---

## 2. Process Termination Causes

A process continues executing line-by-line until one of three conditions occurs:

| Termination Type | Trigger Mechanism | Representative Example | Resulting Signal / Exit Code |
|---|---|---|---|
| **1. Normal Exit** | Function return from `main()` or explicit invocation of `exit(int status)` system call. | `return 0;` or `exit(1);` | Returns exit status (0-255) to parent process. |
| **2. Signal Interrupt** | External asynchronous interrupt originating from the OS kernel or user input. | `Ctrl+C` keyboard press or `kill -9 <PID>` | Terminates via `SIGINT` (Signal 2) or `SIGKILL` (Signal 9). |
| **3. Abnormal Crash** | Execution of an invalid CPU instruction, illegal memory access, or arithmetic fault. | Dereferencing `NULL` pointer, buffer overflow, or division by zero. | Generates `SIGSEGV` (Segmentation Fault) or `SIGFPE` (Floating Point Exception). |

---

## 3. Kernel Cleanup Protocol

When any process terminates, the operating system kernel reclaims all associated resources to prevent system degradation:

1. **Memory Deallocation**: All virtual memory pages assigned to the process (Code, Data, Heap, Stack) are freed and unmapped from the MMU page tables.
2. **File Descriptor Teardown**: Open files, network sockets, and standard streams (`stdin`, `stdout`, `stderr`) are closed.
3. **Exit Status Notification**: The process exit code (or terminating signal number) is packaged and stored in the kernel process table, ready to be collected by the parent process using `wait()` or `waitpid()`. In the shell, this is accessible via `$?`.
4. **Process Table Deletion**: Once the parent acknowledges the exit status, the process's PID is freed and made available for future processes.
