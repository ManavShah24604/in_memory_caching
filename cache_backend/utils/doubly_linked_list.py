
from abc import ABC, abstractmethod
from threading import Lock
from typing import TypeVar, Generic, Optional, Dict, Any

K = TypeVar('K')  # Key type
V = TypeVar('V')  # Value type

class Node(Generic[K]):
    """Node class for doubly linked list implementation."""
    def __init__(self, key: K):
        self.key = key
        self.prev: Optional[Node[K]] = None
        self.next: Optional[Node[K]] = None

class DoublyLinkedList(Generic[K]):
    """Custom implementation of doubly linked list."""
    
    def __init__(self):
        self.head: Optional[Node[K]] = None
        self.tail: Optional[Node[K]] = None
        self._size = 0

    def add_to_front(self, key: K) -> Node[K]:
        """Add a node to the front of the list."""
        new_node = Node(key)
        self._size += 1
        
        if not self.head:
            self.head = self.tail = new_node
            return new_node
            
        new_node.next = self.head
        self.head.prev = new_node
        self.head = new_node
        return new_node

    def add_to_end(self, key: K) -> Node[K]:
        """Add a node to the end of the list."""
        new_node = Node(key)
        self._size += 1
        
        if not self.tail:
            self.head = self.tail = new_node
            return new_node
            
        new_node.prev = self.tail
        self.tail.next = new_node
        self.tail = new_node
        return new_node

    def remove_node(self, node: Node[K]) -> None:
        """Remove a specific node from the list."""
        if not node:
            return
            
        self._size -= 1
        
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
            
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev

    def remove_from_front(self) -> Optional[K]:
        """Remove and return the first node's key."""
        if not self.head:
            return None
            
        key = self.head.key
        self.remove_node(self.head)
        return key

    def remove_from_end(self) -> Optional[K]:
        """Remove and return the last node's key."""
        if not self.tail:
            return None
            
        key = self.tail.key
        self.remove_node(self.tail)
        return key

    def move_to_front(self, node: Node[K]) -> None:
        """Move a given node to the front of the list."""
        if node == self.head:
            return
            
        self.remove_node(node)
        node.prev = None
        node.next = self.head
        
        if self.head:
            self.head.prev = node
        self.head = node
        
        if not self.tail:
            self.tail = node

    def size(self) -> int:
        """Return the current size of the list."""
        return self._size

    def is_empty(self):
        """Check if the list is empty."""
        return self._size == 0
