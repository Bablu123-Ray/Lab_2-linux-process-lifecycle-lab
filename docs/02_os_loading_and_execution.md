# Section 2: How the OS Loads and Executes a Program

Understanding how an operating system transitions a static file on disk into an active executing process in main memory is fundamental to systems programming.

---

## The 7-Step Program Loading Pipeline

```
  Shell (Parent)                               Child Process
        │                                             │
        │─── 1. User types './task1'                  │
        │─── 2. Calls fork() ────────────────────────►│ Cloned child process
        │    (Parent sleeps/waits via waitpid)        │
        │                                             │─── 3. Calls execve("./task1")
        │                                             │    (Replaces shell image with target binary)
        │                                             ▼
        │                                   ┌───────────────────────────┐
        │                                   │ 4. OS Kernel Takes Over   │
        │                                   │ - Validates ELF header    │
        │                                   │ - Maps virtual address    │
        │                                   │ - Allocates page tables   │
        │                                   │ - Maps .text, .data, .bss │
        │                                   │ - Pushes argc, argv, envp │
        │                                   │ - Jumps to _start         │
        │                                   └─────────────┬─────────────┘
        │                                                 │
        │                                                 ▼
        │                                   ┌───────────────────────────┐
        │                                   │ 5. Entry Point: _start    │
        │                                   │ - Invokes crt0 runtime    │
        │                                   │ - Calls __libc_start_main │
        │                                   │ - Invokes main()          │
        │                                   └─────────────┬─────────────┘
        │                                                 │
        │                                                 ▼
        │                                   ┌───────────────────────────┐
        │                                   │ 6. Process Runtime Loop   │
        │                                   │ - Executes instructions   │
        │                                   │ - Performs system calls   │
        │                                   └─────────────┬─────────────┘
        │                                                 │
        │                                                 ▼
        │                                   ┌───────────────────────────┐
        │                                   │ 7. Kernel Cleanup         │
        │                                   │ - Frees allocated RAM     │
        │                                   │ - Closes file descriptors │
        │◄── Exit code ($?) returned via waitpid ─────────┤ - Removes process table PID│
        ▼                                   └───────────────────────────┘
```

---

## Detailed Step Breakdown

### Step 1: User Command
The user types `./program_name` in an interactive shell (e.g., `bash`, `zsh`).

### Step 2: The `fork()` System Call
The shell invokes `fork()`. The Linux kernel duplicates the calling process, producing a child process with an identical address space, identical file descriptors, and a new unique Process ID (PID). The shell process retains its Parent Process ID (PPID) role.

### Step 3: The `execve()` System Call
Inside the child process, the shell invokes `execve("./program_name", argv, envp)`. The kernel obliterates the child process's existing text, data, heap, and stack segments, replacing them entirely with the new executable binary from disk.

### Step 4: OS Kernel Initialization Actions
1. **ELF Validation**: The kernel reads the initial 16-byte ELF identification block, checking the magic number (`0x7F 'E' 'L' 'F'`).
2. **Virtual Memory Allocation**: Configures page directory structures for the new process virtual memory layout.
3. **Segment Mapping**:
   - Maps `.text` segment as Read-Only / Executable (`R-X`).
   - Maps `.data` and `.bss` segments as Read / Write (`RW-`).
4. **Stack Environment Preparation**: Prepares the top of the stack by pushing the argument count (`argc`), argument vector array (`argv`), and environment variable pointers (`envp`).
5. **Instruction Pointer Transfer**: Points the instruction pointer (`%rip`) to the program's true entry symbol: `_start`.

---

## Entry Point Mechanics: `_start` vs. `main()`

A common misconception is that execution begins directly inside the programmer's `main()` function. In reality, the compiler and linker insert runtime glue code:

| Component | Responsibility | Systems Role |
|---|---|---|
| `_start` | The true low-level entry point provided by the C runtime (`crt1.o`). It extracts `argc`, `argv`, and `envp` from the stack, initializes thread-local storage, calls static constructors, and invokes `__libc_start_main()`. | Kernel-to-Userland Bridge |
| `main()` | The high-level programmer entry point where application logic is authored. | User Application Code |
| `Runtime` | The active window during which code instructions are executed on the CPU before a termination condition occurs. | Active Execution Phase |
