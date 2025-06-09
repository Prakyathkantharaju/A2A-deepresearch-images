#!/bin/bash

# start_agents.sh - Script to start all three agent servers

set -e  # Exit on any error

echo "Starting agent servers..."

# Function to check if a port is available
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "Port $1 is already in use"
        return 1
    fi
    return 0
}

# Function to start an agent server
start_agent() {
    local agent_name=$1
    local port=$2
    local script_file=$3
    
    echo "Starting $agent_name on port $port..."
    
    if ! check_port $port; then
        echo "Warning: Port $port is already in use for $agent_name"
        return 1
    fi
    
    # Start the agent server in the background
    python $script_file &
    
    # Store the PID
    local pid=$!
    echo "$agent_name started with PID $pid on port $port"
    echo $pid >> /tmp/agent_pids.txt
}

# Clean up any existing PID file
rm -f /tmp/agent_pids.txt

# Start all three agents
start_agent "GreetingAgent" 8001 "run_greeting_agent.py"
start_agent "ImageAgent" 8003 "run_image_agent.py" 
start_agent "ManagerAgent" 8002 "run_manager_agent.py"

# Wait a moment for servers to start up
sleep 3

echo "All agent servers have been started!"
echo "PIDs stored in /tmp/agent_pids.txt"
echo ""
echo "Agent endpoints:"
echo "  - Greeting Agent: http://127.0.0.1:8001"
echo "  - Image Agent: http://127.0.0.1:8003"
echo "  - Manager Agent: http://127.0.0.1:8002"
echo ""
echo "To stop all agents, run: ./stop_agents.sh" 