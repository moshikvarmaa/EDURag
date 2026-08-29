# Cognition V1 Evaluation

Run the evaluation from the `cognition_v1` directory after installing `requirements.txt`:

```bash
pip install -r requirements.txt
python evaluation/experiment.py
```

The runner writes `evaluation/results.json`.

## Interpretation

The sample dataset in this repository is synthetic and exists only for pipeline validation. Its statistics must **not** be reported as real learner evidence. Replace it with an appropriately collected and annotated dataset before making research claims.

The exponential KS diagnostic is exploratory. A p-value alone does not establish that learner interaction data follow an exponential process; model assumptions, sample size, censoring, dependence, and alternative distributions must be considered.

The next research implementation should add:

- human-annotated signal labels;
- precision/recall/F1 evaluation;
- train/test separation where learned models are introduced;
- Weibull/Gamma comparisons;
- FSM state agreement and transition-stability metrics;
- RAG ablations;
- response-quality and learning-outcome evaluation.
