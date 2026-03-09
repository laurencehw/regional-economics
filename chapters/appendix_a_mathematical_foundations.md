# Appendix A: Mathematical Foundations

---

This appendix collects the key derivations and matrix notation conventions used throughout the book. It is designed as a reference for students who want to see the formal structure behind the methods introduced in Chapters 3-A and 3-B, and for instructors who want to assign technical extensions. Readers who are comfortable with the intuitive explanations in the main text can skip this appendix without loss of continuity.

---

## A.1 Matrix Notation for Spatial Models

### The Spatial Weight Matrix

The spatial weight matrix $$\mathbf{W}$$ is an $$n \times n$$ non-negative matrix where $$n$$ is the number of spatial units (regions, countries, grid cells). Entry $$w_{ij}$$ measures the strength of the spatial relationship between units $$i$$ and $$j$$. Common specifications include:

**Binary contiguity:**
$$
w_{ij} = \begin{cases} 1 & \text{if } i \text{ and } j \text{ share a border} \\ 0 & \text{otherwise} \end{cases}
$$

**Inverse distance:**
$$
w_{ij} = \begin{cases} d_{ij}^{-\alpha} & \text{if } i \neq j \\ 0 & \text{if } i = j \end{cases}
$$

where $$d_{ij}$$ is the distance between units $$i$$ and $$j$$, and $$\alpha > 0$$ is a decay parameter (typically $$\alpha = 1$$ or $$\alpha = 2$$).

**$$k$$-nearest neighbors:**
$$
w_{ij} = \begin{cases} 1 & \text{if } j \text{ is among the } k \text{ nearest neighbors of } i \\ 0 & \text{otherwise} \end{cases}
$$

Note that $$k$$-nearest neighbor weights are generally not symmetric: $$j$$ may be among $$i$$'s nearest neighbors while $$i$$ is not among $$j$$'s.

**Row standardization.** In most applications, $$\mathbf{W}$$ is row-standardized so that each row sums to 1:

$$
\tilde{w}_{ij} = \frac{w_{ij}}{\sum_{k=1}^n w_{ik}}
$$

Row standardization ensures that the spatial lag $$\mathbf{W}\mathbf{y}$$ is a weighted average of neighbors' values rather than a weighted sum, which facilitates interpretation and comparability across units with different numbers of neighbors.

**Convention.** Throughout this book, $$\mathbf{W}$$ denotes the row-standardized weight matrix unless otherwise stated. The diagonal elements are always zero: $$w_{ii} = 0$$ for all $$i$$.

---

## A.2 Spatial Autoregressive Model (SAR)

### Specification

The spatial autoregressive model (also called the spatial lag model) is:

$$
\mathbf{y} = \rho \mathbf{W} \mathbf{y} + \mathbf{X} \boldsymbol{\beta} + \boldsymbol{\varepsilon}, \quad \boldsymbol{\varepsilon} \sim \mathcal{N}(\mathbf{0}, \sigma^2 \mathbf{I}_n)
$$

where:
- $$\mathbf{y}$$ is an $$n \times 1$$ vector of observations on the dependent variable
- $$\mathbf{W}$$ is an $$n \times n$$ spatial weight matrix
- $$\rho$$ is the spatial autoregressive parameter ($$|\rho| < 1$$ for stationarity)
- $$\mathbf{X}$$ is an $$n \times k$$ matrix of exogenous regressors
- $$\boldsymbol{\beta}$$ is a $$k \times 1$$ vector of slope parameters
- $$\boldsymbol{\varepsilon}$$ is an $$n \times 1$$ vector of i.i.d. errors

### Reduced Form

Solving for $$\mathbf{y}$$:

$$
(\mathbf{I}_n - \rho \mathbf{W}) \mathbf{y} = \mathbf{X} \boldsymbol{\beta} + \boldsymbol{\varepsilon}
$$

$$
\mathbf{y} = (\mathbf{I}_n - \rho \mathbf{W})^{-1} \mathbf{X} \boldsymbol{\beta} + (\mathbf{I}_n - \rho \mathbf{W})^{-1} \boldsymbol{\varepsilon}
$$

The matrix $$(\mathbf{I}_n - \rho \mathbf{W})^{-1}$$ is the spatial multiplier matrix. It can be expanded as:

$$
(\mathbf{I}_n - \rho \mathbf{W})^{-1} = \mathbf{I}_n + \rho \mathbf{W} + \rho^2 \mathbf{W}^2 + \rho^3 \mathbf{W}^3 + \cdots
$$

