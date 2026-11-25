"""Bounded in-RAM diagnostic ring buffer."""


class RingLog:
    def __init__(self, capacity=32):
        self.capacity = int(capacity)
        if self.capacity < 1:
            raise ValueError("capacity must be at least 1")
        self._items = [None] * self.capacity
        self._head = 0
        self._size = 0

    def append(self, timestamp_ms, level, message):
        entry = {"timestamp_ms": int(timestamp_ms), "level": str(level), "message": str(message)}
        if self._size == self.capacity:
            self._items[self._head] = entry
            self._head = (self._head + 1) % self.capacity
        else:
            index = (self._head + self._size) % self.capacity
            self._items[index] = entry
            self._size += 1

    def items(self):
        result = []
        for offset in range(self._size):
            entry = self._items[(self._head + offset) % self.capacity]
            result.append(dict(entry))
        return result

    def clear(self):
        self._items = [None] * self.capacity
        self._head = 0
        self._size = 0
