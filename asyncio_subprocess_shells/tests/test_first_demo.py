import asyncio
import logging
import sys

import pytest

from colorama import Fore, init

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def run(cmd, color: Fore):
    logger.info(color + f"Starting execution of %r" + Fore.RESET, cmd)
    await asyncio.sleep(2)
    proc = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await proc.communicate()

    logger.info(
        color + f"[{cmd!r} exited with {proc.returncode}]" + Fore.RESET
    )
    if stdout:
        logger.info(color + f"[stdout]\n{stdout.decode()}" + Fore.RESET)
    if stderr:
        logger.warning(color + f"[stderr]\n{stderr.decode()}" + Fore.RESET)


async def daemon_script():
    while True:
        logger.info(Fore.LIGHTMAGENTA_EX + "Doing some job!" + Fore.RESET)
        await asyncio.sleep(1)


@pytest.mark.asyncio
async def test_run():
    init(autoreset=True)
    daemon = asyncio.Task(daemon_script())
    results = asyncio.gather(
        run("ls -al", Fore.RED),
        run("sleep 1; echo 'Finished sleeping'", Fore.BLUE),
        run("ssdsd", Fore.CYAN),
    )
    await results
    daemon.cancel()
