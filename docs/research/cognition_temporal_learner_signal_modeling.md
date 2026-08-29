# Temporal-Behavioral Learner Signal Extraction for Conversational Learning Using Exponential Interaction Modeling and Finite-State Learner Representation

**Author:** Moshik Varmaa  
**Project:** Cognition / EDURag  
**Affiliation:** VIT Vellore  
**Status:** Research prototype proposal / V1 study draft  
**Version:** 1.0  

> **Research-status note:** This manuscript defines the proposed architecture, hypotheses, methodology, and evaluation protocol. It does **not** claim experimental results that have not yet been collected. Numerical results, statistical significance, and conclusions about model superiority must be added only after the V1 experiment is executed.

---

## Abstract

Large language model (LLM)-based tutoring systems can provide conversational support at scale, but effective personalization requires more than generating a relevant answer to the current question. A learner's sequence of questions, requests for clarification, repeated visits to a concept, and timing between related interactions can contain useful evidence about the learner's current learning situation. This paper proposes a learner-signal extraction architecture for Cognition, an AI learning-intelligence layer intended to complement retrieval-augmented generation (RAG) tutoring rather than replace human teachers. The proposed method combines conversational/semantic signals with temporal interaction features. Inter-arrival times between concept-related interactions are modeled initially with an exponential distribution as a testable statistical hypothesis, while a finite-state machine (FSM) represents an interpretable evolving learner state. The exponential component is not treated as a direct detector of confusion or mastery; instead, its estimated interaction-rate features are combined with semantic and behavioral evidence before state transitions are considered. The study proposes a baseline comparison between conventional RAG, RAG with conversational learner signals, and RAG with conversational signals plus temporal features and FSM-based state context. Evaluation will focus on signal classification, temporal-model fit, learner-state transition consistency, response personalization, and downstream learning performance. The contribution is a transparent, experimentally testable framework for incorporating temporal interaction dynamics into conversational learner modeling.

**Keywords:** learner modeling, conversational AI, intelligent tutoring systems, large language models, retrieval-augmented generation, learner signals, temporal interaction, exponential distribution, finite-state machine, personalization, educational AI.

---

## 1. Introduction

Personalized learning systems attempt to adapt educational content and interaction to differences among learners. Traditional classroom instruction, however, often operates under a one-to-many constraint: a teacher may simultaneously support many students who differ in prior knowledge, misconceptions, confidence, learning preferences, and pace. Digital tutoring systems can observe more interaction data than a human teacher can manually process, creating an opportunity to construct continuously updated learner models.

Recent work shows growing interest in conversational AI for education. Systematic reviews have identified educational chatbots as a rapidly developing area and have discussed their potential to personalize activities, support educators, and provide insight into learner behavior [1], [2]. Recent empirical work has also examined how students interact with AI tutors and how interaction patterns relate to learning engagement and outcomes [3], [4]. Student modeling remains central to personalized tutoring, with recent systems combining diagnostic information, learner characteristics, knowledge levels, and misconceptions with conversational tutoring [5], [6].

However, a conversational tutoring system commonly receives a sequence of learner messages rather than a clean sequence of pedagogically labeled events. A student's interaction can therefore be viewed from multiple perspectives: **what** the student says, **what behavior** the interaction represents, **which concept** is being revisited, and **when** the interaction occurs relative to earlier related interactions. The temporal dimension is particularly interesting because it can provide information that is not contained in message semantics alone.

This paper proposes Cognition's V1 learner-signal architecture around two complementary modeling mechanisms. First, semantic and behavioral analysis extracts interpretable learner signals such as confusion, clarification seeking, example seeking, concept revisiting, and successful follow-up performance. Second, temporal features are calculated from the inter-arrival times of related learner interactions. An exponential distribution is investigated as an initial model for these inter-arrival times. The resulting temporal features are then combined with conversational evidence and passed to an interpretable finite-state learner representation.

The core research question is:

> **Can temporal interaction characteristics, modeled statistically and combined with conversational signals, improve learner-signal extraction and support a more useful interpretable learner-state representation for conversational tutoring?**