This power series representation shows that the effect of a shock to unit $$j$$ propagates to unit $$i$$ through all spatial paths: directly (through $$\rho \mathbf{W}$$), through second-order neighbors ($$\rho^2 \mathbf{W}^2$$), through third-order neighbors ($$\rho^3 \mathbf{W}^3$$), and so on, with geometrically declining weight.

### Maximum Likelihood Estimation

The log-likelihood function for the SAR model is:

$$
\ln L(\rho, \boldsymbol{\beta}, \sigma^2) = -\frac{n}{2} \ln(2\pi) - \frac{n}{2} \ln(\sigma^2) + \ln |\mathbf{I}_n - \rho \mathbf{W}| - \frac{1}{2\sigma^2} \boldsymbol{\varepsilon}' \boldsymbol{\varepsilon}
$$

where $$\boldsymbol{\varepsilon} = (\mathbf{I}_n - \rho \mathbf{W}) \mathbf{y} - \mathbf{X} \boldsymbol{\beta}$$.

The key computational challenge is the log-determinant term $$\ln |\mathbf{I}_n - \rho \mathbf{W}|$$, which must be evaluated at each candidate value of $$\rho$$ during optimization. For the row-standardized case, this can be computed via the eigenvalues of $$\mathbf{W}$$:

$$
\ln |\mathbf{I}_n - \rho \mathbf{W}| = \sum_{i=1}^n \ln(1 - \rho \omega_i)
$$

where $$\omega_1, \ldots, \omega_n$$ are the eigenvalues of $$\mathbf{W}$$. Since the eigenvalues need to be computed only once, the optimization over $$\rho$$ is fast.

### Direct, Indirect, and Total Effects

A key feature of the SAR model is that the marginal effect of a change in $$x_{jk}$$ (the $$k$$-th regressor in unit $$j$$) on $$y_i$$ depends on the spatial relationship between $$i$$ and $$j$$. The matrix of partial effects is:

$$
\frac{\partial \mathbf{y}}{\partial x_{jk}} = (\mathbf{I}_n - \rho \mathbf{W})^{-1} \beta_k
$$

LeSage and Pace (2009) decompose this into:

- **Direct effect:** The average diagonal element of $$(\mathbf{I}_n - \rho \mathbf{W})^{-1} \beta_k$$ — the effect of a change in $$x_{ik}$$ on $$y_i$$ (includes feedback through the spatial multiplier).
- **Indirect effect (spillover):** The average off-diagonal row sum — the effect of a change in $$x_{jk}$$ (for $$j \neq i$$) on $$y_i$$.
- **Total effect:** Direct + Indirect.

---

## A.3 Spatial Error Model (SEM)

### Specification

$$
\mathbf{y} = \mathbf{X} \boldsymbol{\beta} + \mathbf{u}, \quad \mathbf{u} = \lambda \mathbf{W} \mathbf{u} + \boldsymbol{\varepsilon}, \quad \boldsymbol{\varepsilon} \sim \mathcal{N}(\mathbf{0}, \sigma^2 \mathbf{I}_n)
$$

The SEM assumes that spatial dependence enters through the error term rather than the dependent variable. This captures spatially correlated unobservables — omitted variables that are themselves spatially structured.

### Reduced Form

$$
\mathbf{u} = (\mathbf{I}_n - \lambda \mathbf{W})^{-1} \boldsymbol{\varepsilon}
$$

$$
\mathbf{y} = \mathbf{X} \boldsymbol{\beta} + (\mathbf{I}_n - \lambda \mathbf{W})^{-1} \boldsymbol{\varepsilon}
$$

### Implications

In the SEM, $$\boldsymbol{\beta}$$ has its standard interpretation: a change in $$x_{ik}$$ affects $$y_i$$ by $$\beta_k$$, with no spillover effects. Spatial dependence affects only the error structure, making OLS consistent but inefficient. The ML estimator exploits the error structure for efficiency.

### When to Use SAR vs. SEM

- **SAR:** When the theoretical model implies substantive spatial interaction — one region's outcome causally affects its neighbors (trade spillovers, policy competition, knowledge diffusion).
- **SEM:** When the theoretical model implies that spatial patterns arise from omitted spatially correlated variables (climate, geology, historical institutions) rather than from direct interaction.
- **SDM (below):** When both channels may operate simultaneously.

---

## A.4 Spatial Durbin Model (SDM)

### Specification

$$
\mathbf{y} = \rho \mathbf{W} \mathbf{y} + \mathbf{X} \boldsymbol{\beta} + \mathbf{W} \mathbf{X} \boldsymbol{\theta} + \boldsymbol{\varepsilon}
$$

