import pytest
import asyncio
from your_module import cache, slow_function, MyClass, async_func

@pytest.mark.asyncio
async def test_cache_async_function():
    result1 = await async_func(10)
    result2 = await async_func(10)
    assert result1 == result2
    assert cache.data[((async_func, (10,), frozenset()),)] == result1
    result3 = await async_func(20)
    assert result3 != result1
    assert cache.data[((async_func, (20,), frozenset()),)] == result3


def test_cache_sync_function():
    result1 = slow_function(5)
    result2 = slow_function(5)
    assert result1 == result2
    assert cache.data[((slow_function, (5,), frozenset()),)] == result1
    result3 = slow_function(7)
    assert result3 != result1
    assert cache.data[((slow_function, (7,), frozenset()),)] == result3


def test_cache_class_method():
    obj = MyClass()
    result1 = obj.method(15)
    result2 = obj.method(15)
    assert result1 == result2
    assert cache.data[((obj.method, (obj, 15), frozenset()),)] == result1
    result3 = obj.method(20)
    assert result3 != result1
    assert cache.data[((obj.method, (obj, 20), frozenset()),)] == result3


def test_cache_invalidation():
    result1 = slow_function(5)
    assert result1 == slow_function(5)
    assert cache.data[((slow_function, (5,), frozenset()),)] == result1
    cache.invalidate(slow_function)
    assert ((slow_function, (5,), frozenset()),) not in cache.data
    result2 = slow_function(5)
    assert result1 == result2
    assert cache.data[((slow_function, (5,), frozenset()),)] == result2
