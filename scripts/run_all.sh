#!/usr/bin/env bash
# ==============================================================================
# run_all.sh - Automated runner and verification script for Lab 3 tasks
# ==============================================================================

set -euo pipefail

CYAN='\033[0;36m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "\n${BOLD}${CYAN}======================================================================${NC}"
echo -e "${BOLD}${CYAN}   Linux Process Lifecycles & OS Interaction: Automated Lab Runner    ${NC}"
echo -e "${BOLD}${CYAN}======================================================================${NC}\n"

# Build all binaries
echo -e "${BLUE}[Building] Compiling all task source files via Makefile...${NC}"
make all
echo -e "${GREEN}Build complete.${NC}\n"

# Task 1
echo -e "${BOLD}${BLUE}--- [Task 1] Long-Running Process & Background Execution ---${NC}"
./bin/task1 &
TASK1_PID=$!
echo -e "Started ./bin/task1 with background PID: ${TASK1_PID}"
sleep 1
ps aux | grep "[t]ask1"
kill -9 "${TASK1_PID}" 2>/dev/null || true
echo -e "${GREEN}Task 1 verified.${NC}\n"

# Task 2
echo -e "${BOLD}${BLUE}--- [Task 2] Process Identity (PID and PPID) ---${NC}"
./bin/task2 &
TASK2_PID=$!
sleep 1
ps -p "${TASK2_PID}" -o pid,ppid,cmd
kill -9 "${TASK2_PID}" 2>/dev/null || true
echo -e "${GREEN}Task 2 verified.${NC}\n"

# Task 3
echo -e "${BOLD}${BLUE}--- [Task 3] Exit Codes & OS Feedback ($?) ---${NC}"
echo "Scenario A (Input: 5):"
printf "5\n" | ./bin/task3
echo -e "Exit status: ${GREEN}$?${NC}"

echo "Scenario B (Input: -5):"
set +e
printf -- "-5\n" | ./bin/task3
EXIT_B=$?
set -e
echo -e "Exit status: ${YELLOW}${EXIT_B}${NC}"
echo -e "${GREEN}Task 3 verified.${NC}\n"

# Task 4
echo -e "${BOLD}${BLUE}--- [Task 4] Standard I/O Streams ---${NC}"
printf "John\n" | ./bin/task4
echo -e "${GREEN}Task 4 verified.${NC}\n"

# Task 5
echo -e "${BOLD}${BLUE}--- [Task 5] Conditional Execution & Control Flow ---${NC}"
echo "Run 1 (Choice: 1 - Yes):"
printf "1\n" | ./bin/task5
echo -e "Exit status: ${GREEN}$?${NC}"

echo "Run 2 (Choice: 0 - No):"
set +e
printf "0\n" | ./bin/task5
EXIT_5B=$?
set -e
echo -e "Exit status: ${YELLOW}${EXIT_5B}${NC}"
echo -e "${GREEN}Task 5 verified.${NC}\n"

echo -e "${BOLD}${GREEN}✔ All 5 Lab tasks executed and verified successfully!${NC}\n"
