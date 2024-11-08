from collections import deque
from typing import TypeVar, Generic, Optional, Dict, Deque
from abc import ABC, abstractmethod
from cache_backend.eviction_policy import EvictionPolicy

K = TypeVar('K')  # Key type

class FIFOEvictionPolicy(EvictionPolicy[K]):
    """First In First Out eviction policy using deque."""
    
    def __init__(self):
        self.queue: Deque[K] = deque()
        self.key_set: set[K] = set()

    def on_get(self, key: K) -> None:
        pass  # No change in order for FIFO

    def on_put(self, key: K) -> None:
        if key not in self.key_set:
            self.queue.append(key)
            self.key_set.add(key)

    def evict(self) -> K:
        if not self.queue:
            raise ValueError("No keys to evict")
        key = self.queue.popleft()
        self.key_set.remove(key)
        return key

    def remove(self, key: K) -> None:
        if key in self.key_set:
            self.key_set.remove(key)
            # Note: This is O(n), but it's only called during explicit remove
            self.queue.remove(key)
