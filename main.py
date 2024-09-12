import asyncio
from functools import wraps


class Cache:
    def __init__(self):
        self.data = {}

    def __call__(self, func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            key = (func, args, frozenset(kwargs.items()))
            if key in self.data:
                return self.data[key]
            result = await func(*args, **kwargs)
            self.data[key] = result
            return result

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            key = (func, args, frozenset(kwargs.items()))
            if key in self.data:
                return self.data[key]
            result = func(*args, **kwargs)
            self.data[key] = result
            return result

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    def invalidate(self, func):
        keys_to_remove = [key for key in self.data if key[0] == func]
        for key in keys_to_remove:
            del self.data[key]


cache = Cache()


@cache
def slow_function(arg):
    return arg


class MyClass:
    @cache
    def method(self, arg):
        return arg


@cache
async def async_func(arg):
    return arg
