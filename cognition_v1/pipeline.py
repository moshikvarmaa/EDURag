from __future__ import annotations

from pathlib import Path

from data.pipeline import load_jsonl, concept_inter_arrivals
from signals.signal_extractor import Interaction, extract_conversational_signals
from statistics.exponential import fit_exponential
from state.fsm import LearnerFSM


def run(dataset: str | Path) -> list[dict]:
    events = load_jsonl(dataset)
    temporal = concept_inter_arrivals(events)
    fsm_by_learner: dict[str, LearnerFSM] = {}
    previous_topics: dict[str, list[str]] = {}
    rows: list[dict] = []

    for event in events:
        interaction = Interaction(
            learner_id=event.learner_id,
            session_id=event.session_id,
            timestamp=event.timestamp.isoformat(),
            topic_id=event.topic_id,
            message=event.message,
            outcome=event.outcome,
        )
        signals = extract_conversational_signals(
            interaction, previous_topics.get(event.learner_id, [])
        )
        fsm = fsm_by_learner.setdefault(event.learner_id, LearnerFSM())
        state = fsm.transition(set(signals))
        key = (event.learner_id, event.session_id, event.topic_id)
        estimate = fit_exponential(temporal[key]) if key in temporal else None

        rows.append(
            {
                "learner_id": event.learner_id,
                "session_id": event.session_id,
                "topic_id": event.topic_id,
                "timestamp": event.timestamp.isoformat(),
                "signals": signals,
                "state": state,
                "mean_interval_seconds": (
                    estimate.mean_interval_seconds if estimate else None
                ),
                "lambda": estimate.rate_lambda if estimate else None,
            }
        )
        previous_topics.setdefault(event.learner_id, []).append(event.topic_id)

    return rows


if __name__ == "__main__":
    import json

    dataset = Path(__file__).parent / "data" / "sample_interactions.jsonl"
    print(json.dumps(run(dataset), indent=2))
