# Section 5: The Linux `/proc` Virtual Filesystem

The Linux kernel exposes internal process state and system metadata via a pseudo-filesystem mounted at `/proc`. It does not occupy space on physical disk; files are generated on-the-fly by the kernel upon access.

---

## 1. Structure of `/proc/[PID]/`

Every active process with identifier `PID` has a corresponding directory `/proc/[PID]/`:

| Path | Purpose & Content |
|---|---|
| `/proc/[PID]/cmdline` | The complete command-line invocation arguments separated by null bytes (`\0`). |
| `/proc/[PID]/status` | Human-readable breakdown of process state, memory metrics, user/group IDs, and signals. |
| `/proc/[PID]/stat` | Machine-readable single-line telemetry used by utilities like `ps` and `top`. |
| `/proc/[PID]/statm` | Memory utilization in units of hardware pages. |
| `/proc/[PID]/fd/` | Directory containing symbolic links to all open file descriptors (`0` for stdin, `1` for stdout, etc.). |
| `/proc/[PID]/maps` | Memory segment layout showing mapped virtual address regions (Text, Heap, Stack, libc). |
| `/proc/[PID]/exe` | Symbolic link pointing to the executable binary file on disk. |

---

## 2. Inspecting Memory Metrics via `/proc/[PID]/status`

```bash
cat /proc/self/status | grep -E "VmSize|VmRSS|VmData|VmStk"
```

* **`VmSize`**: Total virtual memory size allocated to the process address space.
* **`VmRSS`**: Resident Set Size — the actual physical RAM currently occupied by the process.
* **`VmData`**: Virtual memory dedicated to the data segment (`.data` and `.bss`).
* **`VmStk`**: Virtual memory dedicated to the stack segment.
