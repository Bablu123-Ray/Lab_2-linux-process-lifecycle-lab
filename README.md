# Lab 2: Linux Process Lifecycles & OS Interaction (Step-by-Step Guide)

[![Standard](https://img.shields.io/badge/Language-C11%20%7C%20POSIX-blue.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Linux%20Kernel-orange.svg)]()
[![Course](https://img.shields.io/badge/OS-ST5039CMD%20Programming%20%26%20OS-brightgreen.svg)]()
[![Documentation: PDF](https://img.shields.io/badge/Documentation-PDF%20Guide-red.svg)](Process_Lifecycles_Step_by_Step_Guide.pdf)
[![Documentation: HTML](https://img.shields.io/badge/Documentation-HTML%20Report-blue.svg)](Lab_2_Process_Lifecycles_Documentation.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive systems laboratory investigating **Process Lifecycles**, **OS Program Loading (`fork` & `execve`)**, and **Process Virtual Memory Segments**, mapping directly to **Lecture 2 (A Process Layout & OS Loading)** and **Lab 2 (Investigating Process Lifecycles)**.

---

## 📑 Lab Documentation Quick Links
* **Official PDF Step-by-Step Guide:** [Process_Lifecycles_Step_by_Step_Guide.pdf](Process_Lifecycles_Step_by_Step_Guide.pdf)
* **Comprehensive Web Report:** [Lab_2_Process_Lifecycles_Documentation.html](Lab_2_Process_Lifecycles_Documentation.html)
* **Technical Markdown Documentation:** [Lab_2_Process_Lifecycles_Documentation.md](Lab_2_Process_Lifecycles_Documentation.md)

---

## 📌 Executive Summary & Lab Summarization (LAB 2)

### 1. Lab Purpose & High-Level Summary
The primary objective of **Lab 2** is to explore the dynamic lifecycle of programs in execution. While a program binary is a passive file residing on disk (ELF format), a **process** is an active instance running in main memory (RAM). The operating system kernel manages this transition by provisioning dedicated virtual memory segments, assigning a unique **Process ID (PID)**, scheduling CPU execution, mediating standard input/output streams, and capturing the process's termination exit status code (`$?`).

### 2. Five Practical Lab Tasks Matrix

| Task # | Task Name | Core Concept | Primary Commands | Test Input / Action | Observed State / Return | OS Kernel Mechanism |
|---|---|---|---|---|---|---|
| **Task 1** | **Long-Running Process** | Background Execution | `gcc task1_alive.c -o task1`<br>`./task1 &`<br>`ps aux \| grep task1` | Appending `&` operator | Job `[1] 24810`; State `S` (Interruptible Sleep) | Kernel frees interactive shell immediately; `sleep(1)` yields CPU to prevent wasteful busy-waiting. |
| **Task 2** | **Process Identity & Hierarchy** | Process ID & Parent Shell | `gcc task2_identity.c -o task2`<br>`./task2 &`<br>`ps -p 25102 -o pid,ppid,cmd` | System calls `getpid()`, `getppid()` | `PID: 25102`<br>`PPID: 19440` | Kernel assigns unique PID from process table; PPID references parent bash terminal that spawned it. |
| **Task 3** | **Exit Status Codes & Feedback** | Return Codes & `$?` | `gcc task3_exit.c -o task3`<br>`./task3`<br>`echo $?` | Input `5` (positive)<br>Input `-5` (negative) | `echo $? -> 0` (Success)<br>`echo $? -> 1` (Failure) | Process returns 8-bit integer to OS via `return`/`exit()`; shell records it in `$?` for control flow. |
| **Task 4** | **Standard I/O Streams** | File Descriptors (0 & 1) | `gcc task4_input.c -o task4`<br>`./task4` | Keyboard input (`Bablu`) | stdout string: "Hello, Bablu! Welcome to OS Class." | Kernel automatically attaches `stdin` (fd 0) to keyboard and `stdout` (fd 1) to terminal display. |
| **Task 5** | **Conditional Flow & Lifecycle** | Dynamic Branching & Destruction | `gcc task5_control.c -o task5`<br>`./task5`<br>`echo $?` | Input `1` (Continue)<br>Input `0` (Abort) | Choice 1: sleeps 5s, exit 0<br>Choice 0: aborts, exit 1 | Demonstrates process creation, dynamic execution path, and PCB reclamation upon process exit (`26780` vs `26795`). |

### 3. Process Memory Segments Summary

| Memory Segment | Growth Direction | Access Permissions | Stored Data & Contents | Allocation & Cleanup |
|---|---|---|---|---|
| **Stack Segment** | Downwards (High -> Low Memory) | Read / Write (`RW-`) | Function call frames, local variables, function arguments, return pointers. | Managed automatically by CPU via `%rsp` (LIFO; deallocated upon function return). |
| **Heap Segment** | Upwards (Low -> High Memory) | Read / Write (`RW-`) | Dynamic runtime memory allocated via `malloc()`, `calloc()`, and `realloc()`. | Managed manually by the programmer; persisted until freed via `free()`. |
| **BSS Segment (`.bss`)** | Fixed Size | Read / Write (`RW-`) | Uninitialized global and static variables. | Zero-initialized by kernel loader at startup without taking space in disk binary. |
| **Data Segment (`.data`)** | Fixed Size | Read / Write (`RW-`) | Initialized global and static variables with pre-assigned values. | Loaded directly from the ELF binary file image into RAM. |
| **Code / Text (`.text`)** | Fixed Size | Read / Execute (`R-X`) | Compiled CPU machine instructions (binary opcodes). | Read-only to prevent self-modifying code vulnerabilities; shared among identical processes. |

### 4. OS Loading & Lifecycle Sequence Summary
1. **User Invocation**: Terminal user types `./program`.
2. **`fork()` Call**: Shell forks a duplicate child process.
3. **`execve()` Call**: Child replaces its memory address space with the target binary.
4. **Kernel ELF Validation**: Verifies magic bytes (`0x7F 'E' 'L' 'F'`) and architecture.
5. **Page Allocation**: Memory segments (`.text`, `.data`, `.bss`, heap, stack) are mapped.
6. **Execution**: Control transfers to `_start -> __libc_start_main -> main()`.
7. **Termination & Cleanup**: Kernel frees memory pages, closes open file descriptors, and publishes the exit status code to `$?`.

---

## 🏗️ Architecture Overview: A Process in Memory

```
                      [ Source Code: .c ]
                               │
                               │  gcc Compilation
                               ▼
                      [ Executable Binary: ELF ]
                               │
                               │  ./run (Shell fork + execve)
                               ▼
                    ┌───────────────────────────┐
                    │    PROCESS (PID in RAM)   │
                    │                           │
                    │ ◄── Keyboard (scanf)      │
                    │ ◄── OS Kernel (getpid)    │
                    │ ──► Screen (printf)       │
                    │ ──► Shell Exit Code ($?)  │
                    └───────────────────────────┘
```

### Memory Process Layout
When a process is created, the OS organizes memory into different sections:

![Memory Process Layout](assets/screenshots/raw/06_memory_layout.png)

---

## 🔬 Practical Lab Tasks Walkthrough

### Task 1: The Long-Running Process

* **Objective**: In enterprise servers, processes run for days or months. We must know how to run a process in the background using `&` and monitor it while it is active using `ps aux`.
* **Command**: `cat task1_alive.c then gcc task1_alive.c -o task1 then ./task1 & then ps aux | grep task1`
* **Terminal Screenshot**:

![Task 1 - Long-Running Process](assets/screenshots/raw/01_task1_alive.png)

* **Observation**: The `&` operator executes `./task1` in the background, freeing the terminal shell immediately with job ID `[1]` and PID `24810`. The `ps aux` command confirms the process is active in state `S` (**Interruptible Sleep**), paused during its `sleep(1)` loop without consuming unnecessary CPU cycles.

---

### Task 2: Process Identity (PID and PPID)

* **Objective**: Every process in Linux has a unique Process ID (`PID`). The process that created it is the Parent Process ID (`PPID`), usually your terminal shell. Query these using `getpid()` and `getppid()`, and verify them via `ps -p <PID> -o pid,ppid,cmd`.
* **Command**: `cat task2_identity.c then gcc task2_identity.c -o task2 then ./task2 & then ps -p 25102 -o pid,ppid,cmd`
* **Terminal Screenshot**:

![Task 2 - Process Identity](assets/screenshots/raw/02_task2_identity.png)

* **Observation**: The program queries the Linux kernel and prints its unique `PID (25102)` and parent `PPID (19440)`. The OS `ps` command validates that the PPID `19440` belongs directly to the interactive terminal shell that spawned the process.

---

### Task 3: Exit Codes and OS Feedback ($?)

* **Objective**: When a program finishes, it returns an integer to the OS. `0` means "Success", and any non-zero number (like `1`) means "Error/Failure". The shell stores this in `$?`.
* **Command**: `cat task3_exit.c then gcc task3_exit.c -o task3 then ./task3 then echo $?`
* **Terminal Screenshot**:

![Task 3 - Exit Codes and OS Feedback](assets/screenshots/raw/03_task3_exit.png)

* **Observation**: When given a positive input (`5`), the program returns `0`, and `echo $?` outputs `0` (**Success**). When given a negative input (`-5`), the program returns `1`, and `echo $?` outputs `1` (**Failure**), proving that Unix processes communicate execution status directly to the calling shell.

---

### Task 4: Standard I/O Streams

* **Objective**: The OS provides standard input (`stdin`, fd 0) and standard output (`stdout`, fd 1) streams. `scanf()` reads from `stdin`, and `printf()` writes to `stdout`.
* **Command**: `cat task4_input.c then gcc task4_input.c -o task4 then ./task4`
* **Terminal Screenshot**:

![Task 4 - Standard I/O Streams](assets/screenshots/raw/04_task4_input.png)

* **Observation**: The operating system connects the keyboard stream to `stdin`, which is read by `scanf()` ("Bablu"), and redirects formatted text from `printf()` to `stdout` on the terminal screen ("Hello, Bablu! Welcome to OS Class.").

---

### Task 5: Conditional Execution and Termination

* **Objective**: Programs often branch based on user input. The OS tracks the final exit code to determine if the script or automation pipeline should continue or halt.
* **Command**: `cat task5_control.c then gcc task5_control.c -o task5 then ./task5 then echo $?`
* **Terminal Screenshot**:

![Task 5 - Conditional Execution and Termination](assets/screenshots/raw/05_task5_control.png)

* **Observation**: Choosing `1` causes the process to continue, simulate workload (`sleep(5)`), and return exit code `0` (`Success`). Choosing `0` causes the process to immediately abort and return exit code `1` (`Failure`). Each independent run receives a newly allocated PID from the kernel (`26780` vs `26795`), illustrating process creation and destruction.

---

## 🛠️ Build and Execution Commands

```bash
# Compile all binaries into bin/
make all

# Build debug binaries with symbols for GDB
make debug

# Run interactive terminal menu
chmod +x scripts/menu.sh
./scripts/menu.sh

# Run automated tests and assertions
chmod +x scripts/test_exit_codes.sh
./scripts/test_exit_codes.sh

# Clean build artifacts
make clean
```

---

## 📚 Technical Documentation Directory
- [Process Lifecycles Technical Documentation (Markdown)](Lab_2_Process_Lifecycles_Documentation.md)
- [Process Lifecycles Technical Documentation (HTML)](Lab_2_Process_Lifecycles_Documentation.html)
- [Official Step-by-Step PDF Guide](Process_Lifecycles_Step_by_Step_Guide.pdf)
- [Theory 1: Process Concept & Memory Segments](docs/01_theory_process_layout.md)
- [Theory 2: OS Program Loading (`fork` + `execve`)](docs/02_os_loading_and_execution.md)
- [Theory 3: Process Lifecycle, Termination, and Cleanup](docs/03_process_lifecycle_and_termination.md)
- [Theory 4: Linux `/proc` Virtual Filesystem Internals](docs/05_procfs_internals.md)
- [Theory 5: POSIX Signals & Asynchronous Interrupts Guide](docs/06_posix_signals_guide.md)
- [Lecture 2 Knowledge Assessment: All 15 Q&As](docs/04_knowledge_test_qa.md)

---

## 📄 License
Released under the [MIT License](LICENSE).
