from __future__ import annotations

from dataclasses import dataclass
from math import exp
from statistics import mean


@dataclass(frozen=True)
class ExponentialEstimate:
    sample_count: int
    mean_interval_seconds: float
    rate_lambda: float

    def density(self, t_seconds: float) -> float:
        """Evaluate the fitted exponential density at t >= 0."""
        if t_seconds < 0:
            raise ValueError("t_seconds must be non-negative")
        if self.rate_lambda <= 0:
            return 0.0
        return self.rate_lambda * exp(-self.rate_lambda * t_seconds)


def fit_exponential(inter_arrival_seconds: list[float]) -> ExponentialEstimate:
    """Fit an exponential distribution by maximum likelihood.

    For an exponential distribution, lambda_hat = 1 / sample_mean.
    This function estimates a temporal feature only; it does not infer
    confusion, mastery, motivation, or any other psychological state.
    """
    if not inter_arrival_seconds:
        raise ValueError("At least one inter-arrival time is required")
    if any(t <= 0 for t in inter_arrival_seconds):
        raise ValueError("Inter-arrival times must be positive")

    avg = mean(inter_arrival_seconds)
    return ExponentialEstimate(
        sample_count=len(inter_arrival_seconds),
        mean_interval_seconds=avg,
        rate_lambda=1.0 / avg,
    )
