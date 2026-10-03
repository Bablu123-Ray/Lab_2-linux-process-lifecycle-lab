#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

/**
 * task2_procfs_reader.c - Querying Linux Kernel Virtual Filesystem (/proc)
 *
 * Demonstrates reading process metadata directly from /proc/self/status.
 * The Linux kernel exposes runtime process accounting tables via procfs.
 */
int main(void) {
    printf("--- Direct Linux Kernel ProcFS Inspection ---\n");
    printf("API Syscall Query: getpid() = %d, getppid() = %d\n\n", getpid(), getppid());

    FILE *fp = fopen("/proc/self/status", "r");
    if (!fp) {
        perror("Failed to open /proc/self/status");
        return 1;
    }

    char line[256];
    printf("Kernel /proc/self/status extracts:\n");
    while (fgets(line, sizeof(line), fp)) {
        if (strncmp(line, "Name:", 5) == 0 ||
            strncmp(line, "State:", 6) == 0 ||
            strncmp(line, "Tgid:", 5) == 0 ||
            strncmp(line, "Pid:", 4) == 0 ||
            strncmp(line, "PPid:", 5) == 0 ||
            strncmp(line, "VmSize:", 7) == 0 ||
            strncmp(line, "Threads:", 8) == 0) {
            printf("  %s", line);
        }
    }

    fclose(fp);
    return 0;
}
