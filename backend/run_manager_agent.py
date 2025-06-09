#!/usr/bin/env python3
"""
Standalone script to run the Manager Agent server.
"""

import asyncio
from python_a2a import run_server
from manager_agent import ManagerAgent
from loguru import logger


async def main():
    """Start the Manager Agent server."""
    logger.info("Starting Manager Agent server on port 8002...")
    agent = ManagerAgent()
    await run_server(agent, host="127.0.0.1", port=8002)


if __name__ == "__main__":
    asyncio.run(main())
