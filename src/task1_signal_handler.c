#include <stdio.h>
#include <unistd.h>
#include <signal.h>
#include <stdbool.h>

static volatile bool keep_running = true;

/**
 * sigint_handler - Catches Ctrl+C (SIGINT)
 * @signum: The signal number intercepted
 *
 * Demonstrates how an active process intercepts OS signals
 * to perform graceful shutdown rather than abrupt termination.
 */
void sigint_handler(int signum) {
    if (signum == SIGINT) {
        printf("\n[Signal Caught] Received SIGINT (Ctrl+C). Cleaning up resources...\n");
        keep_running = false;
    }
}

int main(void) {
    // Register signal handler for SIGINT
    signal(SIGINT, sigint_handler);

    printf("Process PID [%d] started with SIGINT trap.\n", getpid());
    printf("Press Ctrl+C to test graceful signal handling, or wait 15 seconds.\n");

    int seconds = 0;
    while (keep_running && seconds < 15) {
        sleep(1);
        seconds++;
        printf("Running... [%d/15s]\n", seconds);
    }

    printf("Exiting gracefully. Return code 0.\n");
    return 0;
}
