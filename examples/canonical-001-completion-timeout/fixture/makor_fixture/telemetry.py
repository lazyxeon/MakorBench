from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from .clock import FakeClock


@dataclass
class Telemetry:
    clock: FakeClock
    events: list[dict[str, Any]] = field(default_factory=list)

    def emit(self, service: str, event: str, **fields: Any) -> None:
        self.events.append(
            {
                "ts": round(self.clock.now, 6),
                "service": service,
                "event": event,
                **fields,
            }
        )

    def matching(self, *, service: str | None = None, event: str | None = None) -> list[dict[str, Any]]:
        result = self.events
        if service is not None:
            result = [item for item in result if item["service"] == service]
        if event is not None:
            result = [item for item in result if item["event"] == event]
        return list(result)

    def jsonl(self) -> str:
        return "\n".join(json.dumps(item, sort_keys=True) for item in self.events) + "\n"
