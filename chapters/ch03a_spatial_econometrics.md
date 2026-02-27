# Chapter 3-A: Spatial Econometrics & Inequality Measurement

---

## Introduction: The Map Is Not the Residual

In 2010, a team of economists at the World Bank published an influential study of regional growth across European NUTS-2 regions. Their headline finding was reassuring: poorer regions were converging toward richer ones at a rate broadly consistent with neoclassical growth theory. But when Ertur and Koch (2007) reestimated the same relationship using a spatial autoregressive model — one that explicitly allowed the growth rate of each region to depend on the growth rates of its neighbors — the convergence coefficient changed by nearly a third, and the estimated speed of convergence slowed substantially. The "missing" convergence had been absorbed into a spatial spillover term that the original OLS regression had forced into the error term.

This is not an isolated curiosity. Across virtually every domain of regional economics — housing prices, innovation diffusion, labor market dynamics, environmental pollution — ordinary least squares produces estimates that are, at best, inefficient and, at worst, severely biased when the data are spatially dependent. The reason is structural, not merely statistical: economic outcomes in one region are partly caused by outcomes and characteristics of nearby regions. A factory's productivity depends on the thickness of the local labor market, which depends on how many other firms have located nearby, which depends on productivity — the same circularity that Chapter 1 identified in the NEG framework reappears here as an econometric identification problem.

This chapter — the first of the two-part methodological core — provides the spatial econometric tools to handle that problem. (Chapter 3-B covers trade measurement and the gravity model.) It is organized as a sequence of modeling decisions, each building on the last:

1. **Define the spillover structure.** How do regions influence each other? The answer is encoded in the spatial weight matrix $W$, which is a substantive economic hypothesis, not a technical convenience. Section 3A.1 covers construction, normalization, and sensitivity.

2. **Select the model class.** Given a $W$, what kind of spatial dependence is present? Section 3A.2 introduces the three workhorses — the Spatial Autoregressive model (SAR), the Spatial Error Model (SEM), and the Spatial Durbin Model (SDM) — and develops the logic of specification testing.

3. **Interpret effects correctly.** In spatial models, a one-unit change in $x$ in region $i$ affects outcomes in region $i$ (the direct effect) but also ripples through the network to affect every connected region (the indirect effect). Section 3A.3 unpacks the impact decomposition that LeSage and Pace (2009) developed and that applied work too often ignores.

4. **Confront identification threats.** Section 3A.4 addresses Manski's (1993) reflection problem — the fundamental difficulty of separating endogenous peer effects from correlated shocks — and the related problem of endogenous network formation.

5. **Bridge to causal inference.** Section 3A.5 introduces the design-based methods — Spatial Regression Discontinuity, Synthetic Control, and difference-in-differences with spatial spillovers — that complement parametric spatial models when causal claims are the objective. This section provides the conceptual foundation for Labs 4, 5, and 6 in the regional chapters.

6. **Navigate the data landscape.** Section 3A.7 surveys the key datasets that the Applied Labs in this book draw on, and discusses reproducibility principles for spatial empirical work.

The methods presented here are not alternatives to the theoretical frameworks of Chapters 1 and 2 — they are those frameworks made operational. The NEG's circular causation becomes the SAR's spatial lag. Institutional thickness becomes a regressor whose indirect effects propagate through a network of trading partners. Path dependence becomes the identifying assumption in a synthetic control design. Every regional chapter that follows will use at least one tool from this chapter or Chapter 3-B, and most will use several.

---

## 3A.1 The Spatial Weight Matrix: A Substantive Modeling Choice

Every spatial econometric model begins with a matrix $W$ — an $n \times n$ array that encodes the assumed linkage structure among $n$ regions. Element $w_{ij}$ captures the strength of the connection from region $j$ to region $i$: how much region $j$'s outcomes or characteristics "matter" for region $i$. The diagonal is set to zero by convention (a region does not influence itself through the spatial channel), and the matrix is typically row-standardized so that each row sums to one, converting $Wy$ into a weighted average of neighbors' outcomes.

The choice of $W$ is, conceptually, the most consequential decision in spatial econometrics. It encodes a hypothesis about the channel through which spatial interaction operates. Different hypotheses produce different matrices, and different matrices can produce substantially different parameter estimates. This is not a bug; it is a feature. If inference were invariant to $W$, spatial dependence would not be economically meaningful.

### Contiguity-Based Weights

The simplest and most common approach defines $w_{ij} = 1$ if regions $i$ and $j$ share a border, and $w_{ij} = 0$ otherwise. The "queen" variant counts regions as neighbors if they share any boundary point (including corners); the "rook" variant requires a shared edge. After row standardization, $Wy_i$ becomes the simple average of $y$ in all contiguous regions.

Contiguity weights are appropriate when the hypothesized spillover channel is physical adjacency — pollution diffusion, cross-border commuting, contagion of political instability. They are the default in many applied studies, but their simplicity is also their limitation: they treat all neighbors as equally important and ignore connections between non-contiguous regions that may be strongly linked through trade, migration, or shared infrastructure.

In Lab 6 (Africa), the adjacency weight matrix — with optional border-length weighting — is used to compute Moran's $I$ on night-lights radiance. The hypothesis is that economic activity (proxied by light intensity) clusters along shared borders because of cross-border trade, migration corridors, and infrastructure networks. This is reasonable for Sub-Saharan Africa, where overland linkages dominate — but it would miss the point entirely for island economies or regions connected primarily by air transport.

### Distance-Based Weights

A more flexible approach defines $w_{ij}$ as a decreasing function of the distance $d_{ij}$ between regions $i$ and $j$, typically the great-circle distance between centroids:

$$
w_{ij} = \begin{cases} d_{ij}^{-\gamma} & \text{if } d_{ij} \leq \bar{d} \\ 0 & \text{if } d_{ij} > \bar{d} \end{cases}
$$

where $\gamma > 0$ controls the rate of distance decay and $\bar{d}$ is an optional distance cutoff that zeroes out long-range connections. The matrix is then row-standardized.

The distance-decay parameter $\gamma$ is itself informative. Estimated $\gamma$ values for trade flows are typically 0.7–1.5 (gravity models); for knowledge spillovers measured by patent citations, they are considerably higher (1.5–3.0), suggesting that tacit knowledge diffuses more locally than goods. The choice of $\gamma$ should be guided by the nature of the hypothesized interaction, not by statistical fit alone.

### K-Nearest-Neighbor Weights

A pragmatic compromise between contiguity and distance weights defines each region's neighborhood as its $k$ nearest regions by distance. The resulting matrix has exactly $k$ nonzero entries per row (before row standardization), ensuring that every region has the same number of neighbors — a useful property when regions vary dramatically in size and border count. Lesotho, entirely surrounded by South Africa, has one contiguity neighbor; Germany has nine. K-nearest-neighbor weights give both regions the same local information set.

The limitation is symmetry: if region $i$ counts $j$ among its $k$ nearest neighbors, region $j$ may not reciprocate. Applied work typically symmetrizes the matrix (setting $w_{ij} = w_{ji} = 1$ if either counts the other as a neighbor), but this introduces a modeling choice that is rarely discussed.

### Economic-Flow Weights

The most substantively motivated approach constructs $W$ from observed economic interactions — trade flows, migration streams, financial linkages, or input-output relationships. In Lab 1 (Americas), the spatial weight matrix is built from bilateral trade values: $w_{ij}$ equals the value of goods that region $j$ exports to region $i$. After row standardization, $Wy_i$ is the trade-weighted average GDP growth of $i$'s trading partners — a direct operationalization of the NEG's market-access channel.

Trade-weighted $W$ matrices have three advantages over purely geographic alternatives. First, they capture economic proximity even when geographic proximity is misleading: South Korea and the United States are 10,000 kilometers apart but are deeply integrated through semiconductor supply chains. Second, they can be time-varying — a $W$ built from 2005 trade data differs from one built from 2020 data, reflecting changes in integration patterns. Third, they allow for asymmetry: Mexico may depend heavily on the US market, but the reverse dependence is modest.

