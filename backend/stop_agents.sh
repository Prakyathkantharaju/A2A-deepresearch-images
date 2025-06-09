#!/bin/bash

# stop_agents.sh - Script to stop all running agent servers

echo "Stopping agent servers..."

# Check if PID file exists
if [ ! -f /tmp/agent_pids.txt ]; then
    echo "No PID file found. Attempting to kill processes by port..."
    
    # Try to kill processes by port
    for port in 8001 8002 8003; do
        pid=$(lsof -ti:$port)
        if [ ! -z "$pid" ]; then
            echo "Killing process on port $port (PID: $pid)"
            kill -TERM $pid 2>/dev/null || true
        fi
    done
else
    # Kill processes by stored PIDs
    echo "Using stored PIDs to stop agents..."
    while read -r pid; do
        if [ ! -z "$pid" ]; then
            echo "Stopping process with PID: $pid"
            kill -TERM $pid 2>/dev/null || true
        fi
    done < /tmp/agent_pids.txt
    
    # Clean up PID file
    rm -f /tmp/agent_pids.txt
fi

# Wait a moment for graceful shutdown
sleep 2

# Force kill if still running
echo "Checking for remaining processes..."
for port in 8001 8002 8003; do
    pid=$(lsof -ti:$port 2>/dev/null)
    if [ ! -z "$pid" ]; then
        echo "Force killing process on port $port (PID: $pid)"
        kill -KILL $pid 2>/dev/null || true
    fi
done

echo "All agent servers have been stopped." 