from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


SIGNALS = {
    "CONFUSION",
    "CLARIFICATION",
    "EXAMPLE_SEEKING",
    "CONCEPT_REVISIT",
    "SUCCESS",
}


@dataclass(frozen=True)
class Interaction:
    learner_id: str
    session_id: str
    timestamp: str
    topic_id: str
    message: str
    outcome: bool | None = None


def extract_conversational_signals(
    interaction: Interaction,
    previous_topic_ids: Iterable[str] = (),
) -> list[str]:
    """Return transparent V1 heuristic signals.

    This is deliberately a baseline, not a psychological classifier.
    """
    text = interaction.message.lower().strip()
    signals: list[str] = []

    confusion_terms = (
        "don't understand",
        "do not understand",
        "still confused",
        "confused",
        "not clear",
        "why does",
        "i don't get",
    )
    clarification_terms = (
        "explain again",
        "explain that again",
        "clarify",
        "simplify",
        "explain this",
        "what do you mean",
    )
    example_terms = (
        "example",
        "worked example",
        "show me",
        "give me a problem",
        "real world example",
    )

    if any(term in text for term in confusion_terms):
        signals.append("CONFUSION")
    if any(term in text for term in clarification_terms):
        signals.append("CLARIFICATION")
    if any(term in text for term in example_terms):
        signals.append("EXAMPLE_SEEKING")
    if interaction.topic_id in set(previous_topic_ids):
        signals.append("CONCEPT_REVISIT")
    if interaction.outcome is True:
        signals.append("SUCCESS")

    return signals
