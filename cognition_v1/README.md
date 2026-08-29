# Cognition V1 Research Prototype

This prototype implements the first experimental pipeline described in the Cognition research paper.

## Current components

1. **Interaction schema** — timestamped, topic-linked learner events.
2. **Conversational signal baseline** — transparent heuristic extraction for five initial signals.
3. **Exponential temporal model** — estimates an interaction-rate feature from positive inter-arrival times.
4. **FSM learner state** — maps extracted signals to an interpretable evolving state.

## Architecture

```text
Student interactions
        |
        +--> conversational signals
        |
        +--> inter-arrival times --> exponential rate feature
        |
        +--------------+----------------+
                       |
                       v
                learner signals
                       |
                       v
                      FSM
                       |
                       v
                learner context
```

## Important research discipline

The exponential model is a **testable hypothesis**, not a claim that interaction frequency directly measures confusion, mastery, motivation, or ability. Short intervals can have many explanations. The V1 experiment must evaluate distribution fit and incremental predictive value.

The FSM transitions are also an initial engineering hypothesis. They must be evaluated against annotated data and revised when evidence requires it.

## Next implementation tasks

- Add a JSONL loader and timestamp parsing.
- Add concept-specific inter-arrival calculation.
- Add goodness-of-fit diagnostics and comparison against Weibull/Gamma alternatives.
- Build a human-annotated evaluation set.
- Implement semantic + temporal signal fusion.
- Add ablation experiments.
- Connect learner context to the existing EDURag retrieval/generation pipeline.

No experimental performance results are claimed yet.
