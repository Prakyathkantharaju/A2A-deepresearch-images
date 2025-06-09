# run_and_test.py
import os
import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# We import the classes after loading the .env file
from greeting_agent import GreetingAgent
from image_agent import ImageAgent
from manager_agent import ManagerAgent
from a2a.client import A2AClient
from a2a.message import Message, TextPart

async def run_test_query(client, query):
    print("="*50)
    print(f"CLIENT: Sending query -> '{query}'")
    initial_message = Message(parts=[TextPart(text=query)])
    response = await client.send_message(initial_message)
    print(f"CLIENT: Final response received <- '{response.get_text()}'")
    print("="*50)

async def main():
    # Check for API key before starting
    if not os.getenv("GOOGLE_API_KEY"):
        print("FATAL: GOOGLE_API_KEY not found in .env file. Please create .env and add it.")
        return

    # --- Start all three agent servers ---
    print("--- Starting Agent Servers ---")
    greeting_agent = GreetingAgent()
    image_agent = ImageAgent()
    manager_agent = ManagerAgent()

    tasks = [
        asyncio.create_task(greeting_agent.run(host="127.0.0.1", port=8001)),
        asyncio.create_task(image_agent.run(host="127.0.0.1", port=8003)),
        asyncio.create_task(manager_agent.run(host="127.0.0.1", port=8002)),
    ]
    await asyncio.sleep(2) # Give servers time to start
    print("--- All agents are running in the background ---\n")

    # --- Test the system with different queries ---
    manager_client = A2AClient(endpoint="http://127.0.0.1:8002")

    # Test Case 1: A query that should be routed to the ImageAgent
    await run_test_query(manager_client, "Draw a picture of a friendly robot programming on a laptop")
    
    await asyncio.sleep(1)

    # Test Case 2: A query that should be routed to the GreetingAgent
    await run_test_query(manager_client, "Write a short, encouraging welcome message for a new developer joining our hackathon team.")

    # --- Cleanly shut down all server tasks ---
    print("\n--- All tests complete. Shutting down agents. ---")
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)

if __name__ == "__main__":
    asyncio.run(main())