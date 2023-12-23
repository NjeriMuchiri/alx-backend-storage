#!/usr/bin/env python3
"""This is the cache class"""


import redis
import uuid
from typing import Union, Callable
from functools import wraps


# def count_calls(method: Callable) -> Callable:
#     @wraps(method)
#     def wrapper(self, *args, **kwargs):
#         key = method.__qualname__
#         self._redis.incr(key)
#         return method(self, *args, **kwargs)
#     return wrapper

def call_history(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = "{}:inputs".format(method.__qualname__)
        output_key = "{}:outputs".format(method.__qualname__)

        """Appends input arguments to the inputs list"""
        self._redis.rpush(input_key, str(args))

        """Executes the wrapped function to retrieve the output"""
        output = method(self, *args, **kwargs)

        """Store the output in the outputs list"""
        self._redis.rpush(output_key, str(output))

        return output

    return wrapper

def replay(method: Callable):
    """Function to display the history of calls for a certain function"""
    input_key = "{}:inputs".format(method.__qualname__)
    output_key = "{}:outputs".format(method.__qualname__)

    inputs = cache._redis.lrange(input_key, 0, -1)
    outputs = cache._redis.lrange(output_key, 0, -1)

    print("{} was called {} times:".format(method.__qualname__, len(inputs)))

    for args, result in zip(inputs, outputs):
        args_str = args.decode("utf-8")
        result_str = result.decode("utf-8")
        print("{}(*{}) -> {}".format(method.__qualname__, args_str, result_str))

class Cache:
    """Cache class declaration"""
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store method"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float, None]:
        data = self._redis.get(key)
        if data is not None and fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        return self.get(key, fn=int)


if __name__ == "__main__":
    cache = Cache()

    data = b"hello"
    key = cache.store(data)
    print(key)

    local_redis = redis.Redis()
    print(local_redis.get(key))
