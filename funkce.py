import time

def measure_time(func , *args, **kwargs):

    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    duration = end_time - start_time
    return result, duration
