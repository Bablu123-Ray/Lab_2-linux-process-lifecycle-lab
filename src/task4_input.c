#include <stdio.h>

/**
 * task4_input.c - Standard Input and Output Streams (stdin & stdout)
 *
 * OS Concept:
 * When a process is initialized by execve(), the kernel sets up standard
 * file descriptors for the process:
 *   File Descriptor 0: stdin  (Standard Input, default: keyboard)
 *   File Descriptor 1: stdout (Standard Output, default: terminal screen)
 *   File Descriptor 2: stderr (Standard Error, default: terminal screen)
 *
 * scanf() reads from stdin, and printf() writes formatted buffers to stdout.
 */
int main(void) {
    char name[50];

    printf("Enter your name: ");
    // Read string from standard input stream (stdin)
    if (scanf("%49s", name) != 1) {
        printf("Failed to read name.\n");
        return 1;
    }

    printf("Hello, %s! Welcome to OS Class.\n", name);
    return 0;
}
