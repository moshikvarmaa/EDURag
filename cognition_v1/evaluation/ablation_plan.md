# Cognition V1 Ablation Plan

## Objective
Measure the incremental contribution of conversational signals, temporal features and FSM context.

## Conditions

A. Baseline RAG: existing EDURag retrieval/generation without Cognition context.

B. RAG + conversational signals: add extracted signal labels.

C. RAG + signals + temporal: add inter-arrival/exponential features.

D. RAG + signals + temporal + FSM: add evolving learner state.

## Primary outcomes

- Signal classification: precision, recall, macro-F1 against human annotations.
- Temporal model: AIC/BIC and KS statistic for exponential, Gamma and Weibull alternatives.
- State modeling: agreement with human state annotations and transition stability.
- Response quality: relevance, clarity, helpfulness and personalization, assessed with a predefined rubric.

## Fair comparison

Keep the underlying knowledge base, retrieval corpus, LLM, prompts unrelated to the learner-state component, and evaluation questions fixed across conditions. Change only the Cognition context supplied to the response generator.

## No-result rule

Do not write numerical claims until the experiment has been executed on a defined evaluation dataset. Synthetic development data may validate code paths but is excluded from research evidence.
