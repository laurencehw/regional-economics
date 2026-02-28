"""Shared PPML estimator for Lab 7 gravity and STRI scripts.

Poisson Pseudo-Maximum Likelihood estimation via IRLS, following
Santos Silva and Tenreyro (2006).  Produces robust (sandwich)
standard errors and deviance-based pseudo-R².
"""

from __future__ import annotations

from typing import Dict, List

import numpy as np


def ppml_estimate(
    y: np.ndarray,
    x: np.ndarray,
    x_names: List[str],
    max_iter: int = 200,
    tol: float = 1e-8,
) -> Dict[str, object]:
    """Poisson Pseudo-Maximum Likelihood estimation via IRLS.

    Estimates: E[y | x] = exp(x @ beta)

    Parameters
    ----------
    y : array of shape (n,)
        Non-negative dependent variable (e.g. trade flows).
    x : array of shape (n, k)
        Regressor matrix (should include an intercept column).
    x_names : list of str
        Names for each column of x.
    max_iter : int
        Maximum IRLS iterations.
    tol : float
        Convergence tolerance on max absolute change in beta.

    Returns
    -------
    dict with keys: betas, se, beta_names, n_obs, pseudo_r2,
    iterations, converged.
    """
    n, k = x.shape
    beta = np.zeros(k)
    converged = False

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

    # Robust (sandwich) standard errors — O(nk²) without forming NxN diag
    residuals = y - mu
    bread = np.linalg.pinv(x.T @ (x * mu[:, None]))
    meat = x.T @ (x * (residuals ** 2)[:, None])
    vcov = bread @ meat @ bread
    se = np.sqrt(np.maximum(np.diag(vcov), 0))

    return {
        "betas": [float(b) for b in beta],
        "se": [float(s) for s in se],
        "beta_names": list(x_names),
        "n_obs": int(n),
        "pseudo_r2": float(pseudo_r2),
        "iterations": int(iteration + 1),
        "converged": converged,
    }
