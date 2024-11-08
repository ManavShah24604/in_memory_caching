from collections import deque
from typing import TypeVar, Generic, Optional, Dict, Deque
from abc import ABC, abstractmethod
from cache_backend.eviction_policy import EvictionPolicy

from cache_backend.utils.doubly_linked_list import DoublyLinkedList,Node

K = TypeVar('K')  # Key type


class LRUEvictionPolicy(EvictionPolicy[K]):
    """Least Recently Used eviction policy."""
    
    def __init__(self):
        self.list = DoublyLinkedList[K]()
        self.key_map: Dict[K, Node[K]] = {}

    def on_get(self, key: K) -> None:
        if key in self.key_map:
            node = self.key_map[key]
            self.list.move_to_front(node)

    def on_put(self, key: K) -> None:
        if key in self.key_map:
            node = self.key_map[key]
            self.list.move_to_front(node)
        else:
            node = self.list.add_to_front(key)
            self.key_map[key] = node

    def evict(self) -> K:
        if not self.list.tail:
            raise ValueError("No keys to evict")
        key = self.list.remove_from_end()
        if key is not None:
            del self.key_map[key]
        return key

    def remove(self, key: K) -> None:
        if key in self.key_map:
            node = self.key_map[key]
            self.list.remove_node(node)
            del self.key_map[key]
