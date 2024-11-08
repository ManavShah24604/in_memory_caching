from cache_backend.cache import Cache
from cache_backend.LRU import LRUEvictionPolicy

cache = Cache[str, int](2, LRUEvictionPolicy())

cache.put("1", 1)
cache.put("2", 2)
cache.put("3", 3)

cache.remove("3")
print(cache.get("1"))
print(cache.get("2"))
print(cache.get("3"))
