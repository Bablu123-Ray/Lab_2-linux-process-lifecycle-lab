# Section 1: Process Concept & Virtual Memory Layout

## 1. Program vs. Process

A computer program begins as human-readable source code written in a high-level language such as C. Before it can execute, a compiler (e.g., `gcc`) translates the source code into a machine-readable executable file containing binary machine instructions (0s and 1s).

A fundamental distinction exists in modern operating systems between a **file** and a **process**:

| Concept | Description | Lifecycle & Location |
|---|---|---|
| **Program / Executable File** | Static entity stored persistently on non-volatile disk storage (e.g., SSD, HDD). It consists of binary instructions, initialization data, and metadata headers (ELF format on Linux). | Inactive on disk until executed. Never changes while stored. |
| **Process** | Dynamic entity: a program in active execution. When launched, the OS loads the binary into volatile main memory (RAM), allocates private system resources, sets up virtual memory, and assigns a unique identifier (PID). | Dynamic in RAM; actively scheduled and managed by the OS kernel. |
| **OS Role** | The kernel is solely responsible for creating, scheduling, managing, isolating, and terminating processes. | Ongoing background execution. |

---

## 2. A Process Layout: System Interaction Flow

When an executable binary is launched, it transitions into an active process residing in RAM, interacting with hardware and kernel subsystems:

```
    [ Source Code: .c ]
            │
            │  1. gcc (Compilation)
            ▼
    [ Executable Binary: .out / ELF ]
            │
            │  2. ./run (Shell fork + execve)
            ▼
 ┌────────────────────────────────────────────────────────┐
 │                   PROCESS (PID in RAM)                 │
 │                                                        │
 │   ◄─── 4. Keyboard (stdin: scanf)                      │
 │   ◄─── OS Kernel (System Information: getpid)          │
 │   ───► 3. Screen Output (stdout: printf)               │
 │   ───► 5. Exit Code to Shell (return status code: $?)  │
 └────────────────────────────────────────────────────────┘
```

---

## 3. Process Virtual Memory Architecture

When a process is instantiated, the Linux kernel allocates a dedicated virtual address space isolated from all other processes via hardware paging (MMU). This memory space is structured into well-defined segments:

![Process Memory Layout](../assets/screenshots/06_process_memory_layout.png)

### Segment Breakdown

1. **Stack Segment (Grows Downwards towards Lower Addresses)**
   - Stores function call stack frames.
   - Contains automatic local variables, function parameters, saved frame pointers (`%rbp`), and return instruction pointers (`%rip`).
   - Managed automatically by the CPU via stack push and pop instructions.

2. **Heap Segment (Grows Upwards towards Higher Addresses)**
   - Manages dynamic memory allocated at runtime via system calls (`brk`, `sbrk`) or allocator APIs (`malloc`, `calloc`, `realloc`, `free`).
   - Persists until explicitly freed by the programmer or reclaimed by the OS upon process exit.

3. **BSS Segment (`.bss` - Block Started by Symbol)**
   - Contains uninitialized global and static variables.
   - Does not consume actual storage space inside the disk binary; initialized to zero by the kernel upon memory mapping.

4. **Data Segment (`.data`)**
   - Contains global and static variables explicitly initialized with non-zero values by the programmer (e.g., `int count = 100;`).
   - Loaded directly from the executable file image into memory.

5. **Code / Text Segment (`.text`)**
   - Holds the compiled binary machine instructions executed by the CPU.
   - Marked as **Read-Only and Executable (`R-X`)** to prevent accidental or malicious self-modification and allow shared code instances across multiple processes.
