#!/usr/bin/env bash
# ==============================================================================
# test_exit_codes.sh - Rigorous automated verification of process exit statuses
# ==============================================================================

set -euo pipefail

make -s all

FAILED=0
TOTAL=0

assert_exit() {
    local cmd="$1"
    local expected="$2"
    local input="${3:-}"
    TOTAL=$((TOTAL + 1))

    set +e
    if [ -n "$input" ]; then
        printf "%s\n" "$input" | eval "$cmd" >/dev/null 2>&1
    else
        eval "$cmd" >/dev/null 2>&1
    fi
    local actual=$?
    set -e

    if [ "$actual" -eq "$expected" ]; then
        echo -e "[\033[0;32mPASS\033[0m] $cmd (Input: '$input') -> Expected: $expected, Got: $actual"
    else
        echo -e "[\033[0;31mFAIL\033[0m] $cmd (Input: '$input') -> Expected: $expected, Got: $actual"
        FAILED=$((FAILED + 1))
    fi
}

echo "Running Exit Code Unit Assertions:"
assert_exit "./bin/task3" 0 "100"
assert_exit "./bin/task3" 0 "1"
assert_exit "./bin/task3" 1 "-1"
assert_exit "./bin/task3" 1 "-42"
assert_exit "./bin/task3" 1 "0"
assert_exit "./bin/task5" 0 "1"
assert_exit "./bin/task5" 1 "0"

echo -e "\nSummary: $((TOTAL - FAILED))/$TOTAL tests passed."
if [ "$FAILED" -ne 0 ]; then
    exit 1
fi
