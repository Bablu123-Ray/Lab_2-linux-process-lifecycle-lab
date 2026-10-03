# Section 4: Operating Systems Knowledge Assessment

This document answers all 15 evaluation questions presented in Lecture 2 (Slide 23) covering process fundamentals, lifecycle stages, and OS interaction.

---

### Q1: What is the difference between source code and an executable?
* **Answer**: **Source code** is human-readable text authored in a high-level programming language (such as C) containing logic, statements, and comments. An **executable** is a machine-readable binary file created by a compiler and linker containing raw machine CPU instructions (0s and 1s), data segments, and ELF metadata that hardware can execute directly.

### Q2: What command compiles a C program?
* **Answer**: The `gcc` (GNU Compiler Collection) or `clang` command. For example:
  ```bash
  gcc program.c -o program
  ```

### Q3: What is a process?
* **Answer**: A **process** is an active program in execution. While a program is a passive entity stored on disk, a process is an active, dynamic entity loaded into main memory (RAM) with dedicated CPU registers, memory segments (Text, Data, BSS, Heap, Stack), and system resources managed by the OS kernel.

### Q4: What does PID stand for?
* **Answer**: **PID** stands for **Process Identifier**. It is a unique integer assigned by the operating system kernel to each active process for identification, tracking, resource accounting, and signal dispatching.

### Q5: How do you check the exit code of the last command?
* **Answer**: In Unix/Linux shells (such as Bash, Zsh, or sh), you evaluate the special parameter `$?`:
  ```bash
  echo $?
  ```

### Q6: What does `return 0;` mean in `main()`?
* **Answer**: In C and Unix systems programming, `return 0;` communicates to the operating system that the program has concluded its execution **successfully without any errors**. Any non-zero return value (e.g., `1`, `2`) signifies an error or atypical termination status.

### Q7: What system call creates a new process?
* **Answer**: The `fork()` system call (or `clone()` in Linux kernel internals). When invoked, `fork()` creates an exact replica child process of the calling parent process.

### Q8: What system call replaces current process with a new program?
* **Answer**: The `execve()` system call (along with its standard C wrapper family: `execl`, `execv`, `execvp`, `execvpe`). `execve()` completely replaces the current process address space, code, and data with a new executable program from disk.

### Q9: How do you see running processes in terminal?
* **Answer**: By using process monitoring utilities such as `ps` (e.g., `ps aux` or `ps -ef`), `top`, or `htop`.

### Q10: What happens to memory when a process ends?
* **Answer**: When a process ends, the operating system kernel immediately deallocates and reclaims all virtual memory pages assigned to the process (Text, Data, Heap, and Stack), unmaps them from the hardware Page Tables (MMU), and returns the physical memory frames back to the available OS memory pool.

### Q11: Where is your program stored before execution?
* **Answer**: Before execution, your program is stored as an inactive, persistent file on secondary non-volatile storage (such as a Hard Disk Drive or Solid State Drive).

### Q12: Where is your program stored during execution?
* **Answer**: During execution, the program is mapped into volatile **main memory (RAM)**, structured within its private virtual address space consisting of Text, Data, BSS, Heap, and Stack segments.

### Q13: Why does the OS assign a PID to each process?
* **Answer**: The OS assigns a PID to distinguish each executing process uniquely. This allows the kernel scheduler to allocate CPU time slices, enforce process isolation and security boundaries, manage inter-process communication (IPC), route signals (`kill`), track parent-child relationships, and monitor resource consumption.

### Q14: When does a process end?
* **Answer**: A process ends when one of three conditions occurs:
  1. **Normal Termination**: The program calls `exit()`, `_exit()`, or returns from `main()`.
  2. **Signal Interruption**: An external signal terminates the process (e.g., `Ctrl+C` sending `SIGINT` or `kill -9` sending `SIGKILL`).
  3. **Fatal Hardware Fault / Crash**: The process triggers an illegal operation causing a CPU exception (e.g., dereferencing an invalid memory address causing a `SIGSEGV` segmentation fault).

### Q15: Who assigns the PID?
* **Answer**: The **Operating System Kernel** (specifically, the kernel's process management and scheduling subsystem) assigns the PID during process creation.
