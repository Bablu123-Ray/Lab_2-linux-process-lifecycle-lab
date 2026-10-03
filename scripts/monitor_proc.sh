#!/usr/bin/env bash
# ==============================================================================
# monitor_proc.sh - Inspect process resources (memory, status, file descriptors)
# ==============================================================================

set -euo pipefail

PID="${1:-}"

if [ -z "$PID" ]; then
    echo "Usage: $0 <PID>"
    echo "Example: $0 12345"
    exit 1
fi

if [ ! -d "/proc/$PID" ]; then
    echo "Error: Process $PID does not exist or has already terminated."
    exit 1
fi

echo "=========================================================="
echo "          Process Resource Snapshot for PID: $PID        "
echo "=========================================================="

echo -e "\n1. Basic Process Identity & State:"
grep -E "^(Name|State|Tgid|Pid|PPID|Uid|Gid)" "/proc/$PID/status"

echo -e "\n2. Virtual Memory Footprint:"
grep -E "^(VmPeak|VmSize|VmLck|VmHWM|VmRSS|VmData|VmStk|VmExe|VmLib)" "/proc/$PID/status"

echo -e "\n3. Open File Descriptors:"
ls -la "/proc/$PID/fd" 2>/dev/null || echo "Permission denied or no open descriptors."

echo -e "\n4. Command Line Invocation:"
tr '\0' ' ' < "/proc/$PID/cmdline"
echo -e "\n"
