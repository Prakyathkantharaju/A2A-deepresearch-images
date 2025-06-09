import asyncio
import os

from python_a2a import A2AClient, Message, TextContent, MessageRole
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from loguru import logger
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()


class Query(BaseModel):
    text: str


app = FastAPI()

# Client to communicate with the manager agent
manager_client = None


@app.on_event("startup")
async def startup_event():
    """
    Handles the startup process of the FastAPI application.
    - Checks for the GOOGLE_API_KEY.
    - Creates a client to communicate with the manager agent.
    """
    logger.info("Application startup...")

    # Check for API key before starting
    if not os.getenv("GOOGLE_API_KEY"):
        logger.error("FATAL: GOOGLE_API_KEY not found in .env file.")
        raise RuntimeError("GOOGLE_API_KEY not found in .env file.")

    # Create a client to communicate with the manager agent
    global manager_client
    manager_client = A2AClient(endpoint_url="http://127.0.0.1:8002")
    logger.info("Manager client created.")
    logger.info("Note: Make sure agent servers are running (use ./start_agents.sh)")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Handles the shutdown process of the FastAPI application.
    """
    logger.info("Application shutdown...")
    logger.info(
        "Note: Agent servers are running independently. Use ./stop_agents.sh to stop them."
    )


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
    initial_message = Message(
        content=TextContent(text=query.text), role=MessageRole.USER
    )

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


@app.get("/health")
def health_check():
    """Health check endpoint to verify the FastAPI server is running."""
    return {"status": "healthy", "message": "FastAPI server is running"}
