"""Countdown timer for quiz questions."""

import time
import threading


class CountdownTimer:
    """Simple countdown timer for per-question time limits."""

    def __init__(self, seconds: int):
        self.total = seconds
        self.remaining = seconds
        self.running = False
        self.thread = None

    def start(self):
        """Start the countdown timer."""
        self.remaining = self.total
        self.running = True
        self.thread = threading.Thread(target=self._countdown, daemon=True)
        self.thread.start()

    def _countdown(self):
        """Countdown in background."""
        while self.remaining > 0 and self.running:
            time.sleep(1)
            self.remaining -= 1

    def stop(self):
        """Stop the timer."""
        self.running = False

    def is_expired(self) -> bool:
        """Check if time is up."""
        return self.remaining <= 0

    def get_remaining(self) -> int:
        """Get remaining seconds."""
        return max(0, self.remaining)
