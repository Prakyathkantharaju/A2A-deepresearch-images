import asyncio
import os

from python_a2a import A2AClient, Message, TextContent, MessageRole, run_server
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from loguru import logger
from pydantic import BaseModel

from greeting_agent import GreetingAgent
from image_agent import ImageAgent
from manager_agent import ManagerAgent

# Load environment variables from .env file
load_dotenv()


class Query(BaseModel):
    text: str


app = FastAPI()

# In-memory storage for agent tasks and clients
agent_tasks = []
manager_client = None


@app.on_event("startup")
async def startup_event():
    """
    Handles the startup process of the FastAPI application.
    - Checks for the GOOGLE_API_KEY.
    - Initializes and runs the agent servers.
    - Creates a client to communicate with the manager agent.
    """
    logger.info("Application startup...")

    # Check for API key before starting
    if not os.getenv("GOOGLE_API_KEY"):
        logger.error("FATAL: GOOGLE_API_KEY not found in .env file.")
        raise RuntimeError("GOOGLE_API_KEY not found in .env file.")

    # Start all three agent servers
    logger.info("Starting agent servers...")
    greeting_agent = GreetingAgent()
    image_agent = ImageAgent()
    manager_agent = ManagerAgent()

    # Create server tasks using run_server function
    tasks = [
        asyncio.create_task(run_server(greeting_agent, host="127.0.0.1", port=8001)),
        asyncio.create_task(run_server(image_agent, host="127.0.0.1", port=8003)),
        asyncio.create_task(run_server(manager_agent, host="127.0.0.1", port=8002)),
    ]
    agent_tasks.extend(tasks)
    await asyncio.sleep(2)  # Give servers time to start
    logger.info("All agents are running in the background.")

    # Create a client to communicate with the manager agent
    global manager_client
    manager_client = A2AClient(endpoint_url="http://127.0.0.1:8002")
    logger.info("Manager client created.")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Handles the shutdown process of the FastAPI application.
    - Cancels all running agent tasks.
    """
    logger.info("Application shutdown...")
    for task in agent_tasks:
        task.cancel()
    await asyncio.gather(*agent_tasks, return_exceptions=True)
    logger.info("All agents have been shut down.")


@app.post("/query")
async def query(query: Query):
    """
    Forwards a query to the manager agent and returns the final response.

    Args:
        query: The user's query.

    Returns:
        The final response from the agent network.
    """
    if not manager_client:
        logger.error("Manager client is not available.")
        raise HTTPException(status_code=503, detail="Manager agent is not available.")

    logger.info(f"Sending query to manager agent: '{query.text}'")
    initial_message = Message(content=TextContent(text=query.text), role=MessageRole.USER)

    try:
        response = await manager_client.send_message(initial_message)
        final_response = response.content.text
        logger.info(f"Final response received: '{final_response}'")
        return {"response": final_response}
    except Exception as e:
        logger.error(f"An error occurred while processing the query: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def read_root():
    return {"message": "Gemini Hackathon Agent Server is running."}
