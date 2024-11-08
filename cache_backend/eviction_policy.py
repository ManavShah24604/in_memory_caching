from typing import TypeVar, Generic
from abc import ABC, abstractmethod


K = TypeVar('K')  # Key type
V = TypeVar('V')  # Value type
class EvictionPolicy(ABC, Generic[K]):
    """Abstract base class for cache eviction policies."""
    
    @abstractmethod
    def on_get(self, key: K) -> None:
        """Called when an item is accessed."""
        pass
    def on_remove(self, key: K) -> None:
        """Called when an item is removed."""
        pass
    
    @abstractmethod
    def on_put(self, key: K) -> None:
        """Called when an item is added."""
        pass
    
    @abstractmethod
    def evict(self) -> K:
        """Returns the key of the item to be evicted."""
        pass