from cache_backend.cache import Cache
from LFU import LFUEvictionPolicy

cache = Cache[str, int](2, LFUEvictionPolicy())

cache.put("1", 1)
cache.put("1", 100)
cache.put("2", 2)
cache.put("3", 3)

print(cache.get("1"))
print(cache.get("2"))
print(cache.get("3"))
