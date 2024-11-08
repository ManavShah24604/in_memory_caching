# In-Memory Cache Library

A thread-safe, generic-type in-memory caching library with support for multiple eviction policies.

## Features

- Generic type support for both keys and values
- Thread-safe operations
- Multiple built-in eviction policies:
  - FIFO (First In First Out)
  - LRU (Least Recently Used)
  - LIFO (Last In First Out)
- Support for custom eviction policies
- Clear and simple API

## Installation

Clone this repository:
```bash
git clone https://github.com/yourusername/cache-library.git
cd cache-library
```

## Usage

### Basic Usage

```python
from cache_backend.cache import Cache
from cache_backend.LRU import LRUEvictionPolicy

cache = Cache[str, int](2, LRUEvictionPolicy())

cache.put("1", 1)
cache.put("2", 2)
cache.put("3", 3)

print(cache.get("1"))
print(cache.get("2"))
print(cache.get("3"))

```

### Available Eviction Policies

1. **FIFO (First In First Out)**


2. **LRU (Least Recently Used)**


3. **LIFO (Last In First Out)**


### Creating Custom Eviction Policies

You can create custom eviction policies by implementing the `EvictionPolicy` abstract base class:

```python
from cache_backend import EvictionPolicy

class CustomEvictionPolicy(EvictionPolicy[K]):
    def __init__(self):
        # Initialize your policy state

    def on_get(self, key: K) -> None:
        # Handle item access

    def on_put(self, key: K) -> None:
        # Handle item addition

    def evict(self) -> K:
        # Return key to evict
```
- LFU.py can be considered as custom eviction policy. 

## Thread Safety

All cache operations are thread-safe by default. The implementation uses Python's threading.Lock to ensure thread safety.

## API Reference

### Cache Class

- `__init__(capacity: int, eviction_policy: EvictionPolicy[K])`: Initialize cache with given capacity and eviction policy
- `get(key: K) -> Optional[V]`: Retrieve item from cache
- `put(key: K, value: V) -> None`: Add item to cache
- `remove(key: K) -> bool`: Remove item from cache
- `clear() -> None`: Remove all items from cache
- `size() -> int`: Get current number of items in cache

### EvictionPolicy Class

- `on_get(key: K) -> None`: Called when an item is accessed
- `on_put(key: K) -> None`: Called when an item is added
- `evict() -> K`: Returns the key of the item to be evicted

## Testing
- Unit testing is done for logic of multiple caching technique ans also concurrency check is done by using threads.