The proposed study deliberately treats the exponential distribution as a hypothesis rather than a guaranteed property of learning behavior. Short interaction intervals do not necessarily mean confusion, and long intervals do not necessarily mean mastery. Engagement, task difficulty, interruptions, and external circumstances can also affect timing. Therefore, the statistical model must be evaluated against observed data and compared with alternative distributions when appropriate.

### Contributions

This paper proposes four contributions for the Cognition V1 research prototype:

1. **A multimodal learner-signal representation** that combines semantic, behavioral, topic, and temporal interaction evidence.
2. **A testable exponential inter-arrival model** for extracting temporal interaction features rather than treating the distribution as a direct psychological interpretation.
3. **An interpretable FSM-based learner-state layer** that maps accumulated learner signals to explicit state transitions.
4. **An evaluation protocol** comparing a conventional RAG baseline with increasingly learner-aware variants without claiming unmeasured results.

---

## 2. Problem Definition

Let a learner session consist of an ordered sequence of interactions:

\[
I = \{i_1,i_2,\ldots,i_n\}
\]

where each interaction is represented as:

\[
i_k=(u_k,t_k,c_k,m_k,o_k)
\]

where:

- \(u_k\) = learner identifier,
- \(t_k\) = timestamp,
- \(c_k\) = concept/topic identifier,
- \(m_k\) = learner message and associated conversational information,
- \(o_k\) = optional observable outcome, such as correctness on a follow-up task.

The objective is not to infer a hidden psychological state with certainty. Instead, the system estimates an interpretable **learner context** from observable interaction evidence.

We define a learner-signal vector:

\[
S_k = [s_{conf},s_{clar},s_{ex},s_{rev},s_{succ},s_{temp},\ldots]
\]

where example dimensions represent confusion evidence, clarification seeking, example seeking, concept revisiting, success evidence, and temporal interaction features.

The learner state at interaction \(k\) is then represented as:

\[
q_k = \delta(q_{k-1},S_k)
\]

where \(\delta\) is an interpretable transition function implemented as an FSM.

---

## 3. Related Work

### 3.1 Conversational AI for education

Educational chatbots have been studied as tools for engagement, tutoring, feedback, and personalized learning. Kuhail et al. reviewed educational chatbot research and identified potential for personalization and insight into learner behavior [1]. A later systematic review of conversational AI in English-language teaching found rapid growth in publications and highlighted the variety of research designs and learning outcomes investigated [2].

Recent work has moved beyond generic chatbot usage toward learner-aware tutoring. Park et al. proposed a conversation-based tutoring system with a student-modeling component that feeds assessment outcomes into an LLM-based tutor [5]. Looi and Jia empirically analyzed student-tutor bot interactions and examined the personalization affordances of current chatbot technology [4]. These studies motivate the need to treat the interaction history as a source of learner information rather than viewing each prompt in isolation.

### 3.2 Student modeling

Student modeling is a long-standing component of intelligent tutoring systems. Modern approaches include knowledge tracing, Bayesian learner models, psychometric models, and hybrid architectures. Nkambou et al. demonstrated a hybrid learner-modeling approach that combined expert-validated Bayesian modeling with deep knowledge tracing for logical reasoning [6]. Other recent work has modeled learner preferences, knowledge, and misconceptions to support customized learning [7].

Cognition differs in emphasis: the proposed V1 focuses on **interaction-derived learner signals** in conversational tutoring and explicitly investigates temporal interaction dynamics as an additional signal source.

### 3.3 Interaction dynamics

Recent educational research has increasingly analyzed sequences of student-AI interactions. Hao et al. analyzed large-scale dialogue data in a long-term multi-agent learning environment and identified interaction patterns such as knowledge co-construction and co-regulation [3]. This supports the premise that the sequence and structure of student-AI interaction can contain meaningful learning information.

