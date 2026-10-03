#include <stdio.h>
#include <unistd.h>

/**
 * task5_control.c - Conditional Execution and Process Termination
 *
 * OS Concept:
 * Real-world automation pipelines, system services, and build systems
 * inspect the exit code of commands. Based on user choices or runtime
 * conditions, a process branches and communicates either success (0)
 * or abort/error (1) back to the calling shell.
 */
int main(void) {
    int choice;

    // Print active PID at initiation
    printf("Current PID: %d\n", getpid());

    printf("Do you want to continue? (1 for Yes, 0 for No): ");
    if (scanf("%d", &choice) != 1) {
        printf("Invalid input.\n");
        return 1;
    }

    if (choice == 1) {
        printf("Continuing...\n");
        sleep(5); // Simulate background work
        return 0; // Success
    } else {
        printf("Exiting...\n");
        return 1; // Abort / Failure
    }
}
