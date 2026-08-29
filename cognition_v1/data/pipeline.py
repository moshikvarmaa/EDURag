from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class Event:
    learner_id: str
    session_id: str
    timestamp: datetime
    topic_id: str
    message: str
    signals: tuple[str, ...]
    outcome: bool | None


def load_jsonl(path: str | Path) -> list[Event]:
    events: list[Event] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            try:
                events.append(
                    Event(
                        learner_id=str(row["learner_id"]),
                        session_id=str(row["session_id"]),
                        timestamp=datetime.fromisoformat(row["timestamp"]),
                        topic_id=str(row["topic_id"]),
                        message=str(row["message"]),
                        signals=tuple(row.get("signals", [])),
                        outcome=row.get("outcome"),
                    )
                )
            except (KeyError, TypeError, ValueError) as exc:
                raise ValueError(f"Invalid record at line {line_no}: {exc}") from exc
    return sorted(events, key=lambda event: event.timestamp)


def concept_inter_arrivals(events: list[Event]) -> dict[tuple[str, str, str], list[float]]:
    """Return positive inter-arrival times by learner/session/topic."""
    grouped: dict[tuple[str, str, str], list[Event]] = {}
    for event in events:
        key = (event.learner_id, event.session_id, event.topic_id)
        grouped.setdefault(key, []).append(event)

    result: dict[tuple[str, str, str], list[float]] = {}
    for key, sequence in grouped.items():
        sequence.sort(key=lambda event: event.timestamp)
        intervals = [
            (b.timestamp - a.timestamp).total_seconds()
            for a, b in zip(sequence, sequence[1:])
            if b.timestamp > a.timestamp
        ]
        if intervals:
            result[key] = intervals
    return result
