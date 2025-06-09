# Agent Server Setup

This project has been refactored to run the agent servers independently from the main FastAPI application.

## Quick Start

1. **Start all agent servers:**
   ```bash
   ./start_agents.sh
   ```

2. **Start the main FastAPI server:**
   ```bash
   python main.py
   # or 
   uvicorn main:app --reload
   ```

3. **Stop all agent servers:**
   ```bash
   ./stop_agents.sh
   ```

## Architecture

- **Main FastAPI app** (`main.py`): Provides the `/query` endpoint and acts as a client to the manager agent
- **Manager Agent** (port 8002): Routes queries to specialist agents
- **Greeting Agent** (port 8001): Handles text queries and research tasks
- **Image Agent** (port 8003): Handles image generation requests

## Individual Agent Scripts

You can also run agents individually:

```bash
python run_greeting_agent.py    # Port 8001
python run_image_agent.py       # Port 8003  
python run_manager_agent.py     # Port 8002
```

## Important Notes

- Make sure to start the agent servers BEFORE starting the main FastAPI application
- The main FastAPI app will attempt to connect to the manager agent on `http://127.0.0.1:8002`
- If agent servers are not running, queries will fail with a connection error
- Use the health check endpoint `/health` to verify the FastAPI server is running

## Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /query` - Send queries to the agent network 