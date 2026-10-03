CC ?= gcc
CFLAGS ?= -Wall -Wextra -Wpedantic -O2
DEBUG_FLAGS ?= -g -DDEBUG -O0
SRC_DIR = src
BIN_DIR = bin

TARGETS = $(BIN_DIR)/task1 $(BIN_DIR)/task2 $(BIN_DIR)/task3 $(BIN_DIR)/task4 $(BIN_DIR)/task5

all: $(BIN_DIR) $(TARGETS)

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

# Standard release builds
$(BIN_DIR)/task1: $(SRC_DIR)/task1_alive.c
	$(CC) $(CFLAGS) $< -o $@

$(BIN_DIR)/task2: $(SRC_DIR)/task2_identity.c
	$(CC) $(CFLAGS) $< -o $@

$(BIN_DIR)/task3: $(SRC_DIR)/task3_exit.c
	$(CC) $(CFLAGS) $< -o $@

$(BIN_DIR)/task4: $(SRC_DIR)/task4_input.c
	$(CC) $(CFLAGS) $< -o $@

$(BIN_DIR)/task5: $(SRC_DIR)/task5_control.c
	$(CC) $(CFLAGS) $< -o $@

# Debug build target with symbols for GDB analysis
debug: CFLAGS = $(DEBUG_FLAGS)
debug: clean all

# Code quality syntax check without linking
check-syntax:
	$(CC) $(CFLAGS) -fsyntax-only $(SRC_DIR)/*.c

clean:
	rm -rf $(BIN_DIR)

.PHONY: all debug check-syntax clean
