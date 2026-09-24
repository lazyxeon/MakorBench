from __future__ import annotations

from .clock import FakeClock
from .telemetry import Telemetry


class TokenManager:
    def __init__(self, clock: FakeClock, telemetry: Telemetry) -> None:
        self._clock = clock
        self._telemetry = telemetry
        self._generation = 1
        self._current_token = self._make_token(self._generation)
        self._telemetry.emit("identity", "token_issued", generation=self._generation)

    @staticmethod
    def _make_token(generation: int) -> str:
        return f"worker-service-token-{generation}"

    @property
    def current_token(self) -> str:
        return self._current_token

    @property
    def generation(self) -> int:
        return self._generation

    def rotate(self) -> str:
        self._generation += 1
        self._current_token = self._make_token(self._generation)
        self._telemetry.emit(
            "identity",
            "token_rotated",
            generation=self._generation,
        )
        return self._current_token
