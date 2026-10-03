#include <stdio.h>
#include <unistd.h>

/**
 * task1_alive.c - Demonstrates a long-running background process
 *
 * OS Concept:
 * Server and daemon processes often run continuously. By running this program
 * in the background using '&', we can inspect its process state in real time
 * from a separate terminal using 'ps aux'.
 */
int main(void) {
    printf("I am starting...\n");

    // Loop for 30 seconds, sleeping 1 second per iteration
    for (int i = 1; i <= 30; i++) {
        sleep(1); // Suspends execution for 1 second via nanosleep syscall
    }

    printf("I am finished.\n");
    return 0;
}