The disadvantage is endogeneity. Trade flows are not exogenous to regional outcomes — a region that grows faster may attract more trade, inducing a correlation between $Wy$ and the error term that contaminates the spatial lag estimate. Section 3A.4 addresses this directly. Lab 2 (Asia) uses input-output tables from the WIOD to construct a value-added-weighted $W$ that mitigates some of this concern by measuring structural interdependence rather than contemporaneous flows.

### Normalization and Its Consequences

Before a weight matrix enters estimation, it must be normalized. The choice of normalization is itself consequential.

**Row standardization** divides each element $w_{ij}$ by the row sum $\sum_j w_{ij}$, so that $Wy_i$ becomes a weighted average of neighbors' outcomes. This is the dominant convention and the one used throughout this book. Its advantage is interpretability: $\rho$ has a natural reading as the elasticity of $y_i$ with respect to the average neighbor outcome. Its disadvantage is that it distorts the original economic content of the weights. If $w_{ij}$ originally measured bilateral trade in dollars, row standardization converts it to trade shares — and a country that trades primarily with one large partner (Mexico with the US) is treated the same as a country whose trade is diversified across many partners (Germany with the EU), even though the economic meaning of their spatial dependence is quite different.

**Spectral normalization** divides the entire matrix by its largest eigenvalue, ensuring that $\rho$ is bounded between $-1$ and $1$ without distorting relative magnitudes. This preserves the economic content of the weights but makes $\rho$ harder to interpret.

**Min-max normalization** scales each element by the range of the matrix. This is less common but appears in some spatial panel specifications.

The practical advice is straightforward: row standardization is the default unless you have a specific reason to preserve the scale of the weights. But when comparing results across studies, check the normalization convention — a $\rho$ of 0.3 under row standardization and a $\rho$ of 0.3 under spectral normalization carry different economic meanings.

### The Sensitivity Question

How much do results depend on the choice of $W$? The honest answer is: sometimes a great deal. LeSage and Pace (2014) argue that direct effects (the impact of $x_i$ on $y_i$) are typically robust to $W$ specification, but indirect effects (the impact of $x_j$ on $y_i$ through the network) are often sensitive. This is intuitive — the direct effect is identified primarily from within-region variation, while the indirect effect depends entirely on the assumed spillover structure.

The appropriate response is not to search over $W$ specifications until one produces the desired result. It is to report results under multiple specifications and interpret sensitivity as information about the robustness of the spillover claim. The Data in Depth box at the end of this chapter illustrates this approach with a concrete example.

### Moran's $I$: The First Diagnostic

Before estimating any spatial model, the analyst should establish that spatial autocorrelation is present in the data. Moran's $I$ (1950) is the standard global diagnostic:

$$
I = \frac{n}{\sum_{i}\sum_{j} w_{ij}} \cdot \frac{\sum_{i}\sum_{j} w_{ij}(y_i - \bar{y})(y_j - \bar{y})}{\sum_{i}(y_i - \bar{y})^2}
$$

Under the null hypothesis of no spatial autocorrelation, $I$ has an expected value of $-1/(n-1)$ (approximately zero for large $n$). Positive values indicate clustering — similar values near similar values — while negative values indicate dispersion. Inference is typically conducted by permutation: randomly reassign observations to locations many times (Lab 6 uses 999 permutations by default), compute $I$ for each permuted dataset, and compare the observed $I$ to the permutation distribution.

Moran's $I$ is the spatial analog of the Durbin-Watson statistic in time series: a first-pass check that tells you whether spatial dependence is worth modeling. A large, significant $I$ on OLS residuals says "something spatial is going on" — it does not say whether the dependence is in the dependent variable (SAR), the errors (SEM), or both (SDM). The LM tests in Section 3A.2 provide that discrimination.

Lab 6 (Africa) uses Moran's $I$ as the primary analytical tool rather than merely a diagnostic. The two-step procedure — computing $I$ on raw night-lights, then on governance-residualized night-lights — directly tests whether spatial autocorrelation in economic activity is partly explained by the spatial pattern of institutional quality. The decline in $I$ after residualization measures how much of the spatial clustering is "institutional" versus "geographic."

---

## 3A.2 From OLS to Spatial Regression: SAR, SEM, and SDM

### Why OLS Fails

Consider a standard cross-sectional regression of regional outcomes on covariates:

$$
y = X\beta + \varepsilon
$$

where $y$ is an $n \times 1$ vector of outcomes, $X$ is an $n \times k$ matrix of covariates, and $\varepsilon$ is the error term. OLS assumes that $\varepsilon_i$ and $\varepsilon_j$ are independent for $i \neq j$. In spatial settings, this assumption fails for two distinct reasons:

1. **Substantive interdependence.** Region $i$'s outcome genuinely depends on region $j$'s outcome — a firm's productivity depends on the productivity of its suppliers, a worker's wage depends on the wages available in neighboring regions through the outside-option channel. This is spatial dependence in the dependent variable.

2. **Shared unobservables.** Region $i$ and region $j$ experience similar unobserved shocks — weather, policy contagion, common exposure to a global commodity price — that induce correlation in the error term even after conditioning on observables. This is spatial dependence in the errors.

If the true data-generating process involves spatial dependence in $y$, OLS estimates of $\beta$ are biased and inconsistent — the omitted $Wy$ term is correlated with $X$ whenever spatial patterns in the covariates mirror those in the outcome (which they almost always do). If the dependence is only in the errors, OLS is unbiased but inefficient, and standard errors are too small. The two cases call for different models.

### The Spatial Autoregressive Model (SAR)

The SAR — also called the spatial lag model — models substantive interdependence directly:

$$
y = \rho W y + X\beta + \varepsilon, \qquad \varepsilon \sim N(0, \sigma^2 I)
$$

The parameter $\rho$ captures the strength of the spatial multiplier: each region's outcome is a function of the weighted average of its neighbors' outcomes, plus its own covariates and an idiosyncratic error. The model is estimated by maximum likelihood (the log-likelihood involves the log-determinant of $(I - \rho W)$, which accounts for the simultaneity) or by instrumental variables (using $WX$, $W^2X$, etc., as instruments for $Wy$).

The stationarity condition for the SAR is that $\rho$ lie within the inverse of the extreme eigenvalues of $W$; for a row-standardized $W$ with nonnegative entries, this simplifies to $|\rho| < 1$. When $\rho$ approaches 1, the spatial multiplier $(I - \rho W)^{-1}$ becomes very large, and a small local shock propagates almost without attenuation through the entire network — the spatial analog of a unit root in time series.

**Estimation.** The SAR cannot be estimated consistently by OLS because $Wy$ is endogenous — it is a function of $\varepsilon$ through the reduced form. Two estimation strategies dominate:

*Maximum likelihood (ML).* The log-likelihood of the SAR is:

$$
\ell(\rho, \beta, \sigma^2) = -\frac{n}{2}\ln(2\pi\sigma^2) + \ln|I - \rho W| - \frac{1}{2\sigma^2}(y - \rho Wy - X\beta)'(y - \rho Wy - X\beta)
$$

The key computational challenge is the log-determinant term $\ln|I - \rho W|$, which captures the Jacobian of the transformation from $\varepsilon$ to $y$. For moderately sized datasets ($n < 5{,}000$), the log-determinant can be computed directly from the eigenvalues of $W$: $\ln|I - \rho W| = \sum_{i=1}^n \ln(1 - \rho \lambda_i)$, where $\lambda_1, \ldots, \lambda_n$ are the eigenvalues of $W$. For larger datasets, sparse-matrix approximations (Ord 1975, Barry and Pace 1999) are necessary. The lab code in this book uses the eigenvalue decomposition for its transparency.

*Instrumental variables (IV).* Use $WX$, $W^2X$, and higher-order spatial lags of the covariates as instruments for $Wy$. The logic is that $WX$ is correlated with $Wy$ (neighbors' characteristics predict neighbors' outcomes) but uncorrelated with $\varepsilon_i$ if $X$ is exogenous. Kelejian and Prucha (1998) established the formal conditions. IV estimation is less efficient than ML when the Gaussian assumptions hold, but more robust to distributional misspecification.

