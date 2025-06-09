#!/usr/bin/env python3
"""
Standalone script to run the Image Agent server.
"""

import asyncio
from python_a2a import run_server
from image_agent import ImageAgent
from loguru import logger


async def main():
    """Start the Image Agent server."""
    logger.info("Starting Image Agent server on port 8003...")
    agent = ImageAgent()
    await run_server(agent, host="127.0.0.1", port=8003)


if __name__ == "__main__":
    asyncio.run(main())
