from functools import wraps


class Cache:
    def __init__(self):
        self.data = {}

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (func, args, frozenset(kwargs.items()))
            if key in self.data:
                return self.data[key]
            result = func(*args, **kwargs)
            self.data[key] = result
            return result

        return wrapper

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
