"""Shared PPML estimator for Lab 7 gravity and STRI scripts.

Poisson Pseudo-Maximum Likelihood estimation via IRLS, following
Santos Silva and Tenreyro (2006). Supports HC1 robust and clustered
sandwich standard errors, plus zero-share / convergence diagnostics.
"""

from __future__ import annotations

from typing import Dict, List, Optional

import numpy as np


def build_fixed_effects(
    labels: np.ndarray,
    prefix: str,
    drop_first: bool = True,
) -> tuple[np.ndarray, List[str]]:
    """Return a dummy matrix and names for categorical labels."""
    categories = np.unique(labels)
    if drop_first and len(categories) > 0:
        categories = categories[1:]
    if len(categories) == 0:
        return np.zeros((len(labels), 0)), []
    dummies = np.column_stack([(labels == cat).astype(float) for cat in categories])
    names = [f"{prefix}_{cat}" for cat in categories]
    return dummies, names


def ppml_estimate(
    y: np.ndarray,
    x: np.ndarray,
    x_names: List[str],
    max_iter: int = 200,
    tol: float = 1e-8,
    cluster: Optional[np.ndarray] = None,
) -> Dict[str, object]:
    """Poisson Pseudo-Maximum Likelihood estimation via IRLS.

    Estimates: E[y | x] = exp(x @ beta)

    Parameters
    ----------
    y : array of shape (n,)
        Non-negative dependent variable (e.g. trade flows).
    x : array of shape (n, k)
        Regressor matrix (should include an intercept column unless FE absorb it).
    x_names : list of str
        Names for each column of x.
    max_iter : int
        Maximum IRLS iterations.
    tol : float
        Convergence tolerance on max absolute change in beta.
    cluster : optional array of shape (n,)
        Cluster identifiers for clustered sandwich SEs. If None, HC1 robust SEs.

    Returns
    -------
    dict with keys: betas, se, beta_names, n_obs, n_zeros, zero_share,
    pseudo_r2, iterations, converged, se_type, n_clusters.
    """
    y = np.asarray(y, dtype=float)
    x = np.asarray(x, dtype=float)
    n, k = x.shape
    if np.any(y < 0):
        raise ValueError("PPML requires non-negative outcomes.")
    n_zeros = int(np.sum(y == 0))
    beta = np.zeros(k)
    converged = False
    iteration = -1

    for iteration in range(max_iter):
        eta = np.clip(x @ beta, -20, 20)
        mu = np.exp(eta)

        # IRLS weight and working variable
        w = mu
        z = eta + (y - mu) / np.where(mu > 1e-10, mu, 1e-10)

        # Weighted least squares step
        w_sqrt = np.sqrt(w)
        xw = x * w_sqrt[:, None]
        zw = z * w_sqrt

        try:
            beta_new = np.linalg.lstsq(xw, zw, rcond=None)[0]
        except np.linalg.LinAlgError:
            break

        if np.max(np.abs(beta_new - beta)) < tol:
            beta = beta_new
            converged = True
            break
        beta = beta_new

    # Final fitted values
    eta = np.clip(x @ beta, -20, 20)
    mu = np.exp(eta)

    # Deviance-based pseudo-R²
    y_safe = np.where(y > 0, y, 1e-10)
    deviance = 2 * np.sum(
        np.where(y > 0, y * np.log(y_safe / np.where(mu > 1e-10, mu, 1e-10)), 0)
        - (y - mu)
    )
    null_mu = np.mean(y)
    null_deviance = 2 * np.sum(
        np.where(y > 0, y * np.log(y_safe / null_mu), 0) - (y - null_mu)
    )
    pseudo_r2 = 1.0 - (deviance / null_deviance) if null_deviance > 0 else 0.0

    # Sandwich variance
    residuals = y - mu
    bread = np.linalg.pinv(x.T @ (x * mu[:, None]))
    n_clusters = None
    if cluster is None:
        meat = x.T @ (x * (residuals ** 2)[:, None])
        # HC1 finite-sample correction
        scale = n / max(n - k, 1)
        vcov = scale * (bread @ meat @ bread)
        se_type = "HC1"
    else:
        cluster = np.asarray(cluster)
        unique = np.unique(cluster)
        n_clusters = int(len(unique))
        meat = np.zeros((k, k))
        for c in unique:
            idx = cluster == c
            score_c = x[idx].T @ residuals[idx]
            meat += np.outer(score_c, score_c)
        # Cameron–Gelbach–Miller cluster adjustment
        scale = (n_clusters / max(n_clusters - 1, 1)) * ((n - 1) / max(n - k, 1))
        vcov = scale * (bread @ meat @ bread)
        se_type = "cluster"

    se = np.sqrt(np.maximum(np.diag(vcov), 0))

    return {
        "betas": [float(b) for b in beta],
        "se": [float(s) for s in se],
        "beta_names": list(x_names),
        "n_obs": int(n),
        "n_zeros": n_zeros,
        "zero_share": float(n_zeros / n) if n else 0.0,
        "pseudo_r2": float(pseudo_r2),
        "iterations": int(iteration + 1),
        "converged": converged,
        "se_type": se_type,
        "n_clusters": n_clusters,
    }
