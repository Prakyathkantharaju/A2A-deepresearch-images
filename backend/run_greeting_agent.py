#!/usr/bin/env python3
"""
Standalone script to run the Greeting Agent server.
"""

import asyncio
from python_a2a import run_server
from greeting_agent import GreetingAgent
from loguru import logger


async def main():
    """Start the Greeting Agent server."""
    logger.info("Starting Greeting Agent server on port 8001...")
    agent = GreetingAgent()
    await run_server(agent, host="127.0.0.1", port=8001)


if __name__ == "__main__":
    asyncio.run(main())
