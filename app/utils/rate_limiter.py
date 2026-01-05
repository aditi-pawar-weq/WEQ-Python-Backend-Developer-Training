import time
from collections import deque
from threading import Lock
from typing import Deque, Dict


class RateLimiter:
    """Simple in-memory rate limiter for demo/testing.

    Not suitable for production (use Redis or a distributed store).
    """

    def __init__(self, limit: int = 5, window_seconds: int = 60):
        self.limit = limit
        self.window = window_seconds
        self.store: Dict[str, Deque[float]] = {}
        self.lock = Lock()

    def allow(self, key: str) -> bool:
        """Return True if the key is allowed (below the rate limit)."""
        now = time.time()
        with self.lock:
            q = self.store.get(key)
            if q is None:
                q = deque()
                self.store[key] = q

            # Pop timestamps older than window
            while q and (now - q[0]) > self.window:
                q.popleft()

            if len(q) < self.limit:
                q.append(now)
                return True
            return False

    def reset(self, key: str) -> None:
        with self.lock:
            if key in self.store:
                del self.store[key]
