# Cognition V1 — Interaction Dataset

This directory defines the dataset format for the Cognition learner-signal experiment.

## Goal

Capture timestamped, concept-linked learner interactions so we can test whether temporal interaction features add useful information to conversational learner-signal extraction.

## Record schema

Each JSONL record should contain:

```json
{
  "learner_id": "L001",
  "session_id": "S001",
  "timestamp": "2026-08-29T10:02:10+05:30",
  "topic_id": "recursion",
  "message": "Can you explain recursion?",
  "signals": ["CLARIFICATION"],
  "outcome": null
}
```

## Initial signal labels

- CONFUSION
- CLARIFICATION
- EXAMPLE_SEEKING
- CONCEPT_REVISIT
- SUCCESS

Multiple labels may be assigned to one interaction.

## Important

Synthetic data may be used to validate the software pipeline, but synthetic data must not be presented as evidence of real learner behavior. Real learner studies require appropriate consent, privacy protection, and institutional approval where applicable.
