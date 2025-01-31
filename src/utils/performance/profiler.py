import cProfile
import pstats
import time
from functools import wraps

class PerformanceProfiler:
    @staticmethod
    def profile(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            profiler = cProfile.Profile()
            profiler.enable()
            start_time = time.time()
            
            result = func(*args, **kwargs)
            
            end_time = time.time()
            profiler.disable()
            
            stats = pstats.Stats(profiler)
            stats.sort_stats('cumtime')
            stats.print_stats(10)
            
            print(f"Execution time: {end_time - start_time:.4f}s")
            return result
        return wrapper

    @staticmethod
    def benchmark(runs=1000):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                times = []
                for _ in range(runs):
                    start = time.perf_counter_ns()
                    result = func(*args, **kwargs)
                    end = time.perf_counter_ns()
                    times.append(end - start)
                avg = sum(times) / len(times)
                print(f"Average execution: {avg/1e6:.4f}ms over {runs} runs")
                return result
            return wrapper
        return decorator