The SDM includes both a spatial lag of the dependent variable ($$\rho \mathbf{W} \mathbf{y}$$) and spatial lags of the regressors ($$\mathbf{W} \mathbf{X} \boldsymbol{\theta}$$). This is the most general of the three standard spatial models and nests both SAR ($$\boldsymbol{\theta} = \mathbf{0}$$) and, under specific parameter restrictions, SEM ($$\boldsymbol{\theta} = -\rho \boldsymbol{\beta}$$).

### Direct and Indirect Effects

The partial effects matrix for the SDM is:

$$
\frac{\partial \mathbf{y}}{\partial x_{jk}} = (\mathbf{I}_n - \rho \mathbf{W})^{-1} (\mathbf{I}_n \beta_k + \mathbf{W} \theta_k)
$$

The decomposition into direct, indirect, and total effects follows the same logic as the SAR, but the indirect effects now include both the spatial lag channel ($$\rho$$) and the spatially lagged regressor channel ($$\theta_k$$).

---

## A.5 Structural Gravity Model

### Theory

The structural gravity model, derived from Anderson and van Wincoop (2003), expresses bilateral trade flows as:

$$
X_{ij} = \frac{Y_i E_j}{Y^W} \left( \frac{\tau_{ij}}{P_j \Pi_i} \right)^{1-\sigma}
$$