The present work narrows this problem to a specific temporal feature: inter-arrival time between concept-related learner interactions. The proposed exponential model is intentionally modest and testable. If the observed data do not support the exponential assumption, alternative models such as Weibull or Gamma distributions should be evaluated rather than forcing an exponential interpretation.

### 3.4 Research gap

The literature establishes the importance of conversational tutoring, student modeling, and interaction analysis, but there remains room for a transparent architecture that explicitly combines: (1) conversational learner signals, (2) temporal interaction features, and (3) an interpretable finite-state learner representation. Cognition V1 targets this intersection as an experimentally testable prototype rather than claiming a complete theory of learning.

---

## 4. Proposed Cognition Architecture

The proposed architecture consists of six layers.

### 4.1 Interaction capture

The system records learner interactions with timestamps, session identifiers, topic/concept identifiers, message content, and available outcome information. Data collection should minimize personally identifiable information and use pseudonymous learner IDs for experiments.

### 4.2 Conversational signal extraction

The first signal layer classifies observable interaction patterns. V1 begins with five signals:

| Signal | Operational interpretation | Example |
|---|---|---|
| CONFUSION | Explicit or strongly implied difficulty | “I still don't understand.” |
| CLARIFICATION | Request to explain or re-explain | “Can you explain that again?” |
| EXAMPLE_SEEKING | Request for an example or worked case | “Can you show me an example?” |
| CONCEPT_REVISIT | Return to the same concept after a prior interaction | Repeated recursion questions |
| SUCCESS | Evidence of successful follow-up performance | Correct answer to a related check |

These signals are observable proxies, not diagnoses of a learner's psychological condition.

### 4.3 Temporal feature extraction

For two related learner interactions \(i_j\) and \(i_k\), the inter-arrival time is:

\[
\Delta t = t_k-t_j, \quad \Delta t>0
\]

For each concept/session sequence, the system collects a set of inter-arrival times:

\[
D_c=\{\Delta t_1,\Delta t_2,\ldots,\Delta t_m\}
\]

The initial hypothesis is that some interaction sequences may be reasonably approximated by an exponential distribution:

\[
f(t;\lambda)=\lambda e^{-\lambda t},\quad t\geq0
\]

with rate parameter:

\[
\hat{\lambda}=\frac{1}{\bar{t}}
\]

where \(\bar{t}\) is the sample mean of the observed inter-arrival times.

The model provides a **temporal feature**, not a semantic interpretation. For example, a higher estimated interaction rate can indicate that interactions are occurring more frequently, but it cannot independently establish that the learner is confused.

### 4.4 Learner-signal fusion

The temporal feature is combined with semantic and behavioral evidence:

\[
S_k = g(C_k,B_k,T_k,O_k)
\]

where:

- \(C_k\) = conversational/semantic features,
- \(B_k\) = behavioral sequence features,
- \(T_k\) = temporal features,
- \(O_k\) = observable outcome features.

The fusion function \(g\) can initially be rule-based for interpretability and later be replaced or compared with a learned classifier.

### 4.5 Finite-state learner representation

The learner model uses an FSM:

\[
M=(Q,\Sigma,\delta,q_0,F)
\]

where:

- \(Q\) = set of learner states,
- \(\Sigma\) = learner-signal/event alphabet,
- \(\delta\) = transition function,
- \(q_0\) = initial state,
- \(F\) = optional terminal/target states.

A candidate V1 state set is:

\[
Q=\{START,LEARNING,CLARIFICATION\_NEEDED,NEEDS\_PRACTICE,IMPROVING,MASTERED\}
\]

These states are engineering abstractions for interaction management. They are not claims that a learner literally occupies one psychological state at a time.

Example transitions include:

| Current state | Signal | Candidate next state |
|---|---|---|
| START | first learning interaction | LEARNING |
| LEARNING | strong clarification/confusion evidence | CLARIFICATION_NEEDED |
| CLARIFICATION_NEEDED | repeated example requests | NEEDS_PRACTICE |
| NEEDS_PRACTICE | successful follow-up | IMPROVING |
| IMPROVING | repeated successful evidence | MASTERED |
| IMPROVING | repeated difficulty evidence | NEEDS_PRACTICE |

