#!/bin/bash

# Kill all transmission-cli processes
killall transmission-cli

# Check if any transmission-cli processes are still running
if pgrep -x "transmission-cli" >/dev/null; then
    echo "Failed to kill all transmission-cli processes"
else
    echo "All transmission-cli processes killed successfully"
fi

