import asyncio
import logging
import sys

import aiohttp
import pytest

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def some_long_running_query():
    async with aiohttp.ClientSession() as session:
        async with session.get("http://httpbin.org/get") as resp:
            logger.info("Starting processing some long request...")
            await asyncio.sleep(1)
            logger.info(
                f"Response status {resp.status}, response text {await resp.text()}"
            )
            logger.info("Processing some long request finished!")


async def some_local_jobs():
    while True:
        logger.info(f"Doing some local job right now!")
        await asyncio.sleep(0.5)


@pytest.mark.asyncio
async def test_run():
    some_long_query_task = asyncio.Task(some_long_running_query())
    some_local_job = asyncio.Task(some_local_jobs())
    logger.info(await some_long_query_task)
    some_local_job.cancel()

