from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy import stats

from data.pipeline import concept_inter_arrivals, load_jsonl
from signals.signal_extractor import Interaction, extract_conversational_signals
from statistics.exponential import fit_exponential


def evaluate(dataset: str | Path) -> dict:
    events = load_jsonl(dataset)
    temporal = concept_inter_arrivals(events)

    all_intervals = [value for values in temporal.values() for value in values]
    temporal_result = {}
    if all_intervals:
        estimate = fit_exponential(all_intervals)
        # scipy's one-sample KS statistic is a useful exploratory diagnostic.
        # The p-value is reported only as a diagnostic, not as proof of the model.
        ks = stats.kstest(all_intervals, "expon", args=(0, 1.0 / estimate.rate_lambda))
        temporal_result = {
            "sample_count": estimate.sample_count,
            "mean_interval_seconds": estimate.mean_interval_seconds,
            "lambda": estimate.rate_lambda,
            "ks_statistic": float(ks.statistic),
            "ks_p_value": float(ks.pvalue),
        }

    signal_counts: dict[str, int] = {}
    for event in events:
        interaction = Interaction(
            learner_id=event.learner_id,
            session_id=event.session_id,
            timestamp=event.timestamp.isoformat(),
            topic_id=event.topic_id,
            message=event.message,
            outcome=event.outcome,
        )
        previous_topics = [e.topic_id for e in events if e.learner_id == event.learner_id and e.timestamp < event.timestamp]
        for signal in extract_conversational_signals(interaction, previous_topics):
            signal_counts[signal] = signal_counts.get(signal, 0) + 1

    return {"event_count": len(events), "signal_counts": signal_counts, "temporal_model": temporal_result}


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    dataset = root / "data" / "sample_interactions.jsonl"
    result = evaluate(dataset)
    output = root / "evaluation" / "results.json"
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
