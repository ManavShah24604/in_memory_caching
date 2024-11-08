
import unittest
import threading
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Set, Type
from cache_backend.cache import Cache
from cache_backend.eviction_policy import EvictionPolicy
from cache_backend.FIFO import  FIFOEvictionPolicy
from cache_backend.LRU import  LRUEvictionPolicy
from cache_backend.LIFO import  LIFOEvictionPolicy

class TestCache(unittest.TestCase):
    def test_fifo_eviction(self):
        cache = Cache[str, int](2, FIFOEvictionPolicy())
        
        # Test basic FIFO behavior
        cache.put("1", 1)
        cache.put("2", 2)
        cache.put("3", 3)  # Should evict "1"
        
        self.assertIsNone(cache.get("1"))
        self.assertEqual(cache.get("2"), 2)
        self.assertEqual(cache.get("3"), 3)
        
        # Test that getting items doesn't affect order
        cache.get("2")
        cache.get("2")
        cache.put("4", 4)  # Should evict "2"
        self.assertIsNone(cache.get("2"))
        self.assertEqual(cache.get("3"), 3)
        self.assertEqual(cache.get("4"), 4)

    def test_lru_eviction(self):
        cache = Cache[str, int](2, LRUEvictionPolicy())
        
        # Test basic LRU behavior
        cache.put("1", 1)
        cache.put("2", 2)
        cache.get("1")  # Make "1" most recently used
        cache.put("3", 3)  # Should evict "2"
        
        self.assertEqual(cache.get("1"), 1)
        self.assertIsNone(cache.get("2"))
        self.assertEqual(cache.get("3"), 3)
        
        # Test that accessing items affects order
        cache.get("1")
        cache.put("4", 4)  # Should evict "3"
        self.assertEqual(cache.get("1"), 1)
        self.assertIsNone(cache.get("3"))
        self.assertEqual(cache.get("4"), 4)

    def test_lifo_eviction(self):
        cache = Cache[str, int](2, LIFOEvictionPolicy())
        
        # Test basic LIFO behavior
        cache.put("1", 1)
        cache.put("2", 2)
        cache.put("3", 3)  # Should evict "2"
        
        self.assertEqual(cache.get("1"), 1)
        self.assertIsNone(cache.get("2"))
        self.assertEqual(cache.get("3"), 3)
        
        # Test that getting items doesn't affect order
        cache.get("3")
        cache.get("3")
        cache.put("4", 4)  # Should evict "3"
        self.assertEqual(cache.get("1"), 1)
        self.assertIsNone(cache.get("3"))
        self.assertEqual(cache.get("4"), 4)

    def test_remove_operation(self):
        for policy in [FIFOEvictionPolicy, LRUEvictionPolicy, LIFOEvictionPolicy]:
            with self.subTest(policy=policy.__name__):
                cache = Cache[str, int](3, policy())
                
                cache.put("1", 1)
                cache.put("2", 2)
                cache.put("3", 3)
                
                self.assertTrue(cache.remove("2"))
                self.assertFalse(cache.remove("nonexistent"))
                
                cache.put("4", 4)  # Should not trigger eviction
                self.assertEqual(cache.size(), 3)
                
                # Verify correct items remain
                self.assertEqual(cache.get("1"), 1)
                self.assertIsNone(cache.get("2"))
                self.assertEqual(cache.get("3"), 3)
                self.assertEqual(cache.get("4"), 4)

    def test_thread_safety(self):
        for policy in [FIFOEvictionPolicy, LRUEvictionPolicy, LIFOEvictionPolicy]:
            with self.subTest(policy=policy.__name__):
                self._test_thread_safety_for_policy(policy)

    def _test_thread_safety_for_policy(self, policy: Type[EvictionPolicy]):
        cache = Cache[int, int](100, policy())
        num_threads = 10
        operations_per_thread = 1000
        
        # Track what should be in the cache
        successful_puts: Set[int] = set()
        
        def worker() -> List[str]:
            local_logs = []
            for _ in range(operations_per_thread):
                op = random.choice(['get', 'put', 'remove'])
                key = random.randint(1, 150)  # Using range larger than cache size
                
                if op == 'get':
                    value = cache.get(key)
                    if value is not None:
                        local_logs.append(f"Successfully got {key}={value}")
                elif op == 'put':
                    value = random.randint(1, 1000)
                    cache.put(key, value)
                    successful_puts.add(key)
                    local_logs.append(f"Put {key}={value}")
                else:  # remove
                    if cache.remove(key):
                        local_logs.append(f"Removed {key}")
                
                # Randomly sleep to increase chance of race conditions
                if random.random() < 0.1:
                    time.sleep(0.001)
            
            return local_logs

        # Run threads
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(worker) for _ in range(num_threads)]
            all_logs = []
            for future in as_completed(futures):
                all_logs.extend(future.result())

        # Verify cache state
        self.assertLessEqual(cache.size(), 100)  # Should never exceed capacity
        
        # Verify no duplicate keys in eviction policy
        seen_keys = set()
        evicted = set()
        
        # Force eviction of all items to verify no duplicates
        while cache.size() > 0:
            try:
                key = cache.eviction_policy.evict()
                self.assertNotIn(key, seen_keys)
                self.assertNotIn(key, evicted)
                seen_keys.add(key)
                evicted.add(key)
            except ValueError:
                break

if __name__ == '__main__':
    unittest.main()