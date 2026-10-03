#!/usr/bin/env bash
# ==============================================================================
# menu.sh - Interactive CLI Menu for Lab 3 Process Tasks
# ==============================================================================

set -euo pipefail

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

make -s all

while true; do
    echo -e "\n${BOLD}${CYAN}==========================================${NC}"
    echo -e "${BOLD}${CYAN}   Linux Process Lifecycle Lab Tasks      ${NC}"
    echo -e "${BOLD}${CYAN}==========================================${NC}"
    echo "1. Run Task 1: Long-Running Process (Background)"
    echo "2. Run Task 2: Process Identity (PID and PPID)"
    echo "3. Run Task 3: Exit Codes and Feedback"
    echo "4. Run Task 4: Standard I/O Streams"
    echo "5. Run Task 5: Conditional Control Flow"
    echo "6. Run All Tasks Automatically"
    echo "7. Exit"
    echo -n "Select an option [1-7]: "
    read -r choice

    case "$choice" in
        1)
            echo -e "\n${YELLOW}Running Task 1 in background...${NC}"
            ./bin/task1 &
            T1_PID=$!
            echo "Background PID: $T1_PID"
            sleep 1
            ps -p "$T1_PID" -o pid,stat,cmd
            kill -9 "$T1_PID" 2>/dev/null || true
            ;;
        2)
            echo -e "\n${YELLOW}Running Task 2...${NC}"
            ./bin/task2 &
            T2_PID=$!
            sleep 1
            ps -p "$T2_PID" -o pid,ppid,cmd
            kill -9 "$T2_PID" 2>/dev/null || true
            ;;
        3)
            echo -e "\n${YELLOW}Running Task 3...${NC}"
            ./bin/task3
            echo "Exit status: $?"
            ;;
        4)
            echo -e "\n${YELLOW}Running Task 4...${NC}"
            ./bin/task4
            ;;
        5)
            echo -e "\n${YELLOW}Running Task 5...${NC}"
            ./bin/task5
            echo "Exit status: $?"
            ;;
        6)
            bash scripts/run_all.sh
            ;;
        7)
            echo -e "${GREEN}Exiting.${NC}"
            exit 0
            ;;
        *)
            echo "Invalid selection. Please choose 1-7."
            ;;
    esac
done
