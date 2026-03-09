"""Unit tests for core numerical estimation functions.

Tests verify correctness against known analytical solutions,
edge cases, and numerical stability -- complementing the
existing subprocess-based smoke tests.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

# ---------------------------------------------------------------------------
# Path manipulation so we can import lab modules directly.
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(REPO_ROOT / "labs" / "lab3_south_asia" / "code"))
sys.path.insert(0, str(REPO_ROOT / "labs" / "lab7_services" / "code"))
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT / "labs" / "lab2_asia" / "code"))
sys.path.insert(0, str(REPO_ROOT / "labs" / "lab6_africa" / "code"))
sys.path.insert(0, str(REPO_ROOT / "labs" / "lab1_americas" / "code"))
sys.path.insert(0, str(REPO_ROOT / "labs" / "lab4_europe" / "code"))

from lab3_concentration_scaffold import (
    compute_gini,
    compute_herfindahl,
    compute_location_quotients,
)
from ppml_estimator import ppml_estimate
from run_lab5_scm_baseline import solve_scm_weights
from lab2_asia_convergence_scaffold import estimate_convergence
from lab6_africa_moran_scaffold import morans_i, permutation_p_value
from lab1_americas_sar_scaffold import estimate_sar_manual
from lab4_europe_rdd_scaffold import (
    estimate_rdd,
    triangular_kernel,
    uniform_kernel,
    select_bandwidth,
)


# ===================================================================
# 1. TestConcentrationIndices
# ===================================================================


class TestConcentrationIndices:
    """Tests for Gini, Herfindahl, and Location Quotient functions."""

    def test_gini_uniform(self):
        """Equal values across all regions should yield Gini = 0."""
        values = np.array([10.0, 10.0, 10.0, 10.0, 10.0])
        assert compute_gini(values) == pytest.approx(0.0, abs=1e-10)

    def test_gini_maximum(self):
        """One region has everything, rest have zero -> Gini approx (n-1)/n."""
        n = 5
        values = np.array([0.0, 0.0, 0.0, 0.0, 100.0])
        expected = (n - 1) / n  # 0.8
        assert compute_gini(values) == pytest.approx(expected, abs=1e-10)

    def test_gini_known_value(self):
        """Hand-computed Gini for [1, 2, 3, 4].

        Sorted: [1, 2, 3, 4], n=4, sum=10.
        numerator = 2*(1*1 + 2*2 + 3*3 + 4*4) - (4+1)*10
                   = 2*(1+4+9+16) - 50 = 60 - 50 = 10
        gini = 10 / (4 * 10) = 0.25
        """
        values = np.array([1.0, 2.0, 3.0, 4.0])
        assert compute_gini(values) == pytest.approx(0.25, abs=1e-10)

    def test_herfindahl_uniform(self):
        """Equal shares across n firms -> HHI = 1/n."""
        n = 5
        values = np.array([20.0] * n)
        assert compute_herfindahl(values) == pytest.approx(1.0 / n, abs=1e-10)

    def test_herfindahl_monopoly(self):
        """Single firm with all output -> HHI = 1.0."""
        values = np.array([100.0])
        assert compute_herfindahl(values) == pytest.approx(1.0, abs=1e-10)

    def test_herfindahl_known(self):
        """Shares [0.5, 0.3, 0.2] -> HHI = 0.25 + 0.09 + 0.04 = 0.38."""
        values = np.array([0.5, 0.3, 0.2])
        assert compute_herfindahl(values) == pytest.approx(0.38, abs=1e-10)

    def test_location_quotient_average(self):
        """A region at the national average IT share should have LQ = 1.0."""
        # 4 regions, each with same IT/GDP ratio
        it_va = np.array([10.0, 20.0, 30.0, 40.0])
        total_gdp = np.array([100.0, 200.0, 300.0, 400.0])
        # Each region has IT share = 0.1, national average = 100/1000 = 0.1
        lq = compute_location_quotients(it_va, total_gdp)
        np.testing.assert_allclose(lq, 1.0, atol=1e-10)

    def test_location_quotient_specialized(self):
        """A region with double the national IT share should have LQ = 2.0."""
        # 2-region example with non-integer LQs.
        # Region 0: IT/GDP = 20/100 = 0.20
        # Region 1: IT/GDP = 10/100 = 0.10
        # National: (20+10)/(100+100) = 30/200 = 0.15
        # LQ_0 = 0.20/0.15 = 4/3, LQ_1 = 0.10/0.15 = 2/3
        it_va = np.array([20.0, 10.0])
        total_gdp = np.array([100.0, 100.0])
        lq = compute_location_quotients(it_va, total_gdp)
        assert lq[0] == pytest.approx(4.0 / 3.0, abs=1e-10)
        assert lq[1] == pytest.approx(2.0 / 3.0, abs=1e-10)

        # Region with exactly double the national average.
        # With equal GDP and b=0: region 0 share = national * 2.
        it_va2 = np.array([50.0, 0.0])
        total_gdp2 = np.array([100.0, 100.0])
        lq2 = compute_location_quotients(it_va2, total_gdp2)
        assert lq2[0] == pytest.approx(2.0, abs=1e-10)
        assert lq2[1] == pytest.approx(0.0, abs=1e-10)


# ===================================================================
# 2. TestPPMLEstimator
# ===================================================================


class TestPPMLEstimator:
    """Tests for the Poisson Pseudo-Maximum Likelihood estimator."""

    @pytest.fixture()
    def well_conditioned_data(self):
        """Generate data from y ~ Poisson(exp(X @ beta)) with known beta."""
        rng = np.random.default_rng(42)
        n = 200
        true_beta = np.array([1.0, -0.5])
        x_raw = rng.normal(0, 1, size=(n, 1))
        x = np.column_stack([np.ones(n), x_raw])
        eta = x @ true_beta
        mu = np.exp(eta)
        y = rng.poisson(mu).astype(float)
        return y, x, true_beta

    def test_ppml_recovers_known_coefficients(self, well_conditioned_data):
        """PPML should recover known beta = [1.0, -0.5] within tolerance."""
        y, x, true_beta = well_conditioned_data
        result = ppml_estimate(y, x, x_names=["const", "x1"])
        betas = np.array(result["betas"])
        np.testing.assert_allclose(betas, true_beta, atol=0.3)

    def test_ppml_convergence_flag(self, well_conditioned_data):
        """Well-conditioned data should converge."""
        y, x, _ = well_conditioned_data
        result = ppml_estimate(y, x, x_names=["const", "x1"])
        assert result["converged"] is True

    def test_ppml_robust_se_positive(self, well_conditioned_data):
        """Robust standard errors must all be strictly positive."""
        y, x, _ = well_conditioned_data
        result = ppml_estimate(y, x, x_names=["const", "x1"])
        for se in result["se"]:
            assert se > 0.0

    def test_ppml_zero_y_handled(self):
        """y containing zeros should not crash -- Poisson allows zeros."""
        rng = np.random.default_rng(99)
        n = 100
        x = np.column_stack([np.ones(n), rng.normal(0, 0.5, size=n)])
        # Many zeros: low mean Poisson
        mu = np.exp(-0.5 + 0.3 * x[:, 1])
        y = rng.poisson(mu).astype(float)
        assert (y == 0).sum() > 0, "Sanity: test data should include zeros"
        result = ppml_estimate(y, x, x_names=["const", "x1"])
        assert "betas" in result
        assert result["n_obs"] == n

    def test_ppml_pseudo_r2_range(self, well_conditioned_data):
        """Pseudo R-squared should be in [0, 1] for reasonable data."""
        y, x, _ = well_conditioned_data
        result = ppml_estimate(y, x, x_names=["const", "x1"])
        assert 0.0 <= result["pseudo_r2"] <= 1.0


# ===================================================================
# 3. TestSCMSolver
# ===================================================================


class TestSCMSolver:
    """Tests for the Synthetic Control Method weight solver."""

    def test_scm_weights_sum_to_one(self):
        """Solved weights must sum to 1.0."""
        rng = np.random.default_rng(42)
        x1 = rng.normal(0, 1, size=20)
        x0 = rng.normal(0, 1, size=(20, 5))
        weights = solve_scm_weights(x1, x0)
        assert weights.sum() == pytest.approx(1.0, abs=1e-6)

    def test_scm_weights_nonnegative(self):
        """All solved weights must be >= 0."""
        rng = np.random.default_rng(42)
        x1 = rng.normal(0, 1, size=15)
        x0 = rng.normal(0, 1, size=(15, 4))
        weights = solve_scm_weights(x1, x0)
        assert np.all(weights >= -1e-10)

    def test_scm_perfect_donor(self):
        """If one donor perfectly matches the treated unit, it gets weight ~1."""
        rng = np.random.default_rng(42)
        x1 = rng.normal(5, 2, size=20)
        # Donor 0 is a perfect copy; others are noise
        x0 = np.column_stack([
            x1,
            rng.normal(0, 1, size=(20, 3)),
        ])
        weights = solve_scm_weights(x1, x0)
        assert weights[0] == pytest.approx(1.0, abs=0.05)

    def test_scm_equal_donors(self):
        """Identical donors should receive roughly equal weights."""
        rng = np.random.default_rng(42)
        base = rng.normal(0, 1, size=20)
        n_donors = 4
        # All donors identical to each other (but different from treated)
        x0 = np.column_stack([base] * n_donors)
        x1 = base + 0.01  # treated is very close
        weights = solve_scm_weights(x1, x0)
        expected = 1.0 / n_donors
        np.testing.assert_allclose(weights, expected, atol=0.15)

    def test_scm_reduces_pre_rmspe(self):
        """Synthetic counterfactual should fit pre-period better than simple average."""
        rng = np.random.default_rng(42)
        x1 = rng.normal(3, 1, size=20)
        x0 = rng.normal(0, 1, size=(20, 5))
        # Make one donor fairly close
        x0[:, 2] = x1 + rng.normal(0, 0.1, size=20)
        weights = solve_scm_weights(x1, x0)

        synth = x0 @ weights
        avg = x0.mean(axis=1)
        rmspe_synth = float(np.sqrt(np.mean((x1 - synth) ** 2)))
        rmspe_avg = float(np.sqrt(np.mean((x1 - avg) ** 2)))
        assert rmspe_synth < rmspe_avg


# ===================================================================
# 4. TestMoransI
# ===================================================================


class TestMoransI:
    """Tests for global Moran's I and its permutation-based p-value."""

    @staticmethod
    def _grid_weight_matrix(n: int) -> np.ndarray:
        """Build a row-standardized rook-contiguity matrix for a 1-D chain."""
        w = np.zeros((n, n))
        for i in range(n):
            if i > 0:
                w[i, i - 1] = 1.0
            if i < n - 1:
                w[i, i + 1] = 1.0
        row_sums = w.sum(axis=1, keepdims=True)
        out = np.zeros_like(w, dtype=float)
        np.divide(w, row_sums, out=out, where=row_sums > 0)
        return out

    def test_morans_i_positive_autocorrelation(self):
        """Spatially clustered data should produce I > E[I]."""
        n = 20
        w = self._grid_weight_matrix(n)
        # Clustered: low values on left, high on right
        y = np.concatenate([np.zeros(n // 2), np.ones(n // 2)])
        i_val, expected_i = morans_i(y, w)
        assert i_val > expected_i

    def test_morans_i_no_autocorrelation(self):
        """Random data should yield I close to E[I] = -1/(n-1)."""
        rng = np.random.default_rng(42)
        n = 50
        w = self._grid_weight_matrix(n)
        # Average over several draws to reduce variance
        i_values = []
        for _ in range(100):
            y = rng.normal(0, 1, size=n)
            i_val, _ = morans_i(y, w)
            i_values.append(i_val)
        mean_i = np.mean(i_values)
        expected_i = -1.0 / (n - 1)
        assert mean_i == pytest.approx(expected_i, abs=0.1)

    def test_morans_i_range(self):
        """I should be in [-1, 1] for row-standardized W."""
        rng = np.random.default_rng(42)
        n = 30
        w = self._grid_weight_matrix(n)
        for _ in range(50):
            y = rng.normal(0, 1, size=n)
            i_val, _ = morans_i(y, w)
            assert -1.0 - 0.01 <= i_val <= 1.0 + 0.01

    def test_permutation_pvalue_range(self):
        """Permutation p-value must be in [0, 1]."""
        rng = np.random.default_rng(42)
        n = 20
        w = self._grid_weight_matrix(n)
        y = rng.normal(0, 1, size=n)
        p, _ = permutation_p_value(y, w, permutations=99, seed=42)
        assert 0.0 <= p <= 1.0

    def test_permutation_pvalue_clustered(self):
        """Strongly clustered data should give a small p-value (< 0.05)."""
        n = 30
        w = self._grid_weight_matrix(n)
        y = np.concatenate([np.zeros(n // 2), np.ones(n // 2)])
        p, _ = permutation_p_value(y, w, permutations=499, seed=42)
        assert p < 0.05


# ===================================================================
# 5. TestConvergence
# ===================================================================


class TestConvergence:
    """Tests for beta-convergence OLS estimation."""

    def test_convergence_negative_beta(self):
        """Constructed converging data (beta < 0) should be detected."""
        rng = np.random.default_rng(42)
        n = 100
        true_beta = -0.15
        log_lag = rng.uniform(8, 14, size=n)
        growth = 2.0 + true_beta * log_lag + rng.normal(0, 0.3, size=n)
        result = estimate_convergence(growth, log_lag)
        assert result["beta"] < 0
        assert result["p_value"] < 0.05

    def test_convergence_half_life(self):
        """Verify half-life formula: half_life = ln(2) / |beta|."""
        rng = np.random.default_rng(42)
        n = 200
        true_beta = -0.10
        log_lag = rng.uniform(8, 14, size=n)
        growth = 2.0 + true_beta * log_lag + rng.normal(0, 0.2, size=n)
        result = estimate_convergence(growth, log_lag)
        # Check that the reported half-life is consistent with the formula
        expected_hl = np.log(2) / abs(result["beta"])
        assert result["half_life_years"] == pytest.approx(expected_hl, rel=1e-8)

    def test_convergence_robust_se(self):
        """Standard error must be positive and smaller than |beta| for strong signal."""
        rng = np.random.default_rng(42)
        n = 200
        true_beta = -0.20
        log_lag = rng.uniform(8, 14, size=n)
        growth = 2.0 + true_beta * log_lag + rng.normal(0, 0.2, size=n)
        result = estimate_convergence(growth, log_lag)
        assert result["se_beta"] > 0
        assert result["se_beta"] < abs(result["beta"])

    def test_no_convergence(self):
        """Random data with no relationship -> beta near 0, not significant."""
        rng = np.random.default_rng(42)
        n = 50
        log_lag = rng.uniform(8, 14, size=n)
        growth = rng.normal(0, 1, size=n)  # no relationship to log_lag
        result = estimate_convergence(growth, log_lag)
        # beta should be close to zero and p-value large
        assert abs(result["beta"]) < 0.5
        assert result["p_value"] > 0.05


# ===================================================================
# 6. TestSAR
# ===================================================================


class TestSAR:
    """Tests for the manual SAR (spatial autoregressive) ML estimator."""

    @staticmethod
    def _row_standardize(w: np.ndarray) -> np.ndarray:
        row_sums = w.sum(axis=1, keepdims=True)
        with np.errstate(divide="ignore", invalid="ignore"):
            out = np.zeros_like(w, dtype=float)
            np.divide(w, row_sums, out=out, where=row_sums > 0)
        return out

    @staticmethod
    def _ring_w(n: int) -> np.ndarray:
        """Build a ring adjacency (each node connected to its two neighbors)."""
        w = np.zeros((n, n))
        for i in range(n):
            w[i, (i - 1) % n] = 1.0
            w[i, (i + 1) % n] = 1.0
        row_sums = w.sum(axis=1, keepdims=True)
        return w / row_sums

    def test_sar_rho_in_bounds(self):
        """Estimated rho must lie within the eigenvalue bounds of W."""
        rng = np.random.default_rng(42)
        n = 30
        w = self._ring_w(n)

        x = rng.normal(0, 1, size=(n, 2))
        y = 1.0 + x @ np.array([0.5, -0.3]) + rng.normal(0, 0.5, size=n)

        result = estimate_sar_manual(y, x, w, x_names=["x1", "x2"])
        eigvals = np.real(np.linalg.eigvals(w))
        lb = 1.0 / min(eigvals)
        ub = 1.0 / max(eigvals)
        low, high = min(lb, ub), max(lb, ub)
        assert low - 0.01 <= result["rho"] <= high + 0.01

    def test_sar_recovers_ols_when_rho_zero(self):
        """When the true rho is 0, SAR betas should be close to OLS betas."""
        rng = np.random.default_rng(42)
        n = 50
        w = self._ring_w(n)

        true_beta = np.array([2.0, 0.8, -0.4])
        x = rng.normal(0, 1, size=(n, 2))
        x_const = np.column_stack([np.ones(n), x])
        y = x_const @ true_beta + rng.normal(0, 0.3, size=n)

        ols_beta = np.linalg.lstsq(x_const, y, rcond=None)[0]
        result = estimate_sar_manual(y, x, w, x_names=["x1", "x2"])
        sar_betas = np.array(result["betas"])

        np.testing.assert_allclose(sar_betas, ols_beta, atol=0.3)
        assert abs(result["rho"]) < 0.3

    def test_sar_positive_sigma(self):
        """Estimated sigma-squared must be strictly positive."""
        rng = np.random.default_rng(42)
        n = 30
        w = self._ring_w(n)

        x = rng.normal(0, 1, size=(n, 2))
        y = 1.0 + x @ np.array([0.5, -0.3]) + rng.normal(0, 0.5, size=n)

        result = estimate_sar_manual(y, x, w, x_names=["x1", "x2"])
        assert result["sigma2"] > 0.0


# ===================================================================
# 7. TestRDD
# ===================================================================


class TestRDD:
    """Tests for Lab 4's RDD estimator and kernel functions."""

    def test_triangular_kernel_at_center(self):
        """Weight at the cutoff (x=0) should be 1.0."""
        x = np.array([0.0])
        w = triangular_kernel(x, bandwidth=5.0)
        assert w[0] == pytest.approx(1.0, abs=1e-10)

    def test_triangular_kernel_at_boundary(self):
        """Weight at |x|=bandwidth should be 0.0."""
        x = np.array([5.0, -5.0])
        w = triangular_kernel(x, bandwidth=5.0)
        np.testing.assert_allclose(w, 0.0, atol=1e-10)

    def test_triangular_kernel_outside_bandwidth(self):
        """Observations outside the bandwidth should get weight 0."""
        x = np.array([6.0, -7.0, 100.0])
        w = triangular_kernel(x, bandwidth=5.0)
        np.testing.assert_allclose(w, 0.0, atol=1e-10)

    def test_triangular_kernel_symmetry(self):
        """Kernel should be symmetric: K(x) = K(-x)."""
        x = np.array([1.0, 2.0, 3.0])
        bw = 5.0
        w_pos = triangular_kernel(x, bw)
        w_neg = triangular_kernel(-x, bw)
        np.testing.assert_allclose(w_pos, w_neg, atol=1e-10)

    def test_uniform_kernel_inside(self):
        """All observations inside bandwidth should get weight 1.0."""
        x = np.array([0.0, 1.0, -2.0, 4.9])
        w = uniform_kernel(x, bandwidth=5.0)
        np.testing.assert_allclose(w, 1.0, atol=1e-10)

    def test_uniform_kernel_outside(self):
        """Observations outside bandwidth should get weight 0.0."""
        x = np.array([5.1, -6.0, 100.0])
        w = uniform_kernel(x, bandwidth=5.0)
        np.testing.assert_allclose(w, 0.0, atol=1e-10)

    def test_select_bandwidth_positive(self):
        """Selected bandwidth should be positive."""
        forcing = np.linspace(-10, 10, 100)
        bw = select_bandwidth(forcing, frac=0.5)
        assert bw > 0
        assert bw == pytest.approx(10.0, abs=1e-10)  # 0.5 * 20 = 10

    def test_rdd_recovers_known_tau(self):
        """RDD should recover a known treatment effect from synthetic data.

        DGP: y = 3.0 + 2.0*D + 0.5*X + noise, so true tau = 2.0.
        """
        rng = np.random.default_rng(42)
        n = 200
        true_tau = 2.0
        forcing = np.concatenate([
            rng.uniform(-10, -0.1, size=n // 2),
            rng.uniform(0.1, 10, size=n // 2),
        ])
        treatment = (forcing < 0).astype(float)
        noise = rng.normal(0, 0.3, size=n)
        outcome = 3.0 + true_tau * treatment + 0.5 * forcing + noise

        bw = select_bandwidth(forcing, frac=0.5)
        weights = triangular_kernel(forcing, bw)
        result = estimate_rdd(outcome, forcing, treatment, weights)

        assert result["tau"] == pytest.approx(true_tau, abs=0.5)
        assert result["se_tau"] > 0
        assert result["p_value"] < 0.05
        assert result["n_obs"] > 10

    def test_rdd_no_effect(self):
        """When true tau=0, estimate should be near zero and not significant."""
        rng = np.random.default_rng(42)
        n = 200
        forcing = np.concatenate([
            rng.uniform(-10, -0.1, size=n // 2),
            rng.uniform(0.1, 10, size=n // 2),
        ])
        treatment = (forcing < 0).astype(float)
        noise = rng.normal(0, 1.0, size=n)
        outcome = 3.0 + 0.5 * forcing + noise  # no treatment effect

        bw = select_bandwidth(forcing, frac=0.5)
        weights = triangular_kernel(forcing, bw)
        result = estimate_rdd(outcome, forcing, treatment, weights)

        assert abs(result["tau"]) < 1.0
        assert result["p_value"] > 0.05

    def test_rdd_uniform_vs_triangular(self):
        """Both kernels should recover similar tau from the same data."""
        rng = np.random.default_rng(42)
        n = 200
        true_tau = 1.5
        forcing = np.concatenate([
            rng.uniform(-10, -0.1, size=n // 2),
            rng.uniform(0.1, 10, size=n // 2),
        ])
        treatment = (forcing < 0).astype(float)
        outcome = 3.0 + true_tau * treatment + 0.5 * forcing + rng.normal(0, 0.3, size=n)

        bw = select_bandwidth(forcing, frac=0.5)
        w_tri = triangular_kernel(forcing, bw)
        w_uni = uniform_kernel(forcing, bw)

        r_tri = estimate_rdd(outcome, forcing, treatment, w_tri)
        r_uni = estimate_rdd(outcome, forcing, treatment, w_uni)

        # Both should be close to true tau
        assert r_tri["tau"] == pytest.approx(true_tau, abs=0.5)
        assert r_uni["tau"] == pytest.approx(true_tau, abs=0.5)