The transition table should be revised after pilot data and expert review.

### 4.6 RAG personalization layer

Cognition is intended to operate around an existing RAG tutoring pipeline:

**Student query → retrieval → reranking → learner context injection → LLM response**

The learner context can include the current FSM state, relevant recent interaction evidence, and selected temporal features. The system should avoid exposing unnecessary raw conversation history to the generation model.

---

## 5. Research Questions and Hypotheses

### RQ1
Can conversational interaction data be classified into a useful set of learner signals with acceptable agreement against human-annotated labels?

### RQ2
Do inter-arrival times of concept-related interactions exhibit sufficient empirical fit to an exponential distribution to justify using an exponential rate feature in V1?

### RQ3
Does adding temporal interaction features improve learner-signal classification compared with conversational/semantic signals alone?

### RQ4
Does an FSM using combined conversational and temporal signals produce more consistent and useful learner-state representations than an FSM using conversational signals alone?

### RQ5
Does learner-aware context improve the quality of personalized tutoring responses compared with a conventional RAG baseline?

### Hypotheses

**H1:** Conversational and behavioral signals can be extracted from tutoring interactions with measurable agreement against human annotations.

**H2:** At least some concept-specific interaction sequences will show an adequate fit to an exponential inter-arrival model; however, the hypothesis may be rejected for some or all sequences.

**H3:** Temporal features provide incremental predictive value beyond semantic features for selected learner-signal categories.

**H4:** Combined temporal and conversational signals improve learner-state transition consistency relative to conversational signals alone.

**H5:** Responses generated with validated learner context will receive higher personalization/relevance ratings or demonstrate better downstream learning performance than responses from the baseline system.

---

## 6. Experimental Methodology

### 6.1 Experimental stages

The V1 study is divided into five stages.

#### Stage A: Dataset construction

Create or collect timestamped tutoring interaction traces around a controlled set of educational topics. If real student data are unavailable, begin with synthetic traces for engineering validation and clearly label them as synthetic. Synthetic data must not be presented as evidence of real learner behavior.

Each record should contain:

```text
learner_id
session_id
timestamp
topic_id
message
interaction_type
outcome (if available)
```

#### Stage B: Human annotation

A sample of interactions should be independently labeled for the five initial learner signals. Multiple annotators should be used where feasible. Agreement should be measured before using the labels as evaluation targets.

#### Stage C: Temporal model testing

For each topic/session sequence:

1. sort related interactions by timestamp;
2. calculate inter-arrival times;
3. estimate the exponential rate parameter;
4. compare the empirical distribution with the fitted exponential distribution;
5. use goodness-of-fit diagnostics;
6. compare with alternative distributions when the exponential model is inadequate.

Potential diagnostics include the Kolmogorov-Smirnov statistic, Q-Q plots, empirical survival curves, and information criteria when comparing fitted parametric alternatives. The exact statistical test should be selected according to sample size and the dependence structure of the collected data.

#### Stage D: Learner-state evaluation

Run two FSM variants:

- **FSM-S:** semantic/behavioral signals only.
- **FSM-ST:** semantic/behavioral signals plus validated temporal features.

Compare transition stability, agreement with annotated states where available, and usefulness to downstream tutoring.

#### Stage E: RAG evaluation

Compare three systems:

**Baseline A — RAG:**

```text
Question → Retrieval → Reranking → LLM
```

**System B — Learner-signal RAG:**

```text
Question → Signals → Retrieval/Reranking + learner context → LLM
```

**System C — Cognition V1:**

```text
Question → Signals + temporal features → FSM → Retrieval/Reranking + learner context → LLM
```

The comparison isolates the contribution of temporal features and FSM-based context.

---

## 7. Evaluation Metrics

### 7.1 Signal extraction

For each signal category:

- Precision
- Recall
- F1-score
- Macro-F1 across categories
- Confusion matrix

Where multiple annotators are used, inter-annotator agreement should also be reported.

