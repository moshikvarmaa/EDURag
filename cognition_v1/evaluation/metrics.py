from __future__ import annotations

from collections import Counter


def classification_metrics(y_true: list[str], y_pred: list[str]) -> dict:
    if len(y_true) != len(y_pred) or not y_true:
        raise ValueError("y_true and y_pred must be non-empty and equal length")

    labels = sorted(set(y_true) | set(y_pred))
    per_label = {}
    for label in labels:
        tp = sum(a == label and b == label for a, b in zip(y_true, y_pred))
        fp = sum(a != label and b == label for a, b in zip(y_true, y_pred))
        fn = sum(a == label and b != label for a, b in zip(y_true, y_pred))
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        per_label[label] = {"precision": precision, "recall": recall, "f1": f1, "support": tp + fn}

    accuracy = sum(a == b for a, b in zip(y_true, y_pred)) / len(y_true)
    macro_f1 = sum(v["f1"] for v in per_label.values()) / len(per_label)
    return {"accuracy": accuracy, "macro_f1": macro_f1, "per_label": per_label}


def confusion_counts(y_true: list[str], y_pred: list[str]) -> dict[str, int]:
    return dict(Counter(f"true={a}|pred={b}" for a, b in zip(y_true, y_pred)))
