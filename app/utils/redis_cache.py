from functools import wraps
from typing import Any, Callable

from app.utils.client import r_client
from orjson import orjson
from pydantic import BaseModel


def redis_cache(ttl: int = 60):
    """
    Asynchronous decorator for caching function results using Redis.

    :param ttl: Cache lifetime in seconds (default is 60 seconds)
    :return: Cached result or the result of the function execution if it is not in the cache.
    """

    def decorator(func: Callable[..., Any]):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            """
            Asynchronous wrapper for caching function result
            :param args: Positional arguments passed to the original function.
            :param kwargs: Keyword arguments passed to the original function.
            :return: Cached result or the result of the original function execution.
            """
            ignore_cache = kwargs.pop('ignore_cache', False)
            cache_key = f"{func.__name__}_{args}_{kwargs}"

            async def get_and_cache_result():
                result = await func(*args, **kwargs)

                # Преобразуем Pydantic модели в словарь перед сериализацией
                if isinstance(result, (list, tuple)):
                    serialized_result = [item.model_dump() if isinstance(item, BaseModel) else item for item in result]
                elif isinstance(result, BaseModel):
                    serialized_result = result.model_dump()
                else:
                    serialized_result = result

                await r_client.setex(cache_key, ttl, orjson.dumps(serialized_result))
                return result

            if ignore_cache:
                return await get_and_cache_result()

            cached_result = await r_client.get(cache_key)

            if cached_result:
                return orjson.loads(cached_result)

            return await get_and_cache_result()

        return wrapper

    return decorator