### 7.2 Exponential-model fit

Report:

- estimated \(\lambda\),
- mean inter-arrival time,
- goodness-of-fit statistics,
- visual distribution diagnostics,
- comparison with alternative distributions where appropriate.

The paper should not interpret a statistically adequate exponential fit as proof of a learning mechanism. It only supports using the distribution as a compact temporal representation for the observed interaction process.

### 7.3 FSM quality

Evaluate:

- transition consistency,
- state persistence/stability,
- agreement with human judgments where available,
- number of unnecessary state transitions,
- usefulness for selecting the next tutoring strategy.

### 7.4 Response quality

Use blinded human ratings or a validated evaluation protocol for:

- relevance,
- groundedness,
- personalization,
- clarity,
- instructional usefulness.

Automated LLM-as-judge evaluation may be used as a supplementary measure but should not be the sole evidence for educational effectiveness.

### 7.5 Learning outcome

Where feasible, use a pre/post or repeated follow-up assessment. Candidate measures include:

- correctness on related follow-up questions,
- reduction in repeated misconceptions,
- transfer to a new but related problem,
- delayed retention where study duration permits.

---

## 8. Expected Results and Interpretation Plan

Because this manuscript describes a V1 study that has not yet been executed, no numerical results are claimed.

The expected outcome is not necessarily that the exponential model will fit all learner interaction sequences. Three outcomes are scientifically meaningful:

1. **Adequate fit:** temporal interaction data support an exponential feature for some sequences.
2. **Partial fit:** the exponential model is useful only for certain interaction classes, topics, or session conditions.
3. **Poor fit:** the exponential assumption is inadequate, motivating alternatives such as Weibull, Gamma, or non-parametric temporal representations.

Similarly, the FSM may provide useful interpretability without being the optimal predictive model. If a more complex model performs better, the FSM can remain as an explanation/monitoring layer while another model provides prediction.

The key empirical test is therefore whether temporal features provide **incremental value** when combined with conversational signals.

---

## 9. Ablation Study

Ablation is essential to determine which component contributes value.

| Variant | Semantic | Temporal | FSM | Purpose |
|---|---:|---:|---:|---|
| A | No | No | No | Conventional RAG baseline |
| B | Yes | No | No | Effect of conversational learner signals |
| C | Yes | Yes | No | Effect of temporal features |
| D | Yes | No | Yes | Effect of FSM context |
| E | Yes | Yes | Yes | Full Cognition V1 |

This structure prevents the paper from attributing improvements to the exponential model when they may actually come from semantic signal extraction or FSM context.

---

## 10. Implementation Plan

The initial prototype can be implemented using the existing EDURag/RAG foundation and the following logical modules:

```text
cognition/
├── events/
│   ├── schema.py
│   └── topic_sequence.py
├── signals/
│   ├── semantic.py
│   ├── behavioral.py
│   └── temporal.py
├── statistics/
│   ├── exponential.py
│   └── distribution_fit.py
├── state/
│   ├── fsm.py
│   └── transitions.py
├── learner_context/
│   └── builder.py
└── evaluation/
    ├── signal_metrics.py
    ├── state_metrics.py
    └── response_metrics.py
```

The first implementation should be intentionally small. The goal is to validate the pipeline before introducing complex machine-learning models.

### Suggested V1 sequence

1. Define the event schema.
2. Build a small labeled interaction dataset.
3. Implement five signal categories.
4. Calculate concept-specific inter-arrival times.
5. Fit and evaluate the exponential model.
6. Build the FSM transition table.
7. Fuse temporal and semantic signals.
8. Inject the resulting learner context into the RAG pipeline.
9. Run the ablation experiment.
10. Record results and revise the research claims.

---

## 11. Ethical and Privacy Considerations

Learner modeling involves potentially sensitive educational information. The system should therefore:

