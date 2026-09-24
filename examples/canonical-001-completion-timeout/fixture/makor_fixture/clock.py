from __future__ import annotations


class FakeClock:
    def __init__(self, start: float = 0.0) -> None:
        self._now = float(start)

    @property
    def now(self) -> float:
        return self._now

    def advance(self, seconds: float) -> float:
        if seconds < 0:
            raise ValueError("clock cannot move backwards")
        self._now += float(seconds)
        return self._now
