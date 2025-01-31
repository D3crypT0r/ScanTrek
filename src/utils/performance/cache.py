import diskcache
from datetime import timedelta

class CacheManager:
    def __init__(self, cache_dir='.cache', ttl=3600):
        self.cache = diskcache.Cache(
            cache_dir,
            size_limit=2**30, 
            eviction_policy='least-recently-used'
        )
        self.ttl = ttl

    @ErrorHandler.retry
    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache.set(key, value, expire=self.ttl)

    def memoize(self, ttl=None):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                cache_key = self._generate_key(func.__name__, args, kwargs)
                cached = self.get(cache_key)
                if cached is not None:
                    return cached
                result = func(*args, **kwargs)
                self.set(cache_key, result, ttl or self.ttl)
                return result
            return wrapper
        return decorator

    def _generate_key(self, func_name, args, kwargs):
        return f"{func_name}-{hash(args)}-{hash(frozenset(kwargs.items()))}"
