from __future__ import annotations

from dataclasses import dataclass


STATES = (
    "START",
    "LEARNING",
    "CLARIFICATION_NEEDED",
    "NEEDS_PRACTICE",
    "IMPROVING",
    "MASTERED",
)


@dataclass
class LearnerFSM:
    state: str = "START"

    def transition(self, signals: set[str]) -> str:
        """Apply transparent V1 transitions.

        These rules are an initial engineering hypothesis and must be
        evaluated/revised against annotated interaction data.
        """
        if self.state == "START":
            self.state = "LEARNING"
        elif "SUCCESS" in signals and self.state in {"NEEDS_PRACTICE", "CLARIFICATION_NEEDED"}:
            self.state = "IMPROVING"
        elif "CONFUSION" in signals or "CLARIFICATION" in signals:
            self.state = "CLARIFICATION_NEEDED"
        elif "EXAMPLE_SEEKING" in signals or "CONCEPT_REVISIT" in signals:
            self.state = "NEEDS_PRACTICE"
        elif "SUCCESS" in signals and self.state == "IMPROVING":
            self.state = "MASTERED"
        return self.state