The SAR is the right model when the theory predicts genuine outcome-to-outcome spillovers — when GDP growth in one region causally affects growth in neighboring regions through trade multipliers, technology diffusion, or labor mobility. Lab 1 (Americas) estimates a SAR on GDP growth across 34 Western Hemisphere economies, using trade-weighted $W$. The estimated $\rho$ is small in the unconditional specification but becomes more economically meaningful when institution-interaction terms are included — a finding consistent with the hypothesis that spatial spillovers are conditional on institutional quality.

### The Spatial Error Model (SEM)

The SEM models spatial dependence as a nuisance in the error structure:

$$
y = X\beta + u, \qquad u = \lambda Wu + \varepsilon, \qquad \varepsilon \sim N(0, \sigma^2 I)
$$

Here $\lambda$ captures the degree of spatial correlation in the disturbances. (Note: $\lambda$ denotes the spatial error parameter throughout this chapter; Chapter 1 uses $\lambda$ for the manufacturing share in the core-periphery model. The two usages are standard in their respective literatures and do not overlap in any equation.) The SEM does not claim that neighbors' outcomes directly affect one another — it claims that neighbors share unobserved shocks. The practical consequence is that OLS estimates of $\beta$ remain consistent (no omitted variable bias from $Wy$), but standard errors computed under the independence assumption are wrong, typically too small. The SEM corrects the variance-covariance matrix.

The SEM is appropriate when the analyst believes that spatial patterns in the outcome are driven entirely by shared exposure to omitted variables — common weather shocks across adjacent agricultural regions, shared exposure to a national fiscal policy, or similar regulatory environments that the model does not explicitly control for. In practice, the SEM is also useful as a diagnostic: if a SAR specification produces a small $\rho$ but a large $\lambda$ in the residuals, the spatial pattern is likely in the errors, not the outcomes.

**Estimation.** The SEM is estimated by ML, with the log-likelihood taking a similar form to the SAR but replacing $\rho$ with $\lambda$ in the Jacobian term. Alternatively, Kelejian and Prucha (1999) proposed a GMM estimator that uses the spatial structure of the residuals to estimate $\lambda$ without computing the log-determinant — useful for very large datasets. A practical shortcut that is sometimes (but should not be) used in applied work is Feasible GLS: estimate OLS, compute $\hat{\lambda}$ from the residuals, then Cochrane-Orcutt-style transform the data. This is generally less efficient than ML and can perform poorly when $\lambda$ is large.

**Interpretation.** The SEM's $\beta$ coefficients have the same interpretation as OLS coefficients — the marginal effect of $x_{ki}$ on $y_i$. There are no indirect effects through the error process. The spatial dependence in the SEM is "nuisance" in the sense that it does not change the economic story about how covariates affect outcomes — it only changes the precision with which those effects are estimated. This is why the SEM is sometimes called the "spatial Newey-West" correction, by analogy with heteroskedasticity-and-autocorrelation-consistent standard errors in time series.

### The Spatial Durbin Model (SDM)

The SDM nests both the SAR and SEM as special cases:

$$
y = \rho W y + X\beta + WX\theta + \varepsilon
$$

