from collections import defaultdict
from typing import TypeVar, Generic, Optional, Dict, Deque
from abc import ABC, abstractmethod
from cache_backend.eviction_policy import EvictionPolicy
from cache_backend.utils.doubly_linked_list import DoublyLinkedList, Node

K = TypeVar('K')  # Key type

class LFUEvictionPolicy(EvictionPolicy[K]):
    """Least Frequently Used eviction policy."""
    
    def __init__(self):
        # Tracks frequency lists with doubly linked lists for each frequency level
        self.freq_map: Dict[int, DoublyLinkedList[K]] = defaultdict(DoublyLinkedList)
        self.key_map: Dict[K, (Node[K], int)] = {}  # Maps keys to (node, frequency)
        self.min_freq = 0  # Track the minimum frequency in the cache

    def on_get(self, key: K) -> None:
        if key in self.key_map:
            node, freq = self.key_map[key]
            self._update_frequency(key, node, freq)

    def on_put(self, key: K) -> None:
        if key in self.key_map:
            node, freq = self.key_map[key]
            self._update_frequency(key, node, freq)
        else:
            # New key with frequency 1
            node = self.freq_map[1].add_to_front(key)
            self.key_map[key] = (node, 1)
            self.min_freq = 1  # Reset min frequency to 1 for new entry

    def evict(self) -> K:
        if self.min_freq not in self.freq_map or self.freq_map[self.min_freq].is_empty():
            raise ValueError("No keys to evict")
        
        # Evict from the least frequently accessed list
        evict_key = self.freq_map[self.min_freq].remove_from_end()
        if evict_key is not None:
            del self.key_map[evict_key]
        
        if self.freq_map[self.min_freq].is_empty():
            del self.freq_map[self.min_freq]

        return evict_key

    def remove(self, key: K) -> None:
        if key in self.key_map:
            node, freq = self.key_map[key]
            self.freq_map[freq].remove_node(node)
            del self.key_map[key]
            if self.min_freq == freq and self.freq_map[freq].is_empty():
                del self.freq_map[freq]

    def _update_frequency(self, key: K, node: Node[K], freq: int) -> None:
        self.freq_map[freq].remove_node(node)
        if self.freq_map[freq].is_empty():
            del self.freq_map[freq]
            if self.min_freq == freq:
                self.min_freq += 1

        new_freq = freq + 1
        new_node = self.freq_map[new_freq].add_to_front(key)
        self.key_map[key] = (new_node, new_freq)