- use pseudonymous learner identifiers;
- collect only data required for the experiment;
- avoid storing unnecessary raw conversations;
- provide clear consent procedures for real-student studies;
- separate experimental learner analytics from grading decisions;
- avoid claiming psychological or clinical diagnoses from interaction patterns;
- allow teachers to inspect or challenge system-generated learner signals;
- avoid using automated learner states as high-stakes decisions without human oversight.

In particular, a temporal feature such as a short inter-arrival time should never be treated as definitive evidence of confusion, motivation, ability, or disengagement.

---

## 12. Limitations

Several limitations should be expected.

First, interaction timing is affected by factors outside learning, including interruptions, device availability, multitasking, and session design. Second, the exponential distribution has a strong memoryless assumption and may not represent all human interaction processes. Third, an FSM simplifies complex and potentially continuous learning dynamics into discrete states. Fourth, semantic signal extraction can introduce classification errors. Fifth, synthetic or small datasets may not generalize to real classrooms. Finally, personalization quality does not automatically imply improved learning outcomes; controlled educational evaluation is required.

These limitations are not reasons to reject the architecture. They define the boundaries that the V1 experiment must test.

---

## 13. Discussion

The central design principle of Cognition is that a tutoring system should treat the learner's interaction history as evidence rather than merely as a sequence of independent prompts. Existing work supports the broader importance of student modeling and the analysis of student-AI interaction [3]–[7]. Cognition's proposed contribution is narrower: introduce temporal interaction features into a transparent learner-signal pipeline and use those features alongside conversational evidence in an FSM-based representation.

The exponential model is especially useful as a research starting point because it converts a sequence of timestamps into a compact parameter, \(\lambda\), that can be compared across interaction sequences. However, its value depends entirely on empirical validation. If the data show non-exponential behavior, the research can pivot to a more appropriate distribution without changing the broader architecture.

The FSM also provides an important interpretability layer. A system that reports “current learner context: clarification needed; repeated concept: recursion; recent interaction rate: high” is easier for a teacher or researcher to inspect than an opaque embedding representing the same learner history. The FSM should therefore be viewed as a controllable state abstraction, not a complete cognitive model.

The broader goal is a human-in-the-loop tutoring system. Cognition should not replace teacher judgment. Instead, it can potentially transform large volumes of interaction data into structured signals that help teachers understand where students repeatedly struggle and how learners interact with educational content.

---

## 14. Conclusion

This paper proposed a V1 architecture for Cognition that combines conversational learner-signal extraction, temporal interaction modeling, and finite-state learner representation around an existing RAG tutoring system. The proposed exponential component models inter-arrival times between related interactions as an initial statistical hypothesis, producing temporal features rather than direct interpretations of learner psychology. These features are combined with semantic and behavioral signals and passed to an interpretable FSM that represents an evolving learner context.

The proposed study is designed to answer an experimentally testable question: whether temporal interaction information adds useful signal beyond conversational content alone. The research deliberately includes ablation studies and distribution-fit testing so that the exponential assumption can be accepted, restricted, or rejected based on evidence.

The immediate next step is not to claim that Cognition has solved personalized learning. It is to build the V1 pipeline, collect or construct appropriately labeled interaction data, evaluate the statistical assumptions, and compare the learner-aware system against a conventional RAG baseline. This evidence-driven approach can turn Cognition from a conceptual learner-intelligence layer into a measurable research prototype.

---

## References

[1] M. A. Kuhail, N. Alturki, S. Alramlawi, and K. Alhejori, “Interacting with educational chatbots: A systematic review,” *Education and Information Technologies*, vol. 28, pp. 973–1018, 2023, doi: 10.1007/s10639-022-11177-3.

[2] “A systematic review of conversational AI tools in ELT: Publication trends, tools, research methods, learning outcomes, and antecedents,” *Computers and Education: Artificial Intelligence*, vol. 7, 2024, Art. no. 100291, doi: 10.1016/j.caeai.2024.100291.

[3] Z. Hao, J. Cao, R. Li, J. Yu, Z. Liu, and Y. Zhang, “Mapping student-AI interaction dynamics in multi-agent learning environments: Supporting personalized learning and reducing performance gaps,” *Computers & Education*, 2025, Art. no. 105472, doi: 10.1016/j.compedu.2025.105472.

