#include <stdio.h>
#include <unistd.h>

/**
 * task2_identity.c - Querying Process Identity (PID and PPID)
 *
 * OS Concept:
 * Every active process in Linux has a unique integer identifier called a
 * Process ID (PID). The process that spawned it is its parent, identified
 * by the Parent Process ID (PPID) - typically the interactive shell (bash/zsh).
 */
int main(void) {
    // Query current process ID using getpid() syscall
    pid_t my_pid = getpid();

    // Query parent process ID using getppid() syscall
    pid_t my_ppid = getppid();

    printf("My PID is: %d\n", my_pid);
    printf("My Parent PID is: %d\n", my_ppid);

    printf("Sleeping for 20 seconds...\n");
    sleep(20);

    return 0;
}
