from __future__ import annotations

from dataclasses import asdict
from math import log

import numpy as np
from scipy import stats


def fit_distribution_comparison(intervals: list[float]) -> dict:
    """Compare exponential, gamma and Weibull fits using AIC/BIC.

    This is exploratory model comparison. It does not establish causality or
    imply that any fitted distribution represents a psychological state.
    """
    x = np.asarray(intervals, dtype=float)
    if len(x) < 3 or np.any(x <= 0):
        raise ValueError("Need at least 3 positive intervals")

    candidates = {
        "exponential": (stats.expon, (0, np.mean(x))),
        "gamma": (stats.gamma, stats.gamma.fit(x, floc=0)),
        "weibull": (stats.weibull_min, stats.weibull_min.fit(x, floc=0)),
    }
    rows = []
    for name, (dist, params) in candidates.items():
        loglik = float(np.sum(dist.logpdf(x, *params)))
        k = len(params)
        rows.append({
            "distribution": name,
            "log_likelihood": loglik,
            "aic": 2 * k - 2 * loglik,
            "bic": k * log(len(x)) - 2 * loglik,
            "ks_statistic": float(stats.kstest(x, dist.cdf, args=params).statistic),
        })
    return {"n": len(x), "models": rows}
