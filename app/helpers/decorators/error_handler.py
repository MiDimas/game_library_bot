
from functools import wraps
from typing import Callable, TypeVar, ParamSpec, Awaitable

P = ParamSpec('P')
R = TypeVar('R')


def async_error_handler(func: Callable[P,  Awaitable[R]]) -> Callable[P, Awaitable[R]]:
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            print(e)
            return None
    return wrapper

