#include <stdio.h>

/**
 * task3_exit.c - Exit codes and OS Feedback ($?)
 *
 * OS Concept:
 * When a process terminates, it delivers an integer exit status (0-255)
 * back to the parent process via waitpid(). By Unix convention:
 *   0 = Success
 *  >0 = Error / Failure condition
 * The shell stores this value in the special parameter '$?'.
 */
int main(void) {
    int num;

    printf("Enter a number (positive for success, negative for fail): ");
    if (scanf("%d", &num) != 1) {
        printf("Invalid input format.\n");
        return 1;
    }

    if (num > 0) {
        printf("Success\n");
        return 0; // Inform OS: execution succeeded
    } else {
        printf("Failure\n");
        return 1; // Inform OS: error / failure condition
    }
}
