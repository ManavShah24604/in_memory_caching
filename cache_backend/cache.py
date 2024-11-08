from abc import ABC, abstractmethod
from threading import Lock
from typing import TypeVar, Generic, Optional, Dict, Any, Dict

from cache_backend.eviction_policy import EvictionPolicy

K = TypeVar('K')  # Key type
V = TypeVar('V')  # Value type

class Cache(Generic[K, V]):
    """Thread-safe in-memory cache with configurable eviction policies."""
    
    def __init__(self, capacity: int, eviction_policy: EvictionPolicy[K]):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
            
        self.capacity = capacity
        self.eviction_policy = eviction_policy
        self.cache: Dict[K, V] = {}
        self.lock = Lock()

    def get(self, key: K) -> Optional[V]:
        """
        Retrieve an item from the cache.
        Returns None if the key doesn't exist.
        """
        with self.lock:
            if key in self.cache:
                self.eviction_policy.on_get(key)
                return self.cache[key]
            return None

    def put(self, key: K, value: V) -> None:
        """
        Add an item to the cache.
        If the cache is full, evicts an item according to the eviction policy.
        """
        with self.lock:
            if key in self.cache:
                self.cache[key] = value
                self.eviction_policy.on_get(key)
            else:
                if len(self.cache) >= self.capacity:
                    evicted_key = self.eviction_policy.evict()
                    del self.cache[evicted_key]
                self.cache[key] = value
                self.eviction_policy.on_put(key)

    def remove(self, key: K) -> bool:
        """
        Remove an item from the cache.
        Returns True if the item was removed, False if it didn't exist.
        """
        with self.lock:
            if key in self.cache:
                del self.cache[key]
                self.eviction_policy.on_remove(key)
                return True
            return False

    def clear(self) -> None:
        """Remove all items from the cache."""
        with self.lock:
            self.cache.clear()

    def size(self) -> int:
        """Return the current number of items in the cache."""
        with self.lock:
            return len(self.cache)