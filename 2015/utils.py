import timeit
import psutil
import os

def measure_runtime(func, repeat=None, number=None):
    def wrapper(*args, **kwargs):
        avg_time = sum(timeit.repeat(lambda: func(*args, **kwargs), number=number, repeat=repeat)) / repeat
        print(f"Execution time: {avg_time:.9f} seconds")
        return func(*args, **kwargs)
    return wrapper

def measure_memory(func):
    def wrapper(*args, **kwargs):
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss
        result = func(*args, **kwargs)
        mem_after = process.memory_info().rss
        print(f"Memory usage: {(mem_after - mem_before)/1024:.4f} KB")
        return result
    return wrapper