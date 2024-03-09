
import time
import sys
from collections import OrderedDict
from typing import Callable
import random


class LruCache:
    def __init__(self, func:Callable, size:int=None, capacity:int=None) -> None:
        self.size = size
        self.func = func
        self.capacity = capacity
        self.__cache = OrderedDict()
        self.cache_info = {
            'hits': 0,
            'miss': 0,
            'current_capacity': 0,
            'current_cache_size': 0 
        }

    def __call__(self, *args, **kwargs) -> Callable:
        cache_key = args+tuple(kwargs.keys())
        get_item = self.get(cache_key)
        if get_item is None:
            cal_val = self.func(*args, **kwargs)
            self.put(cache_key, cal_val)
            return cal_val
        return get_item
    
    def get(self, key):
        try:
            item = self.__cache.pop(key)
            self.__cache[key] = item
            self.cache_info['hits'] = self.cache_info['hits']+1
            return item
        except KeyError:
            self.cache_info['miss'] = self.cache_info['miss']+1
            return None
        
    def __insert(self, key, value):
        '''
        insert by removing least recently used item when capacity/size is maxed
        '''
        self.__cache.popitem(last=False)

        self.__cache[key] = value
        
        if self.capacity is not None:
            self.cache_info['current_capacity'] = len(self.__cache)
        
        if self.size is not None:
            self.cache_info['current_cache_size'] = sys.getsizeof(self.__cache)
    
    def put(self, key, value):
        if self.size is not None:
            if self.cache_info['current_cache_size'] >= self.size:
                self.__insert(key, value)
        if self.capacity is not None:
            if self.cache_info['current_capacity'] >= self.capacity:
                self.__insert(key, value)
        self.__cache[key] = value
        self.cache_info['current_capacity'] = len(self.__cache)
        self.cache_info['current_cache_size'] = sys.getsizeof(self.__cache)


def lru_cache(size=None, capacity=None):
    def decorate(func):
        global cache_info
        inst = LruCache(func, size, capacity)
        cache_info = inst.cache_info
        return inst
    return decorate


@lru_cache(size=1024)
def test(i):
    print(test.cache_info)
    time.sleep(3)
    return i


for i in range(100):
    
    rand = random.choice(range(1,20))
    print(i, rand)
    t = test(rand)
    # print(cache_info)