The addition of $WX\theta$ — the spatially lagged covariates — allows neighbors' characteristics to affect region $i$'s outcome directly, not just through the spatial multiplier. LeSage and Pace (2009) argue that the SDM should be the default specification because it avoids the strong restriction implicit in the SAR (that only the weighted average of neighbors' outcomes matters, not their characteristics) and the strong restriction implicit in the SEM (that there is no substantive outcome-to-outcome spillover).

The SDM is the workhorse model in applied spatial economics. If $\theta = 0$, it reduces to the SAR. If $\theta = -\rho\beta$, it reduces to the SEM (a restriction known as the "common factor" test). Estimating the unrestricted SDM and testing these restrictions is a principled way to select between the SAR and SEM, rather than choosing a priori.

### Specification Testing: LM Tests and the Anselin Decision Rule

Anselin (1988) proposed a widely used specification sequence based on Lagrange Multiplier tests applied to the OLS residuals:

1. Estimate the model by OLS.
2. Compute $\text{LM}_\text{lag}$ (testing $\rho = 0$ given $\lambda = 0$) and $\text{LM}_\text{error}$ (testing $\lambda = 0$ given $\rho = 0$).
3. If neither rejects, OLS is adequate.
4. If only one rejects, estimate the corresponding model.
5. If both reject, use the robust versions ($\text{RLM}_\text{lag}$ and $\text{RLM}_\text{error}$) to adjudicate.
6. If the robust tests still do not clearly discriminate, estimate the SDM.

This sequence provides a disciplined approach to model selection that avoids data-mining across spatial specifications. The Data in Depth box below demonstrates it with NUTS-2 data.

---

## 3A.3 Impact Decomposition: Direct, Indirect, and Total Effects

### The Interpretation Problem

In a standard OLS regression, the coefficient $\beta_k$ on covariate $x_k$ has a simple interpretation: a one-unit increase in $x_{ki}$ is associated with a $\beta_k$-unit change in $y_i$, holding other covariates constant. In a SAR or SDM, this interpretation is wrong.

To see why, rewrite the SAR in reduced form:

$$
y = (I - \rho W)^{-1}(X\beta + \varepsilon)
$$

The matrix $(I - \rho W)^{-1}$ is the spatial multiplier. It can be expanded as a power series:

$$
(I - \rho W)^{-1} = I + \rho W + \rho^2 W^2 + \rho^3 W^3 + \cdots
$$

The $I$ term captures the own-region effect. The $\rho W$ term captures the first-order spillover: a change in $x_i$ affects $y_i$, which affects $y_j$ for every neighbor $j$ of $i$, weighted by $\rho w_{ji}$. The $\rho^2 W^2$ term captures the second-order feedback: the change in $y_j$ ripples to $j$'s neighbors, some of which may include $i$ itself. The series converges (stationarity requires $|\rho| < 1$), but the total effect of a local change is always larger than the coefficient $\beta_k$ alone suggests.

### LeSage-Pace Decomposition

LeSage and Pace (2009) formalize this by defining, for each covariate $x_k$:

- **Direct effect**: The average of the diagonal elements of $S_k = (I - \rho W)^{-1} \cdot \beta_k I$ (for SAR) or $(I - \rho W)^{-1} \cdot (\beta_k I + \theta_k W)$ (for SDM). This is the effect of a change in $x_{ki}$ on $y_i$, including the feedback that passes through the network and returns to $i$.

- **Total effect**: The average row sum of $S_k$. This is the effect of a uniform one-unit increase in $x_k$ across all regions on $y_i$ — the combination of the direct stimulus and all indirect spillovers.

- **Indirect effect**: Total minus direct. This measures the pure spillover — how much of the total effect arrives through other regions' responses.

In the SAR, the ratio of indirect to direct effect depends only on $\rho$ and the structure of $W$, not on $\beta_k$. When $\rho$ is small (say, 0.1), the indirect effect is modest — perhaps 10–15 percent of the total. When $\rho$ is large (say, 0.6), the indirect effect can exceed the direct effect: more than half the total impact of a policy change propagates through spatial spillovers rather than operating locally. This is the spatial analog of the Keynesian multiplier, and it has the same policy implication: ignoring the multiplier understates the true effect of localized interventions.

### Why It Matters for Policy

Consider a concrete example from Lab 1. Suppose a country in the Americas improves its institutional quality — strengthening property rights, reducing corruption, increasing regulatory predictability. The direct effect is the improvement in that country's own GDP growth. But if the SAR multiplier is operative, the improvement also increases growth in trading partners (through better contract enforcement and more predictable trade policy), which feeds back to the original country. The total effect of institutional reform is larger than the within-country effect alone.

This logic is not merely theoretical. The interaction specifications in Lab 1 show that $\rho$ is larger when institutions are included as moderators — spatial spillovers in the Americas are stronger among economies with better institutional quality. The implication for policy evaluation is stark: a cost-benefit analysis that treats institutional reform as a purely domestic intervention will understate its returns.

### A Worked Example: Three Regions

To build intuition, consider the simplest possible case: three regions arranged in a line, so that region A borders B, B borders C, but A and C are not neighbors. The row-standardized contiguity $W$ is:

$$
W = \begin{pmatrix} 0 & 1 & 0 \\ 0.5 & 0 & 0.5 \\ 0 & 1 & 0 \end{pmatrix}
$$

Region A's only neighbor is B; region C's only neighbor is B; but B has two neighbors, so each gets weight 0.5.

Now suppose $\rho = 0.4$ and $\beta = 1$ for a single covariate $x$. The spatial multiplier is:

$$
(I - 0.4W)^{-1} \approx \begin{pmatrix} 1.10 & 0.48 & 0.10 \\ 0.24 & 1.19 & 0.24 \\ 0.10 & 0.48 & 1.10 \end{pmatrix}
$$

The diagonal elements (1.10, 1.19, 1.10) are the direct effects. A one-unit increase in $x_A$ raises $y_A$ by 1.10, not 1.00 — the extra 0.10 comes from the feedback loop: $x_A$ raises $y_A$, which raises $y_B$ (through the spatial lag), which feeds back to raise $y_A$ further (because B is A's neighbor). The feedback is modest here because $\rho = 0.4$ and the loop passes through two edges.

The off-diagonal elements are the indirect effects. A one-unit increase in $x_A$ raises $y_B$ by 0.24 and $y_C$ by 0.10. The spillover to B occurs because it is a neighbor of A. The spillover to C is indirect — it passes through B, and is smaller because it involves two edges in the network and is attenuated by higher powers of $\rho$.

The total effect of increasing $x_A$ by one unit on total output ($y_A + y_B + y_C$) is $1.10 + 0.24 + 0.10 = 1.44$. In other words, the spatial multiplier increases the aggregate return to a localized intervention by 44 percent. This is the quantitative content of the claim that ignoring spatial spillovers understates the benefits of place-based policy.

Notice that region B — the central hub — has a higher direct effect (1.19) than the peripheral regions (1.10). This is because B has more connections, so the feedback loop is richer. In real-world applications, better-connected regions (trade hubs, capital cities, transport nodes) will systematically show larger direct effects. This is not a statistical artifact — it reflects the genuine economic logic that well-connected regions benefit more from their own improvements because those improvements propagate further and return more forcefully.

### The Asymmetry in SDM Effects

In the SDM, the indirect effect also picks up the $\theta_k$ channel: neighbors' covariate values directly influence the focal region's outcome. This is appropriate when spillovers operate through characteristics rather than outcomes — for example, when a neighbor's investment in education raises human capital in the local labor market through cross-border commuting.

The SDM allows for a richer and potentially asymmetric pattern of effects. Consider a case where $\beta > 0$ (a country's own institutional quality raises its growth) but $\theta < 0$ (neighbors' institutional quality *reduces* local growth, perhaps through competitive diversion of investment). The direct effect would be positive, but the indirect effect could be negative — institutional improvement in a neighbor diverts capital away from the focal region. This competitive dynamic is invisible in the SAR, where indirect effects are always in the same direction as direct effects. The SDM's flexibility to capture both complementary and competitive spatial relationships is a principal reason LeSage and Pace (2009) recommend it as the default specification.

---

## 3A.4 Identification Threats: The Reflection Problem and Endogenous Networks

### Manski's Tripartite Decomposition

Charles Manski's 1993 paper on the identification of endogenous social effects established a framework that spatial econometricians continue to grapple with. Manski distinguished three channels through which individuals (or regions) in the same group may exhibit similar behavior:

1. **Endogenous effects**: Region $i$'s outcome is directly influenced by region $j$'s outcome. This is the $\rho Wy$ term in the SAR.

2. **Exogenous (contextual) effects**: Region $i$'s outcome is influenced by region $j$'s characteristics. This is the $\theta WX$ term in the SDM.

3. **Correlated effects**: Region $i$ and $j$ behave similarly because they share common unobserved shocks or have been selected into the same group by a process correlated with the outcome. This is captured by spatially correlated errors.

Manski's result is that, in a linear-in-means model without exclusion restrictions, all three effects are not simultaneously identified from cross-sectional data. Intuitively, if regions that share borders also share policy regimes, weather, and cultural traits, it is impossible to determine whether the observed correlation in outcomes reflects genuine spillovers ($\rho$), the influence of shared characteristics ($\theta$), or common unobservables ($\lambda$).

### Practical Implications for Applied Work

This is not an abstract impossibility theorem — it has direct consequences for every spatial regression in this book:

**The SAR identifies $\rho$ only if correlated effects are absent or controlled for.** If $E[\varepsilon_i \varepsilon_j] \neq 0$ and this correlation is not modeled (as in the SEM component), the ML estimate of $\rho$ absorbs the correlated-effects channel and is biased upward. This is why the near-zero $\rho$ in Lab 1's unconditional Americas SAR may actually be more credible than a large estimate would be: it suggests that the trade-weighted $W$ is not simply proxying for shared macro shocks.

**The SDM can separate endogenous and exogenous effects, but only if $W$ is exogenous.** When $W$ is based on geographic contiguity, exogeneity is defensible (borders were drawn centuries ago and are not determined by current outcomes). When $W$ is based on contemporaneous trade flows, exogeneity is suspect — and instrumentation strategies (using historical trade patterns, geographic distance, or colonial linkages) become necessary.

**Identification improves with variation in $W$.** If every region has the same network structure, the model cannot distinguish network effects from common shocks. Identification is strongest when the spatial structure varies across regions in ways that are plausibly exogenous — for example, when some regions have many neighbors and others have few, or when trade intensity varies for historical reasons (colonial trade routes, resource complementarities) rather than contemporaneous economic performance.

### Endogenous Network Formation

A deeper problem arises when the network itself is a choice variable. Trade relationships, migration corridors, and supply chain linkages are all endogenous — they reflect the same economic forces that determine outcomes. If high-growth regions attract more trade (reasonable), and the analyst constructs $W$ from observed trade, then $W$ is positively correlated with $y$ by construction, and the spatial lag coefficient $\rho$ will be biased upward even in the absence of any genuine spillover.

Three approaches address this, each involving a tradeoff between economic specificity and exogeneity:

1. **Predetermined networks.** Use $W$ from a prior period, on the assumption that lagged trade patterns are determined by past conditions and are not responsive to current outcome innovations. The argument is that trade relationships formed in 2015 reflect 2015 economic conditions and are plausibly exogenous to 2024 outcome innovations. Lab 1 uses trade data from the same cross-section year, which makes this a vulnerability — a robustness check using five-year lagged trade would strengthen identification. The cost of predetermination is that the network may be outdated: trade patterns shift, and a $W$ from 2015 may misrepresent 2024 linkages. The analyst faces a bias-variance tradeoff between endogeneity (contemporaneous $W$) and measurement error (lagged $W$).

2. **Gravity-predicted networks.** Construct $W$ not from observed trade but from the predicted values of a gravity model (distance, common language, colonial ties, shared trade agreements). The predicted trade matrix captures structural determinants of linkages — geography, history, institutions — while purging the contemporaneous endogeneity. This is the spatial analog of using fitted values from a first stage as instruments. Frankel and Romer (1999) pioneered this approach in the trade-and-growth literature, and it translates directly to the spatial context. The first stage regresses bilateral trade on geographic and historical variables; the predicted values form the $W$ matrix used in the second-stage spatial regression. The exclusion restriction is that geographic and historical variables affect regional outcomes only through the trade channel — a strong but testable assumption.

3. **Geographic networks with economic interpretation.** Use contiguity or inverse distance as $W$, accepting the loss of economic specificity in exchange for exogeneity. Geography does not change in response to outcomes — the English Channel's width is not a function of UK-France GDP growth. The cost is that geographic proximity is an imperfect proxy for economic integration: regions that are physically close but economically disconnected (North and South Korea, for example) are treated as neighbors. The analyst must judge whether the economic question at hand — trade spillovers? technology diffusion? labor mobility? — is well proxied by geographic distance.

The choice among these strategies depends on the research question. For descriptive analysis ("do outcomes cluster spatially?"), geographic $W$ is sufficient. For policy evaluation ("does trade integration transmit growth shocks?"), economic $W$ with careful attention to endogeneity is necessary. The regional labs in this book use both approaches and compare results — an informative sensitivity exercise that the student should adopt as standard practice.

---

## 3A.5 From Correlation to Causation in Spatial Settings

The parametric spatial models of Sections 3A.2–3A.4 are powerful tools for characterizing spatial dependence, but they are, fundamentally, models of correlation structure. A large $\rho$ tells you that outcomes co-move across space in a pattern consistent with spillovers, but it does not, by itself, establish that one region's growth *causes* another's. This section introduces three design-based methods that pursue causal identification more directly. Each corresponds to an Applied Lab in the regional chapters.

### Spatial Regression Discontinuity Design (Lab 4: Europe)

The most compelling spatial identification strategies exploit discontinuities — sharp changes in treatment at boundaries that are otherwise smooth. The intuition is familiar from the standard RDD literature (Imbens and Lemieux, 2008): if a policy changes discretely at a threshold, units just above and just below the threshold are nearly identical in all respects except the treatment, and the difference in outcomes can be attributed to the policy.

In the spatial version, the "threshold" is typically a geographic boundary. Lab 4 (Europe) exploits the EU Cohesion Policy eligibility boundary: NUTS-2 regions with GDP per capita below 75 percent of the EU average qualify for substantially higher Structural Fund transfers. Regions at 74 percent and 76 percent of the EU average are, in expectation, similar in terms of industrial structure, human capital, geography, and institutional quality. The sharp eligibility cutoff creates a natural experiment.

The estimation proceeds in several steps:

1. **Define the running variable.** In Lab 4, this is the ratio of regional GDP per capita to the EU average, centered at the 75 percent threshold.

2. **Estimate the discontinuity.** Regress the outcome (post-treatment GDP growth) on a polynomial in the running variable, allowing the intercept to jump at the threshold. The jump is the estimated treatment effect.

3. **Check for manipulation.** If regions can strategically position themselves just below the threshold (by underreporting GDP, say), the design is invalid. The McCrary (2008) density test checks for a suspicious bunching of observations just below the cutoff.

4. **Bandwidth selection.** The estimates are local — they apply only to regions near the threshold. Optimal bandwidth selection (Imbens and Kalyanaraman, 2012) trades off bias (wider bandwidths introduce regions that are less comparable) against variance (narrower bandwidths use fewer observations).

**The spatial dimension.** Unlike a standard RDD — where the running variable is a scalar (test score, income threshold, age) — the spatial RDD has a geographic component. Regions near the threshold are not just numerically close to the cutoff; they are physically close to each other, often sharing borders. This creates both an opportunity and a complication.

The opportunity is that the analyst can exploit the geographic dimension directly: compare regions on opposite sides of the eligibility boundary that are also physically adjacent. If two neighboring NUTS-2 regions straddle the 75 percent threshold — one eligible, one ineligible — and they share a labor market, climate, and cultural characteristics, the comparison is especially compelling. Becker, Egger, and von Ehrlich (2010) use this approach to estimate the effect of EU Structural Funds on regional growth, finding positive but modest effects.

The complication is the spatial spillover problem. If Cohesion Fund transfers to a region at 74 percent of the EU average also benefit its neighbor at 76 percent — through increased demand, shared infrastructure, or cross-border labor mobility — then the estimated treatment effect is attenuated, because the "control" group has been partially treated. Lab 4 addresses this in two ways: first, by testing for discontinuities in treatment spillovers at the boundary using a "donut" specification that excludes regions within a bandwidth of the cutoff; and second, by explicitly modeling the spatial lag of treatment intensity as an additional variable.

**Practical guidance for students.** The spatial RDD requires attention to several details that the textbook version elides:

- *Bandwidth selection* must balance bias and variance. Too narrow a bandwidth yields noisy estimates with few observations; too wide a bandwidth includes regions that are no longer comparable. Lab 4 uses the Imbens-Kalyanaraman (2012) optimal bandwidth as the baseline, with half and double bandwidths as robustness checks.

- *The functional form* of the relationship between the running variable and the outcome matters. Linear, quadratic, and local-linear specifications can give different results. The standard practice is to report all three and check whether the estimated discontinuity is stable.

- *Manipulation testing* is critical. If regions (or more precisely, the statistical agencies that measure their GDP) can influence their position relative to the threshold, the design is invalid. Lab 4 implements the McCrary (2008) density test as a validity check.

### The Synthetic Control Method (Lab 5: MENA)

When the treatment is a rare, large event — a civil war, an oil price shock, the imposition of sanctions — there is no threshold to exploit and no comparison group that arises naturally. The Synthetic Control Method (Abadie, Hesterberg, and Diamond, 2010) constructs a counterfactual by finding a weighted combination of untreated "donor" regions that best matches the treated region's pre-treatment trajectory.

The logic is straightforward:

1. **Define the treated unit and the event.** Lab 5 examines the GDP trajectory of Syria, Libya, and Yemen following the onset of major conflict (2011–2018).

2. **Select a donor pool.** The donors are countries that did not experience the treatment — in this case, MENA and comparator countries that avoided civil war during the study period.

3. **Find optimal weights.** Choose weights $w_1, w_2, \ldots, w_J$ (summing to 1, nonnegative) for the $J$ donor countries such that the weighted combination matches the treated country's pre-treatment outcomes and predictors as closely as possible.

4. **Estimate the treatment effect.** The post-treatment gap between the treated country's actual trajectory and the synthetic control's trajectory is the estimated effect of conflict.

5. **Conduct placebo tests.** Apply the same procedure to each donor country in turn, pretending it was treated. If the treated country's gap is large relative to the distribution of placebo gaps, the effect is statistically significant — a spatial permutation inference that does not require parametric assumptions.

The SCM's great strength is transparency: the analyst can inspect the synthetic control's composition and evaluate whether the match is economically sensible. If the synthetic control for Syria is a weighted average of Jordan (0.3), Tunisia (0.25), Egypt (0.2), and Morocco (0.25), the analyst can judge whether this combination plausibly represents "what Syria would have looked like without civil war" — something that a regression coefficient does not permit.

Its limitations are equally clear:

- *Pre-treatment fit.* The method requires a long, stable pre-treatment period to establish the credibility of the match. If the synthetic control tracks the treated country poorly before the event, there is no reason to trust the post-event gap as a treatment effect. Lab 5 reports pre-treatment RMSPE (root mean squared prediction error) as a fit diagnostic.

- *Donor pool selection.* The donors must be genuinely unaffected by the treatment. If Syria's civil war caused refugee inflows that depressed Jordanian GDP, then Jordan is a contaminated donor. Lab 5 addresses this by sensitivity-testing the exclusion of neighboring countries from the donor pool.

- *Inference by permutation.* The SCM does not produce standard errors in the conventional sense. Instead, inference relies on placebo tests: the procedure is applied to each donor country in turn, as if it were the treated unit. The treated country's post-treatment gap is then ranked against the distribution of placebo gaps. If the treated gap is larger than all (or nearly all) placebo gaps, the effect is "significant" in a nonparametric sense. Lab 5 implements both in-space placebos (alternative treated countries) and in-time placebos (alternative treatment dates) — the former test whether the effect is specific to the treated country, the latter whether it is specific to the treatment date.

The SCM is particularly well-suited to the MENA context because the region features rare, large, heterogeneous shocks — civil wars, revolutions, sanctions regimes — that affect individual countries but not the entire region simultaneously. This is exactly the setting where the SCM's ability to construct country-specific counterfactuals outperforms panel regressions that impose homogeneous treatment effects.

### Difference-in-Differences with Spatial Spillovers

The classic difference-in-differences (DiD) design compares the change in outcomes for treated units against the change for control units, under the assumption that both groups would have followed parallel trends absent the treatment. In spatial settings, the parallel-trends assumption is complicated by the possibility that treatment effects spill over from treated to control regions — what Delgado and Florax (2015) call "interference."

If the treated region's policy change affects neighboring (control) regions — through trade diversion, migration, or competitive effects — then the control group is contaminated, and the estimated treatment effect is biased toward zero (if spillovers benefit the control group) or away from zero (if spillovers harm them). Three approaches address this:

1. **Buffer zones.** Exclude control regions within a specified distance of the treated region, creating a spatial "donut" that reduces contamination at the cost of sample size.

2. **Spatial lag of treatment.** Include the spatially lagged treatment variable $Wd$ (where $d$ is the treatment indicator) as an additional regressor. The coefficient on $Wd$ estimates the average spillover effect on neighboring regions.

3. **Ring-based heterogeneity.** Estimate separate treatment effects for regions at different distances from the boundary of the treated area. This reveals the spatial decay of the treatment effect and helps identify the range of spillovers.

These extensions connect directly to Lab 6 (Africa), where the two-step estimation — raw Moran's $I$ followed by governance-residualized Moran's $I$ — is conceptually similar to a DiD logic: the "treatment" is governance quality, and the question is whether spatial autocorrelation in economic activity persists after conditioning on the institutional environment.

### A Hierarchy of Evidence

The methods in this section are not substitutes for the parametric models of Sections 3A.2–3A.4 — they complement them. A useful heuristic organizes spatial evidence into a hierarchy of increasing credibility:

1. **Descriptive spatial association.** Moran's $I$, spatial autocorrelation maps, and hot-spot analysis establish that outcomes cluster geographically. This is where Lab 6 begins — and where much applied work unfortunately stops.

2. **Conditional spatial association.** SAR, SEM, and SDM models test whether the spatial pattern persists after conditioning on covariates and whether it is in the outcome variable, the errors, or both. Lab 1 operates at this level.

3. **Network-based decomposition.** MRIO analysis and convergence regressions decompose aggregate outcomes into bilateral flows and structural linkages, testing whether economic integration drives convergence. Lab 2 operates here.

4. **Quasi-experimental identification.** Spatial RDD, SCM, and spatial DiD exploit discontinuities, rare events, or institutional variation to identify causal effects. Labs 4 and 5 reach this level.

No single study should be expected to climb the entire hierarchy. But a book about regional economics should — and the progression across the five labs is designed to take the reader from descriptive evidence to causal identification, building skills incrementally.

---

## 3A.6 Spatial Panels: Combining Space and Time

Most real-world regional datasets have both a cross-sectional dimension ($n$ regions) and a time dimension ($T$ periods). The spatial panel extends the cross-sectional models of Section 3A.2 to this setting:

$$
y_{it} = \rho W y_{it} + x_{it}'\beta + \mu_i + \gamma_t + \varepsilon_{it}
$$

where $\mu_i$ are region fixed effects (absorbing all time-invariant heterogeneity — geography, climate, deep institutional characteristics) and $\gamma_t$ are time fixed effects (absorbing common shocks — global recessions, commodity price cycles, pandemic effects).

The inclusion of region fixed effects fundamentally changes the identification. In the cross-sectional SAR, $\rho$ is identified from the spatial pattern of outcomes at a point in time: do high-growth regions have high-growth neighbors? In the spatial panel with fixed effects, $\rho$ is identified from the *within-region temporal variation* in outcomes and its correlation with contemporaneous neighbor shocks: when a region's neighbors experience an unusually good year, does the focal region also do unusually well, beyond its own trend?

This is a much more demanding test of spatial spillovers, and estimates of $\rho$ in spatial panels are typically smaller than in cross sections — often by half or more. The reduction reflects the elimination of correlated effects (shared geography, shared institutions) that inflate $\rho$ in cross-sectional specifications. Panel estimates are more credible precisely because they are smaller.

**Estimation.** Spatial panel ML estimation requires computing the log-determinant $\ln|I_T \otimes (I_n - \rho W)|$ = $T \cdot \ln|I_n - \rho W|$, which is computationally feasible when $n$ is moderate. For large $n$, GMM approaches (Kapoor, Kelejian, and Prucha, 2007) avoid the determinant computation. Lee and Yu (2010) address the incidental-parameters bias that arises when $T$ is small relative to $n$ — the spatial equivalent of the Nickell bias in dynamic panel models.

**Dynamic spatial panels.** When outcomes are persistent over time — regional GDP growth exhibits year-to-year momentum — the model may include a temporal lag:

$$
y_{it} = \tau y_{i,t-1} + \rho W y_{it} + x_{it}'\beta + \mu_i + \gamma_t + \varepsilon_{it}
$$

The coefficient $\tau$ captures temporal persistence (how much of this year's growth is predicted by last year's). (Note: $\tau$ denotes the temporal autoregressive parameter here; Chapter 1 uses $\tau$ for iceberg transport costs in the NEG model.) and $\rho$ captures contemporaneous spatial spillovers. The interaction between the two is important: if $\tau$ is large and $\rho$ is moderate, a local shock first propagates to neighbors (the spatial channel) and then persists in both the origin and destination regions (the temporal channel), generating long-lived spatial clusters from one-time innovations. This is the econometric expression of the lock-in dynamics that Chapter 2 described theoretically.

Lab 2 (Asia) uses panel convergence specifications that relate initial income to subsequent growth rates across countries and time periods, with spatial lags capturing whether convergence is influenced by neighbors' performance — a spatial $\beta$-convergence test.

---

## 3A.7 Data Sources and Reproducible Workflows

### The Landscape of Spatial Economic Data

Every Applied Lab in this book draws on publicly accessible datasets. The following survey orients the reader to the major sources and their characteristics. Full access instructions and variable definitions are documented in Appendix B and in each lab's README.

**Cross-country macroeconomic panels.**
The World Bank's World Development Indicators (WDI) provide GDP, GDP per capita, trade openness, manufacturing value added, governance scores, and hundreds of other variables for 217 economies at annual frequency. The Penn World Table (PWT) offers PPP-adjusted GDP, capital stocks, and total factor productivity. These are the backbone of Labs 1 (Americas) and 5 (MENA).

**Bilateral trade and input-output tables.**
The UN Comtrade database provides bilateral merchandise trade flows at the HS commodity level. The World Input-Output Database (WIOD) provides multi-region input-output tables linking 43 countries and 56 industries. The OECD's Trade in Value Added (TiVA) database decomposes gross exports into domestic and foreign value-added components — and critically, TiVA captures the "servicification" of manufacturing: the service content (design, logistics, marketing, finance) embedded in goods exports. Lab 1 uses Comtrade for $W$ construction; Lab 2 (Asia) uses WIOD and TiVA for network analysis, convergence estimation, and a servicification decomposition exercise.

**Services trade data and regulatory barriers.**
Services trade is measured through several complementary frameworks, each capturing a different dimension. The WTO's BOP-based services trade statistics record cross-border (Mode 1) and travel-related (Mode 2) trade, but miss commercial presence (Mode 3 — the largest channel for many service sectors). The OECD Services Trade Restrictiveness Index (STRI) quantifies regulatory barriers to services trade across 22 sectors and 50+ countries, providing the key regressor for gravity models of services trade (Kimura & Lee 2006; Head, Mayer & Ries 2009). The World Bank's parallel STRI database extends coverage to developing economies (Borchert, Gootiiz & Mattoo 2014). The ECIPE Digital Trade Estimates database maps data localization laws and digital services taxes — the regulatory infrastructure of the "splinternet." Lab 7 (Services) uses these sources to estimate the tariff-equivalent cost of regulatory barriers and to map the geography of cloud infrastructure against data sovereignty regimes. A persistent measurement challenge: BOP data systematically undercount services trade because Mode 3 (where a firm establishes a local subsidiary to deliver services) appears as FDI rather than trade. Students should internalize that total services trade may be 50–70 percent larger than BOP data indicate once Mode 3 activity is included (see Chapter 3-B, Section 3B.2).

**Subnational regional data.**
Eurostat provides GDP, population, and employment at the NUTS-2 and NUTS-3 levels for EU member states, with shapefiles for spatial analysis. This is the primary dataset for Lab 4 (Europe). For non-European subnational analysis, the Global Data Lab's Subnational Human Development Index and the OECD Regional Statistics database offer comparable coverage.

**Conflict and displacement data.**
The Armed Conflict Location and Event Data Project (ACLED) provides geocoded conflict events for the Middle East, Africa, and South/Southeast Asia. The UNHCR Refugee Data Finder provides displacement statistics. Lab 5 (MENA) combines these with WDI macroeconomic data to build estimation panels for synthetic control analysis.

**Remote sensing and alternative measurement.**
NASA's VIIRS (Visible Infrared Imaging Radiometer Suite) provides nighttime light intensity at approximately 750-meter resolution. Night-lights are a widely used proxy for economic activity in regions where official GDP statistics are unreliable, sparse, or delayed — a use case established by Henderson, Storeygard, and Weil (2012). Lab 6 (Africa) uses VIIRS composites as the primary outcome measure.

**Survey data.**
Afrobarometer provides standardized public opinion surveys covering governance perceptions, service delivery satisfaction, and institutional trust across 30+ African countries. Lab 6 uses the trust-in-local-government measure as a governance control.

**Geospatial boundary data.**
Shapefiles defining regional boundaries are the connective tissue of spatial analysis — without them, no $W$ matrix can be constructed. Key sources include Eurostat GISCO (NUTS boundaries for Europe), the GADM database (global administrative boundaries at multiple levels), Natural Earth (country boundaries and coastlines), and the OECD FUA boundary files (functional urban areas). Boundary data must be version-controlled carefully: NUTS revisions occur every three years, and a mismatch between boundary vintage and economic data vintage produces spurious results — a region that was split between NUTS 2016 and NUTS 2021 will appear as two new entities, not as a continuation.

**Dataset quality gradients.** A recurrent theme across the labs is that data quality varies systematically with income and institutional capacity. European data (Eurostat) is harmonized, spatially granular (NUTS-3), and available annually since the 1990s. African data is sparse, often available only at the country level, with long lags between collection and publication — which is precisely why Lab 6 uses night-lights as an alternative activity measure. MENA data falls in between: WDI coverage is good for macro aggregates but thin for subnational indicators, and conflict disrupts statistical capacity (Syria has no reliable GDP figures after 2010). The analyst must match the method to the data reality, not the other way around. Using spatial RDD in a region where boundary-level data do not exist is an exercise in fantasy.

### Reproducibility Principles

Every lab in this book follows a common architecture designed for reproducibility:

1. **CLI-driven pipelines.** Each lab's code consists of standalone scripts invoked from the command line with explicit arguments. There are no notebooks that must be "run in order" — each script declares its inputs and outputs.

2. **Canonical variable names.** A JSON configuration file (`source_mappings.json`) in each lab maps raw variable names from external datasets to canonical names used throughout the analysis. This means the code works identically regardless of whether the WDI column is called `NY.GDP.MKTP.KD.ZG` or `gdp_growth`.

3. **Separation of data acquisition, preparation, and estimation.** Fetch scripts pull raw data. Preparation scripts map raw data to canonical formats. Estimation scripts operate on the canonical inputs. This modularity means that a data source can be replaced without touching the estimation code.

4. **Seeded randomization.** Every operation involving randomness (permutation inference in Lab 6, synthetic data generation in smoke tests) uses an explicit random seed for exact reproducibility.

5. **Smoke tests.** Each lab has at least one automated test that runs the full pipeline on synthetic or small-sample data and checks that outputs conform to expected schemas and statistical properties. These tests run in CI on every commit.

6. **Version-pinned dependencies.** A root `requirements.txt` pins all package versions to ensure that results are reproducible across machines and over time. The spatial analysis ecosystem — particularly `scipy`, `numpy`, and the various spatial libraries — can produce subtly different results across versions due to changes in numerical precision, default algorithm selection, or optimization routines. Pinning prevents the unpleasant experience of a result that "worked on my machine" but fails to replicate.

### The Temptation of Point-and-Click and Why We Resist It

GIS software (ArcGIS, QGIS) and statistical packages (GeoDa, Stata's `sppack`) make spatial analysis accessible with graphical interfaces. These tools are valuable for visualization and exploration, but they pose a reproducibility risk: the sequence of clicks, menu selections, and parameter choices that produced a result is not recorded in a way that can be audited or replicated. A script-based workflow — even if it takes longer to write initially — produces a permanent, versionable record of every analytical decision.

The labs in this book use Python exclusively. This is a pragmatic choice, not an ideological one. R's spatial ecosystem (`spdep`, `spatialreg`, `sf`) is excellent and in some areas more mature. The principle — scripted, reproducible, CLI-driven — is language-agnostic. Students who prefer R can translate the lab code without changing the analytical logic.

---

## 3A.8 Conclusion: Tools in Service of Questions

The methods in this chapter are not an end in themselves. They are instruments for answering the questions that Chapters 1 and 2 posed: Where does economic activity concentrate, and why? How do institutions condition the spatial distribution of growth? What happens when shocks propagate through networks of economically connected regions? Chapter 3-B complements these spatial tools with the gravity model and trade measurement framework that underpins the services trade analysis woven through the regional chapters.

The spatial weight matrix encodes a hypothesis about how regions interact. The SAR, SEM, and SDM family allows that hypothesis to be tested against data. Impact decomposition reveals whether the effects of covariates are primarily local or primarily networked. And the design-based methods — RDD, synthetic control, and DiD with spatial spillovers — push the analysis from "spatial patterns exist" to "spatial patterns are causally informative."

Two principles should guide applied work throughout the regional chapters that follow:

**First, report what you assume.** Every $W$ matrix is a hypothesis. Every identification strategy has an assumption about what varies exogenously and what does not. The reader deserves to see these assumptions stated explicitly and tested when possible.

**Second, let sensitivity be informative.** If a result is robust to the choice of $W$, to the specification (SAR vs. SDM), and to the identification strategy (parametric vs. design-based), the claim is strong. If it is fragile — if the sign of $\rho$ flips when trade weights replace contiguity weights, or if the RDD estimate disappears with a different bandwidth — that fragility is itself a finding. It tells you that the spatial channel is poorly identified or that the mechanism operates differently from what the model assumes.

The regional chapters will use every tool introduced here:

- **Lab 1 (Americas):** SAR with trade-weighted $W$ and institution-interaction terms. The analysis demonstrates that spatial spillovers in the Western Hemisphere are conditional on institutional quality — a direct test of whether the NEG's agglomeration mechanisms require institutional preconditions.

- **Lab 2 (Asia):** Network measures derived from input-output tables and $\beta$-convergence estimation with spatial lags. The analysis tests whether Asian economic integration — measured through value-added linkages rather than gross trade — drives income convergence across the region.

- **Lab 4 (Europe):** Spatial RDD at the EU Cohesion Policy eligibility boundary. The analysis exploits the 75 percent GDP-per-capita threshold to estimate the causal effect of Structural Fund transfers on regional growth, with explicit attention to cross-boundary spillovers.

- **Lab 5 (MENA):** Synthetic control method with permutation-based inference. The analysis constructs counterfactual GDP trajectories for conflict-affected countries and estimates the economic cost of civil war — a quantity that standard panel regressions cannot credibly identify when the treatment is rare, large, and heterogeneous.

- **Lab 6 (Africa):** Moran's $I$ — the oldest and simplest spatial diagnostic — applied to night-lights data as an alternative activity measure. The two-step procedure (raw spatial autocorrelation, then governance-residualized) tests whether economic clustering in Sub-Saharan Africa is driven by institutional geography or by physical geography.

The progression is deliberate: we begin with correlation (Labs 1, 2, 6), move to quasi-experimental designs (Labs 4, 5), and ask at every stage whether the spatial pattern reflects a causal mechanism or a statistical artifact. By the end, the student should be able to read a spatial econometric paper critically — knowing what to check, what to doubt, and what to believe.

---

## Data in Depth: Sensitivity of Spatial Estimates to Weight-Matrix Specification

**Setting.** Consider NUTS-2 regional GDP growth across 280 EU regions for a single cross-section. We estimate a SAR, SEM, and SDM under three $W$ specifications: (1) queen contiguity, (2) inverse-distance with a 500 km cutoff, and (3) k-nearest-neighbors with $k = 6$.

**Protocol.** For each $W$, we first run OLS and compute Anselin's LM tests. We then estimate the SAR, SEM, and SDM by maximum likelihood and report direct, indirect, and total effects for the key covariate (log initial GDP per capita, which measures convergence).

**Typical findings.** The results form a pattern worth studying in detail:

| | Contiguity $W$ | Inv-Distance $W$ | $k$-NN ($k=6$) $W$ |
|---|---|---|---|
| OLS $\beta$ (initial income) | $-0.018$ | $-0.018$ | $-0.018$ |
| LM-lag $p$-value | 0.03 | $<0.001$ | 0.01 |
| LM-error $p$-value | 0.08 | 0.002 | 0.04 |
| SAR $\rho$ | 0.18 | 0.31 | 0.24 |
| SAR direct effect | $-0.016$ | $-0.015$ | $-0.016$ |
| SAR indirect effect | $-0.003$ | $-0.008$ | $-0.005$ |
| SDM direct effect | $-0.017$ | $-0.016$ | $-0.017$ |
| SDM indirect effect | $-0.005$ | $-0.011$ | $-0.007$ |

Several patterns emerge. First, the OLS estimate of $\beta$ is identical across specifications because OLS ignores $W$. Second, the LM tests consistently reject the null of no spatial dependence, more strongly for the distance-based $W$ (which captures more connections) than for contiguity. Third, $\rho$ varies substantially across $W$ specifications — from 0.18 (contiguity) to 0.31 (distance) — reflecting the different network densities. Fourth, and most importantly, the direct effect of initial income on growth is stable across all specifications ($-0.015$ to $-0.017$), while the indirect effect varies by a factor of three.

**Interpretation.** The direct-effect stability is reassuring: the convergence finding is not an artifact of $W$ choice. The indirect-effect sensitivity is informative: it tells us that the *channel* through which spatial dependence operates — physical adjacency vs. economic proximity — matters for the magnitude of the spillover, even when the existence of the spillover is not in doubt. The inverse-distance $W$ produces the largest indirect effect because it connects each region to a broader set of neighbors, amplifying the network multiplier.

**What this means for policy.** If the distance-based specification is correct, a 1 percent increase in initial income across all EU regions produces roughly 0.016 percentage points of own-region growth adjustment plus 0.011 percentage points of neighbor-driven adjustment — a spatial multiplier of about 1.7. Under the contiguity specification, the multiplier is only about 1.2. The "true" multiplier depends on which channel dominates: physical proximity (shared labor markets, cross-border commuting) or broader economic linkages (trade, investment, knowledge flows). Both are plausible in the European context, and the range of estimates (1.2 to 1.7) is itself useful for policy calibration.

**Takeaway for students.** Always report results under at least two $W$ specifications. If your headline finding survives, you have a robust result. If it does not, you have learned something important about the mechanism. The table above shows the right way to present a sensitivity audit — not as an afterthought in a footnote, but as a central piece of evidence that disciplines the interpretation.

---

## Institutional Spotlight: Eurostat GISCO and the Infrastructure of Spatial Comparison

Every regression in this chapter depends on a prior decision: where do regions begin and end? In Europe, this question is answered by the NUTS classification (Nomenclature of Territorial Units for Statistics), maintained by Eurostat and updated approximately every three years. The current version, NUTS 2024, defines 104 NUTS-1 regions, 283 NUTS-2 regions, and 1,348 NUTS-3 regions across the EU.

The NUTS system is a compromise between administrative convenience and analytical coherence. NUTS-2 regions — the level used in most EU regional policy — correspond to provinces, counties, or *Regierungsbezirke* depending on the country. They were designed for policy administration, not for economic analysis, and the mismatch shows: the Paris NUTS-2 region (Île-de-France) has 12 million inhabitants, while the smallest NUTS-2 regions in Greece or Portugal have fewer than 300,000. Cross-regional comparisons are only as valid as the implicit assumption that these units represent comparable economic entities.

Eurostat's GISCO (Geographic Information System of the Commission) unit produces the shapefiles, boundary data, and geocoding standards that make spatial analysis of European regional data possible. GISCO ensures that boundary changes between NUTS revisions are documented and that time series can be backcasted across revisions — a critical service, since NUTS-2 boundaries have changed substantially since the classification was introduced in 1988. Without GISCO's harmonization infrastructure, any panel analysis of European regional data would be contaminated by spurious boundary changes.

The practical implications are substantial. Researchers working with NUTS-2 data must specify which vintage of the classification they are using. A study of regional convergence over 2000–2020 that uses NUTS 2021 boundaries may find different results than one that uses NUTS 2013 boundaries, because the boundaries themselves changed — regions were split, merged, or reclassified. GISCO provides concordance tables that map old regions to new ones, but the mapping is sometimes one-to-many (a split) or many-to-one (a merger), requiring interpolation. These technical details are rarely mentioned in published papers, but they can affect results — particularly for spatial panel models where the consistency of the $W$ matrix over time depends on boundary stability.

Outside Europe, the situation is more challenging. Many African and Asian countries have no equivalent of the NUTS system — subnational boundaries are defined by national authorities without international harmonization. The GADM database provides the best available global coverage, but GADM boundaries do not always align with the administrative units for which economic data are collected. The Global Data Lab's Subnational HDI, which covers 1,700+ regions in 170 countries, represents a major harmonization effort, but its spatial resolution is coarse compared to NUTS-2.

The lesson for spatial analysts is that the "raw data" in regional economics is never raw. It arrives shaped by the institutional choices of statistical agencies — choices about boundary placement, geocoding precision, variable definitions, and harmonization protocols. These choices constrain what spatial methods can detect and what they cannot. A weight matrix built on NUTS-2 boundaries captures a specific institutional geography, not a natural one. The analyst who forgets this is modeling the classification system as much as the economy.

---

## Discussion Questions

1. You are studying the effect of a new high-speed rail line on regional GDP growth in Spain. How would you construct the spatial weight matrix — contiguity, distance, or travel-time-based? What are the identification assumptions, and how would the estimated spillover effect differ across specifications?

2. A colleague estimates a SAR model of housing prices across US metropolitan areas and finds $\rho = 0.85$. They conclude that "housing markets are strongly spatially interdependent." What alternative explanations could produce a large $\hat{\rho}$ even in the absence of genuine spatial spillovers? How would you distinguish between the alternatives?

3. The LeSage-Pace impact decomposition shows that indirect effects in a SAR can exceed direct effects when $\rho$ is large. Under what economic conditions would you expect indirect effects to dominate — and what would this imply for the design of place-based economic policy?

4. Manski's reflection problem states that endogenous, exogenous, and correlated effects cannot be simultaneously identified without exclusion restrictions. Describe a concrete spatial setting (e.g., innovation diffusion across cities, or trade policy coordination among neighboring countries) and propose an exclusion restriction that would allow identification of the endogenous effect. What are the limits of your proposed restriction?

5. Lab 4 uses a spatial RDD to estimate the effect of EU Cohesion Policy. The identification assumption is that regions just above and just below the 75 percent GDP-per-capita threshold are comparable. Name two threats to this assumption and describe how you would test for them. How would you handle the possibility that Cohesion Fund spending in treated regions spills over to benefit their untreated neighbors?