[4] C.-K. Looi and F. Jia, “Personalization capabilities of current technology chatbots in a learning environment: An analysis of student-tutor bot interactions,” *Education and Information Technologies*, vol. 30, pp. 14165–14195, 2025, doi: 10.1007/s10639-025-13369-z.

[5] M. Park, S. Kim, S. Lee, S. Kwon, and K. Kim, “Empowering Personalized Learning through a Conversation-based Tutoring System with Student Modeling,” arXiv:2403.14071, 2024.

[6] R. Nkambou, J. Brisson, A. Tato, and S. Robert, “Learning Logical Reasoning Using an Intelligent Tutoring System: A Hybrid Approach to Student Modeling,” *Proceedings of the AAAI Conference on Artificial Intelligence*, vol. 37, no. 13, pp. 15930–15937, 2023/2024 publication record, doi: 10.1609/aaai.v37i13.26891.

[7] “Modeling students' preferences and knowledge for improving educational achievements,” *Frontiers in Computer Science*, 2024, doi: 10.3389/fcomp.2024.1359770.

[8] “How educational chatbots support self-regulated learning? A systematic review of the literature,” *Education and Information Technologies*, 2024, doi: 10.1007/s10639-024-12881-y.

[9] H.-A. Kang, A. Sales, and T. A. Whittaker, “Flow with an intelligent tutor: A latent variable modeling approach to tracking flow during artificial tutoring,” *Behavior Research Methods*, vol. 56, pp. 615–638, 2024, doi: 10.3758/s13428-022-02041-w.

[10] S. Basu, J. Brown, C. Lum, J. Park, and A. K. Goel, “Bidirectional Feedback-Based Personalization of Learning using Multi-tier AI: A Real-World Assessment of its Efficacy in Classrooms,” *Proceedings of the AAAI Symposium Series*, vol. 5, no. 1, pp. 50–51, 2025, doi: 10.1609/aaaiss.v5i1.35553.

---

## Appendix A — Initial Signal Annotation Guide

Annotators should label an interaction only from observable evidence. They should not infer intelligence, personality, motivation, or mental state.

### CONFUSION
Label when the learner explicitly reports difficulty or demonstrates a strong direct request for clarification.

### CLARIFICATION
Label when the learner requests a re-explanation, simplification, or clarification of an earlier explanation.

### EXAMPLE_SEEKING
Label when the learner explicitly requests an example, analogy, worked problem, or concrete demonstration.

### CONCEPT_REVISIT
Label when the learner returns to a concept already discussed in the current analysis window.

### SUCCESS
Label when an observable follow-up response demonstrates successful understanding according to a predefined task criterion.

Multiple labels may be valid for a single interaction. For example, “I still don't understand; can you show me an example?” can receive both CONFUSION and EXAMPLE_SEEKING.

---

## Appendix B — Minimal Experimental Record

```json
{
  "learner_id": "L001",
  "session_id": "S001",
  "timestamp": "2026-08-29T10:02:10",
  "topic_id": "recursion",
  "message": "Can you explain recursion?",
  "signals": ["CLARIFICATION"],
  "outcome": null
}
```

A later related interaction can be linked using `topic_id`, session context, and timestamp. The research implementation must define a reproducible topic-linking rule before temporal statistics are calculated.

---

## Appendix C — Research Claim Discipline

The following claims are **allowed before experimentation**:

- “We propose..."
- “We investigate..."
- “We hypothesize..."
- “We design..."
- “We evaluate..."

The following claims should **not** be made until supported by measured data:

- “The exponential distribution accurately models learners.”
- “Shorter interaction intervals indicate confusion.”
- “The FSM correctly identifies learner states.”
- “Cognition improves learning outcomes.”
- “Cognition outperforms ChatGPT/Claude.”

The V1 paper should be updated with measured evidence before being submitted to a peer-reviewed venue.