where:
- $$X_{ij}$$ is the trade flow from exporter $$i$$ to importer $$j$$
- $$Y_i$$ is the total output of exporter $$i$$
- $$E_j$$ is the total expenditure of importer $$j$$
- $$Y^W$$ is world output
- $$\tau_{ij}$$ is the bilateral trade cost (iceberg form: $$\tau_{ij} \geq 1$$)
- $$\sigma > 1$$ is the elasticity of substitution
- $$P_j$$ is the inward multilateral resistance term (importer's price index)
- $$\Pi_i$$ is the outward multilateral resistance term

### Estimation via PPML

Taking the structural gravity equation to data:

$$
X_{ij} = \exp(\underbrace{\alpha_i}_{\text{exporter FE}} + \underbrace{\gamma_j}_{\text{importer FE}} + \underbrace{\boldsymbol{\delta}' \mathbf{z}_{ij}}_{\text{bilateral costs}}) \cdot \eta_{ij}
$$

where $$\mathbf{z}_{ij}$$ is a vector of observable bilateral trade cost proxies (log distance, contiguity, common language, colonial ties, RTA membership, STRI scores) and $$\eta_{ij}$$ is a multiplicative error term.

Santos Silva and Tenreyro (2006) showed that PPML estimation of this equation:

1. Is consistent under heteroskedasticity (unlike log-linearized OLS)
2. Naturally handles zero trade flows (unlike log-linearized OLS, which drops them)
3. Provides a consistent estimator of the parameters of the multiplicative model

The PPML estimator solves the first-order conditions:

$$
\sum_{i,j} \mathbf{z}_{ij} [X_{ij} - \exp(\hat{\alpha}_i + \hat{\gamma}_j + \hat{\boldsymbol{\delta}}' \mathbf{z}_{ij})] = \mathbf{0}
$$

via iteratively reweighted least squares (IRLS), as implemented in Lab 7's `ppml_estimator.py`.

### Interpreting Gravity Coefficients

The coefficient $$\delta_k$$ on a bilateral cost variable $$z_k$$ has the interpretation:

$$
\frac{\partial \ln E[X_{ij}]}{\partial z_k} = \delta_k
$$

For dummy variables (contiguity, common language, RTA), the semi-elasticity is $$e^{\delta_k} - 1$$ — the percentage change in trade associated with the presence vs. absence of the attribute.

For the STRI tariff equivalent (Lab 7), the ad-valorem tariff equivalent of an STRI score change $$\Delta s$$ is:

$$
\tau = e^{-\delta_{\text{STRI}} \cdot \Delta s} - 1
$$

where $$\delta_{\text{STRI}} < 0$$ (higher STRI reduces trade), so the tariff equivalent is positive.

---

## A.6 Convergence Measurement

### $$\beta$$-Convergence

$$\beta$$-convergence tests whether initially poorer regions grow faster than initially richer regions — "catch-up" growth. The standard cross-sectional regression is:

$$
\frac{1}{T} \ln \left( \frac{y_{i,t+T}}{y_{i,t}} \right) = \alpha + \beta \ln(y_{i,t}) + \varepsilon_i
$$

A negative $$\hat{\beta}$$ indicates unconditional $$\beta$$-convergence. The implied convergence speed is:

$$
b = -\frac{\ln(1 + \hat{\beta} T)}{T}
$$

and the half-life of convergence (years to close half the initial gap) is:

$$
t_{1/2} = \frac{\ln 2}{b}
$$

**Simplified form.** When the time period $$T = 1$$ (annual data), the convergence speed reduces to $$b \approx |\hat{\beta}|$$ (for small $$|\hat{\beta}|$$), and the half-life simplifies to $$t_{1/2} \approx \ln 2 / |\hat{\beta}|$$. This is the formula used in Lab 2's scaffold. For multi-year intervals ($$T > 1$$), the general formula above must be used to avoid overstating the convergence speed.

### $$\sigma$$-Convergence

$$\sigma$$-convergence tests whether the cross-sectional dispersion of income levels is declining over time:

$$
\sigma_t^2 = \frac{1}{n} \sum_{i=1}^n (\ln y_{it} - \overline{\ln y_t})^2
$$

$$\sigma$$-convergence occurs if $$\sigma_t^2$$ is declining. Note that $$\beta$$-convergence is necessary but not sufficient for $$\sigma$$-convergence: regions can exhibit catch-up growth while dispersion remains constant or increases (if shocks are large relative to the catch-up effect).

---

## A.7 Regression Discontinuity Design (RDD)

### Sharp RDD

The spatial regression discontinuity design exploits a geographic boundary that determines treatment assignment. Let $$r_i$$ denote the running variable (distance to the boundary), with treatment $$D_i = \mathbf{1}(r_i < 0)$$ (this matches the sign convention used in Lab 4, where units with negative forcing values are treated). The sharp RDD estimator identifies the local average treatment effect at the boundary (treated side just to the left of the cutoff minus control side just to the right):

$$
\tau_{\text{RDD}} = \lim_{r \uparrow 0} E[Y_i \mid r_i = r] - \lim_{r \downarrow 0} E[Y_i \mid r_i = r]
$$

### Local Linear Estimation

In practice, $$\tau_{\text{RDD}}$$ is estimated by fitting separate local linear regressions on each side of the cutoff within a bandwidth $$h$$:

$$
Y_i = \alpha + \tau D_i + \beta_1 r_i + \beta_2 D_i \cdot r_i + \varepsilon_i, \quad |r_i| \leq h
$$

Observations are weighted by a kernel function $$K(r_i / h)$$. Common kernels include:

- **Triangular:** $$K(u) = (1 - |u|) \cdot \mathbf{1}(|u| \leq 1)$$ — gives most weight to observations near the cutoff (preferred for RDD; Imbens and Kalyanaraman 2012)
- **Uniform:** $$K(u) = \mathbf{1}(|u| \leq 1)$$ — equal weight within the bandwidth

### Bandwidth Selection

The bandwidth $$h$$ trades off bias (smaller $$h$$ reduces bias from nonlinearity) against variance (smaller $$h$$ uses fewer observations). The Imbens-Kalyanaraman (2012) optimal bandwidth is a widely used data-driven choice that minimizes asymptotic mean squared error and serves as a benchmark in the literature. In the current Lab 4 scaffold, however, the bandwidth is selected using a simple rule-of-thumb based on a fixed fraction of the running variable's range; implementing the IK bandwidth and a sensitivity analysis across alternative values of $$h$$ is left as an extension.

### Inference

Standard errors are computed using the HC1 heteroskedasticity-consistent estimator:

$$
\hat{V}_{\text{HC1}} = \frac{n}{n-k} (\mathbf{X}' \mathbf{K} \mathbf{X})^{-1} \mathbf{X}' \mathbf{K} \hat{\boldsymbol{e}} \hat{\boldsymbol{e}}' \mathbf{K} \mathbf{X} (\mathbf{X}' \mathbf{K} \mathbf{X})^{-1}
$$

where $$\mathbf{K}$$ is the diagonal kernel weight matrix and $$\hat{\boldsymbol{e}}$$ is the vector of residuals.

---

## A.8 Synthetic Control Method (SCM)

### Setup

The synthetic control method (Abadie and Gardeazabal 2003; Abadie, Diamond, and Hainmueller 2010, 2015) estimates the causal effect of an event on a treated unit by constructing a counterfactual from a weighted combination of untreated "donor" units. Let $$Y_{1t}$$ denote the outcome for the treated unit and $$Y_{0t} = (Y_{2t}, \ldots, Y_{J+1,t})'$$ the outcomes for $$J$$ donor units.

### Optimization

The synthetic control weights $$\mathbf{w} = (w_2, \ldots, w_{J+1})'$$ are chosen to minimize the pre-treatment prediction error:

$$
\mathbf{w}^* = \arg\min_{\mathbf{w}} \| \mathbf{X}_1 - \mathbf{X}_0 \mathbf{w} \|_{\mathbf{V}}^2 \quad \text{s.t. } w_j \geq 0, \; \sum_{j=2}^{J+1} w_j = 1
$$

where $$\mathbf{X}_1$$ is a vector of pre-treatment characteristics for the treated unit, $$\mathbf{X}_0$$ is the corresponding matrix for donor units, and $$\mathbf{V}$$ is a positive definite weighting matrix (typically diagonal, with entries reflecting the predictive power of each covariate).

### Treatment Effect

The estimated treatment effect at time $$t$$ (post-intervention) is:

$$
\hat{\tau}_t = Y_{1t} - \sum_{j=2}^{J+1} w_j^* Y_{jt}
$$

The "gap plot" — $$\hat{\tau}_t$$ over time — is the primary visual output of the SCM (Lab 5).

### Inference via Placebo Tests

Because the SCM typically has $$J$$ small, conventional inference is infeasible. Instead, "in-space" placebo tests iteratively apply the SCM procedure to each donor unit as if it were treated, producing a distribution of placebo gaps. The treated unit's gap is compared to this distribution. If the treated unit's post-treatment gap is extreme relative to the placebo distribution, the effect is considered significant. A common criterion is that the treated unit's post/pre RMSPE ratio falls in the top $$\alpha$$ fraction of placebo ratios.

---

## A.9 Spatial Autocorrelation: Moran's I

### Definition

Moran's $$I$$ statistic measures the degree of spatial autocorrelation in a variable:

$$
I = \frac{n}{\sum_{i}\sum_{j} w_{ij}} \cdot \frac{\sum_{i}\sum_{j} w_{ij} (y_i - \bar{y})(y_j - \bar{y})}{\sum_{i} (y_i - \bar{y})^2}
$$

Under the null hypothesis of no spatial autocorrelation, $$E[I] = -1/(n-1) \approx 0$$ for large $$n$$.

### Inference

**Permutation inference.** Under the null, any permutation of $$\mathbf{y}$$ across spatial locations is equally likely. The reference distribution is constructed by:

1. Randomly permuting $$\mathbf{y}$$ across locations (while holding $$\mathbf{W}$$ fixed)
2. Computing $$I$$ for each permutation
3. Repeating $$B$$ times (typically $$B = 999$$)
4. Computing the pseudo-p-value as the fraction of permuted $$I$$ values that exceed the observed $$I$$

This is the approach used in Lab 6.

---

## A.10 Notation Index

| Symbol | Meaning | Chapter(s) |
|---|---|---|
| $$\mathbf{W}$$ | Spatial weight matrix | 3-A, Labs 1, 6 |
| $$\rho$$ | SAR spatial autoregressive parameter | 3-A, Lab 1 |
| $$\lambda$$ | SEM spatial error parameter | 3-A |
| $$\boldsymbol{\beta}$$ | Slope parameter vector | Throughout |
| $$\boldsymbol{\theta}$$ | SDM spatially lagged regressor coefficients | 3-A |
| $$\tau_{ij}$$ | Bilateral trade cost (iceberg form) | 1, 3-B, Lab 7 |
| $$\sigma$$ | Elasticity of substitution (gravity); also cross-sectional std. dev. (convergence) | 3-B; 3-A |
| $$P_j, \Pi_i$$ | Multilateral resistance terms | 3-B |
| $$I$$ | Moran's $$I$$ statistic | 3-A, Lab 6 |
| $$\omega_i$$ | Eigenvalues of $$\mathbf{W}$$ | A.2 |
| $$n$$ | Number of spatial units | Throughout |
| $$k$$ | Number of regressors | Throughout |
| $$T$$ | Time period length | 3-A (convergence) |
| $$h$$ | RDD bandwidth | A.7, Lab 4 |
| $$K(\cdot)$$ | Kernel function | A.7, Lab 4 |
| $$\mathbf{w}$$ | SCM donor weights | A.8, Lab 5 |
| $$\mathbf{V}$$ | SCM covariate weighting matrix | A.8, Lab 5 |

**Note on overloaded symbols.** Several symbols serve double duty across chapters — a common and unavoidable feature of interdisciplinary work. $$\sigma$$ denotes the elasticity of substitution in the trade/gravity context (Chapters 1, 3-B) and cross-sectional standard deviation in the convergence context (Chapter 3-A). $$\tau$$ denotes iceberg trade costs in Chapters 1 and 3-B and has no conflicting usage. $$\lambda$$ denotes the SEM spatial error parameter in Chapter 3-A and the manufacturing expenditure share in Chapter 1's core-periphery model. Context disambiguates in all cases.
