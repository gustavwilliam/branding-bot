import asyncio
from loguru import logger
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, TypeVar



_EXECUTOR = ThreadPoolExecutor(10)
T = TypeVar("T")


async def in_executor(func: Callable[..., T], *args, **kwargs) -> T:
    """
    Runs the given synchronous function `func` in an executor.
    This is useful for running slow, blocking code within async
    functions, so that they don't block the bot.
    """
    logger.debug(f"Running {func.__name__} in an executor.")
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_EXECUTOR, func, *args, **kwargs)
