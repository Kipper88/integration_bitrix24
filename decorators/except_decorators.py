from asyncio import iscoroutinefunction
import functools
import logging

logger = logging.getLogger("webhook")

def async_exception_logger(func):
    if not iscoroutinefunction(func):
        raise TypeError("Этот декоратор предназначен только для асинхронных функций")

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.exception(f"Ошибка при обработке ({func.__name__}): {e}")
            
    return wrapper