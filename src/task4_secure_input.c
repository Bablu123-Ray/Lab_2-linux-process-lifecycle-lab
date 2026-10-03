#include <stdio.h>
#include <string.h>

/**
 * task4_secure_input.c - Safe Standard Input Handling
 *
 * Demonstrates mitigating buffer overflow vulnerabilities inherent to
 * unconstrained scanf("%s") by utilizing fgets() with explicit buffer bounds.
 */
int main(void) {
    char name[32];

    printf("Enter your name (safe input via fgets): ");
    if (fgets(name, sizeof(name), stdin) == NULL) {
        fprintf(stderr, "Error reading from stdin.\n");
        return 1;
    }

    // Strip trailing newline if present
    size_t len = strlen(name);
    if (len > 0 && name[len - 1] == '\n') {
        name[len - 1] = '\0';
    }

    printf("Securely read: '%s' (Length: %zu bytes)\n", name, strlen(name));
    return 0;
}
