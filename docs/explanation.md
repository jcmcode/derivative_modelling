# Breeden-Litzenberger Model: Complete Mathematical Walkthrough

## Table of Contents

1. [Introduction and Motivation](#1-introduction-and-motivation)
2. [Theoretical Foundations: Arrow-Debreu Securities and State Prices](#2-theoretical-foundations-arrow-debreu-securities-and-state-prices)
3. [The Breeden-Litzenberger Theorem](#3-the-breeden-litzenberger-theorem)
4. [Risk-Neutral Pricing and the Risk-Neutral Measure](#4-risk-neutral-pricing-and-the-risk-neutral-measure)
5. [The Black-Scholes Framework](#5-the-black-scholes-framework)
6. [From Implied Volatilities to the Risk-Neutral Density](#6-from-implied-volatilities-to-the-risk-neutral-density)
7. [The Malz (2014) Cookbook Procedure](#7-the-malz-2014-cookbook-procedure)
8. [No-Arbitrage Conditions and Diagnostics](#8-no-arbitrage-conditions-and-diagnostics)
9. [Interpretation: What the Market Is Telling Us](#9-interpretation-what-the-market-is-telling-us)
10. [Implementation Details](#10-implementation-details)
11. [References](#11-references)

---

## 1. Introduction and Motivation

Option prices contain a wealth of information. When a trader pays a premium for a put option struck 20% below the current price, they are effectively placing a bet on a large market decline. Aggregated across all market participants, the full set of option prices across different strikes and expiries encodes the market's collective forward-looking view of where the underlying asset might end up — and, crucially, how much probability the market assigns to extreme moves.

The **Breeden-Litzenberger (1978)** method provides a model-free way to extract this forward-looking probability distribution — called the **risk-neutral probability distribution (RND)** — directly from observed option prices. The only assumption needed is that option markets are free of arbitrage.

### Why This Matters

The standard Black-Scholes model assumes that log returns are normally distributed (equivalently, that the future price is lognormally distributed). This implies a symmetric, thin-tailed distribution. In reality:

- Markets crash more often and more severely than lognormal models predict
- The volatility "smile" or "skew" observed in option markets is direct evidence that the market disagrees with Black-Scholes
- The market-implied distribution is typically **left-skewed** (heavier left tail) and **leptokurtic** (fatter tails than normal)

By extracting the RND from market prices, we can quantify these deviations and measure the market's true assessment of tail risk.

---

## 2. Theoretical Foundations: Arrow-Debreu Securities and State Prices

### The Arrow-Debreu Framework

Consider a simplified economy with a finite set of possible future states of the world, indexed by $i = 1, 2, \ldots, N$. An **Arrow-Debreu security** (or elementary contingent claim) for state $i$ is a contract that pays exactly \$1 if state $i$ occurs and \$0 otherwise.

If we denote the price of the Arrow-Debreu security for state $i$ as $\pi_i$, then the price of *any* security with known state-contingent payoffs $X_i$ is simply:

$$V = \sum_{i=1}^{N} \pi_i \cdot X_i$$

This is a direct consequence of no-arbitrage: if the law of one price holds and markets are complete, the price of any derivative is uniquely determined by state prices.

### State Prices vs Probabilities

State prices $\pi_i$ are *not* probabilities, but they are closely related. We can decompose each state price into three components:

$$\pi_i = e^{-rT} \cdot Q_i \cdot \frac{P_i}{Q_i}$$

where:
- $e^{-rT}$ is the time discount factor (risk-free rate $r$, time horizon $T$)
- $Q_i$ is the actual (physical) probability of state $i$
- $P_i / Q_i$ is the **pricing kernel** (or stochastic discount factor) — the ratio of state price to probability, reflecting risk preferences

The **risk-neutral probability** is defined as:

$$\tilde{P}_i = e^{rT} \cdot \pi_i$$

Under risk-neutral probabilities, the price of any security equals its expected payoff discounted at the risk-free rate:

$$V = e^{-rT} \sum_{i=1}^{N} \tilde{P}_i \cdot X_i = e^{-rT} \, \tilde{E}[X]$$

### The Pricing Kernel

The pricing kernel $m_i = \pi_i / Q_i$ captures the market's risk preferences. In the simple two-state example from Jackwerth (2004):

| State | Stock Price | Actual Prob $Q_i$ | State Price $\pi_i$ | Pricing Kernel $m_i$ |
|-------|------------|-------------------|---------------------|---------------------|
| Up    | 1.2214     | 0.90              | 0.6350              | 0.706               |
| Down  | 0.8187     | 0.10              | 0.2741              | 2.741               |

The pricing kernel is **decreasing in wealth** — the poorer the investor (down state), the higher the marginal value placed on an additional dollar. This is the economic content of risk aversion: states where wealth is low are valued disproportionately more than their probability alone would suggest.

### From Discrete to Continuous

In a continuous setting, the state price *density* replaces the discrete state prices. If $S_T$ is the future price of the underlying asset, the state price density $p(S_T)$ is defined such that $p(S_T) \, dS_T$ is the price today of receiving \$1 if the future price falls in the interval $[S_T, S_T + dS_T]$.

The risk-neutral probability density is:

$$\tilde{\pi}(S_T) = e^{rT} \cdot p(S_T)$$

---

## 3. The Breeden-Litzenberger Theorem

### Setup

Consider a European call option on an asset with current price $S_0$, struck at $X$, expiring at time $T$. Its payoff is $\max(S_T - X, 0)$. Under the risk-neutral measure, its price is:

$$c(X) = e^{-rT} \int_X^{\infty} (s - X) \, \tilde{\pi}(s) \, ds$$

### The First Derivative: Exercise-Price Delta

Differentiating with respect to the strike price $X$ (using Leibniz's rule):

$$\frac{\partial c}{\partial X} = e^{-rT} \left[ \int_0^X \tilde{\pi}(s) \, ds - 1 \right]$$

This is the **exercise-price delta** — the sensitivity of the call price to changes in the strike. Note this is *different* from the standard Black-Scholes delta (sensitivity to the spot price). The exercise-price delta is always negative (higher strike means lower call value) and bounded between $-e^{-rT}$ and $0$.

Rearranging gives the **risk-neutral CDF**:

$$\boxed{\tilde{\Pi}(X) \equiv \int_0^X \tilde{\pi}(s) \, ds = 1 + e^{rT} \frac{\partial c}{\partial X}}$$

**Interpretation:** The probability that $S_T \leq X$ under the risk-neutral measure equals one plus the future value of the exercise-price delta. This is Malz (2014), Equation (2).

### The Second Derivative: The Core Result

Differentiating once more:

$$\boxed{\tilde{\pi}(X) = e^{rT} \frac{\partial^2 c}{\partial X^2}}$$

**This is the Breeden-Litzenberger theorem.** The risk-neutral probability density at any price level $X$ is proportional to the second derivative of the call price with respect to strike, evaluated at that strike. This is Breeden & Litzenberger (1978), Equation (2); Malz (2014), Equation (3); and Jackwerth (2004), Equation (7).

### Intuition via the Butterfly Spread

The second derivative can be approximated by a **butterfly spread** — a portfolio of three call options:

$$\frac{\partial^2 c}{\partial X^2} \approx \frac{c(X + \Delta) + c(X - \Delta) - 2c(X)}{\Delta^2}$$

A butterfly spread centred at strike $X$ with width $\Delta$ pays off a triangular amount centred at $S_T = X$. As $\Delta \to 0$, this triangular payoff converges to a Dirac delta function — i.e., it pays off only when $S_T = X$. This is precisely an Arrow-Debreu security.

Therefore:

$$\text{State price density at } X = \lim_{\Delta \to 0} \frac{\text{Butterfly spread price centred at } X}{\Delta^2}$$

The cost of this infinitesimal butterfly, properly normalised, gives the market's assessment of the probability of the underlying ending at exactly $X$.

### Model-Free Nature

A remarkable feature of this result is that it requires **no assumptions about the dynamics of the underlying asset**. We do not need to specify:
- A stochastic process for $S_T$
- A utility function for investors
- Anything about market completeness

The only requirements are:
1. European call prices exist as a smooth function of the strike price
2. Markets are free of arbitrage (so the call price function is decreasing and convex in $X$)

---

## 4. Risk-Neutral Pricing and the Risk-Neutral Measure

### What "Risk-Neutral" Means

The risk-neutral distribution is **not** the market's best estimate of where the stock will actually end up. Instead, it is the distribution under which the price of every traded security equals the discounted expected payoff at the risk-free rate.

The relationship between risk-neutral probabilities $\tilde{P}$ and actual (physical) probabilities $Q$ is:

$$\tilde{P}(S_T) = Q(S_T) \cdot \frac{m(S_T)}{E^Q[m]}$$

where $m(S_T)$ is the pricing kernel. Since the pricing kernel is typically decreasing in $S_T$ (risk-averse investors value bad states more), risk-neutral probabilities overweight bad outcomes relative to actual probabilities. This is why:

- The risk-neutral distribution has a **fatter left tail** than the actual distribution
- The risk-neutral mean equals the forward price $F = S_0 e^{(r-q)T}$, which may differ from the expected future spot under physical probabilities

### The Fundamental Theorem of Asset Pricing

The existence of a risk-neutral measure is equivalent to no-arbitrage. More precisely:

> **First Fundamental Theorem:** A market admits no arbitrage if and only if there exists at least one probability measure $\tilde{P}$ equivalent to the physical measure $Q$ under which discounted asset prices are martingales.

> **Second Fundamental Theorem:** The market is complete (every contingent claim can be replicated) if and only if the risk-neutral measure is unique.

For the BL method, we only need the first theorem — that a risk-neutral density exists. The BL method then recovers it from market prices without assuming completeness.

### Connection to Breeden-Litzenberger (1978), Theorem 1

Breeden and Litzenberger showed that under two key assumptions:
- **(A1)** Each individual has a time-additive, state-independent utility function
- **(A2)** All individuals agree on conditional probabilities of states given aggregate consumption

Any unconstrained Pareto-optimal allocation is such that, at each date, all states with the same level of aggregate consumption have the same allocation. Furthermore, European call options on aggregate consumption are **sufficient** to span all Arrow-Debreu securities and achieve any Pareto-optimal allocation.

---

## 5. The Black-Scholes Framework

### The Black-Scholes Call Price

Under the Black-Scholes model, the underlying follows geometric Brownian motion:

$$dS = (r - q) S \, dt + \sigma S \, dW$$

where $r$ is the risk-free rate, $q$ is the continuous dividend yield, and $\sigma$ is the constant volatility. The European call price is:

$$c(S, X, T, r, q, \sigma) = S e^{-qT} \Phi(d_1) - X e^{-rT} \Phi(d_2)$$

where:

$$d_1 = \frac{\ln(S/X) + (r - q + \sigma^2/2)T}{\sigma\sqrt{T}}, \qquad d_2 = d_1 - \sigma\sqrt{T}$$

and $\Phi(\cdot)$ is the standard normal CDF.

### The Lognormal Distribution Under Black-Scholes

Under the risk-neutral measure in the Black-Scholes model:

$$\ln S_T \sim \mathcal{N}\!\left(\ln S_0 + (r - q - \tfrac{\sigma^2}{2})T, \;\; \sigma^2 T\right)$$

The risk-neutral density of $S_T$ is therefore lognormal:

$$\tilde{\pi}_{\text{BS}}(S_T) = \frac{1}{S_T \sigma \sqrt{2\pi T}} \exp\!\left(-\frac{\left[\ln S_T - \ln S_0 - (r - q - \sigma^2/2)T\right]^2}{2\sigma^2 T}\right)$$

One can verify that applying the Breeden-Litzenberger formula to the Black-Scholes call price recovers exactly this lognormal density. This was derived explicitly in Breeden & Litzenberger (1978), Equation (5).

### Implied Volatility and the Volatility Smile

In practice, the Black-Scholes model does *not* hold perfectly. If it did, the implied volatility would be the same for all strikes and expiries. Instead, we observe the **volatility smile** (or skew): implied volatility varies systematically with strike price.

For equity indices like the S&P 500 (post-1987):
- **Low-strike options** (OTM puts) trade at *higher* implied volatility — the market charges more for downside protection
- **High-strike options** (OTM calls) trade at *lower* implied volatility
- The smile is typically a downward-sloping "smirk"

This smile is the market's way of encoding a non-lognormal distribution into the Black-Scholes framework. By treating implied volatility as a function of strike — $\sigma(X)$ rather than a constant — and feeding it back through the BS formula, we can reconstruct the market's true (non-lognormal) pricing function.

### Inverting Black-Scholes: From Prices to Implied Vols

Given a market call price $c_{\text{mkt}}$, the implied volatility $\sigma_{\text{imp}}$ is the unique value of $\sigma$ that makes the Black-Scholes formula match:

$$c_{\text{BS}}(S, X, T, r, q, \sigma_{\text{imp}}) = c_{\text{mkt}}$$

This inversion is well-defined because the Black-Scholes price is strictly increasing in $\sigma$ (positive vega). We solve it numerically using **Brent's method**, which is guaranteed to converge for bracketed roots and requires no derivatives.

### OTM Convention for the Smile

We construct the smile using **out-of-the-money (OTM) options**:
- For $X < S_0$: use OTM puts (convert to call-equivalent IV via put-call parity)
- For $X \geq S_0$: use OTM calls

This is standard market practice because OTM options are more liquid, have tighter bid-ask spreads, and carry less model risk than their in-the-money counterparts.

---

## 6. From Implied Volatilities to the Risk-Neutral Density

### The Key Insight

Rather than differentiating market call prices directly (which are noisy and observed at discrete strikes), we:

1. **Interpolate** the implied volatility smile as a smooth function $\sigma(X)$
2. **Reconstruct** call prices on a fine grid: $c(X) = \text{BS}(S_0, X, T, r, q, \sigma(X))$
3. **Differentiate** the reconstructed call price function numerically

This two-step approach (smile interpolation then BS repricing) is the method advocated by Jackwerth (2004) and operationalised by Malz (2014). Its advantage is that implied volatilities vary much more slowly across strikes than call prices do, making interpolation far more stable.

### The Call Valuation Function

The **call valuation function** is defined as:

$$c(t, X, \tau) = v\!\left[S_t, X, \tau, \sigma(t, X, \tau), r_t, q_t\right]$$

where $v[\cdot]$ is the Black-Scholes formula and $\sigma(t, X, \tau)$ is the interpolated implied volatility at strike $X$. This function:

- Is defined for all $X > 0$, not just observed strikes
- Is smooth (at least $C^2$) by construction, enabling differentiation
- Agrees with observed market prices at the data points
- Satisfies no-arbitrage conditions when the interpolation is done correctly

---

## 7. The Malz (2014) Cookbook Procedure

### Step 1: Interpolate and Extrapolate the Volatility Smile

Given observed implied volatilities $\{(X_1, \sigma_1), \ldots, (X_n, \sigma_n)\}$ ordered by strike, fit a **clamped cubic spline** $f(X)$.

A cubic spline through $n$ knot points consists of $n - 1$ cubic polynomials, one on each interval $[X_i, X_{i+1}]$. The spline satisfies:
- **Interpolation:** $f(X_i) = \sigma_i$ for all $i$
- **Continuity:** $f$, $f'$, and $f''$ are continuous at all interior knots
- **Clamped boundary conditions:** $f'(X_1) = 0$ and $f'(X_n) = 0$

The **clamped** condition (zero first derivative at the boundaries) is crucial. It means the smile flattens out at the edges of the data, enabling natural flat extrapolation:

$$\sigma(X) = \begin{cases} \sigma_1 & \text{if } X < X_1 \\ f(X) & \text{if } X_1 \leq X \leq X_n \\ \sigma_n & \text{if } X > X_n \end{cases}$$

**Why clamped, not natural?** A natural cubic spline has $f''(X_1) = f''(X_n) = 0$ at the boundaries, which allows $f'$ to be nonzero there. When extrapolated beyond the data, a natural spline continues with its boundary slope, causing implied volatility to increase or decrease linearly. This eventually produces:
- Negative implied volatilities (nonsensical)
- Non-monotone call prices (arbitrage violation)
- Negative probability densities

The clamped spline avoids all of these problems by ensuring flat extrapolation.

### Step 2: Build the Call Valuation Function

For each point $X$ on a fine strike grid:

$$c(X) = S_0 e^{-qT} \Phi(d_1(X)) - X e^{-rT} \Phi(d_2(X))$$

where $d_1(X)$ and $d_2(X)$ use $\sigma = \sigma(X)$ from the interpolated smile. This gives us a smooth, arbitrage-consistent set of call prices on an arbitrarily fine grid.

### Step 3: Finite Differencing

We approximate the first and second derivatives of $c(X)$ using **central finite differences** with step size $\Delta$:

**Risk-neutral CDF:**

$$\tilde{\Pi}(X) \approx 1 + e^{rT} \cdot \frac{c(X + \Delta/2) - c(X - \Delta/2)}{\Delta}$$

**Risk-neutral PDF:**

$$\tilde{\pi}(X) \approx e^{rT} \cdot \frac{c(X + \Delta) + c(X - \Delta) - 2c(X)}{\Delta^2}$$

The second formula is immediately recognisable as the butterfly spread formula: the numerator is the cost of a butterfly spread centred at $X$ with wing width $\Delta$.

### The Step Size $\Delta$

The step size $\Delta$ is a **smoothing parameter** that trades off resolution against noise:

| $\Delta$ too small | $\Delta$ too large |
|---|---|
| High resolution | Low resolution |
| Captures fine structure | Smooths over features |
| Prone to negative densities | Always non-negative |
| Noisy | Over-smoothed |

Malz (2014) recommends $\Delta$ as a fraction of the forward price $F$:

$$\Delta = \alpha \cdot F, \qquad \text{typically } \alpha \approx 0.025$$

Our implementation uses $\alpha = 0.025$ (2.5% of the forward price) as the baseline, with a sensitivity analysis showing the effect of varying $\alpha$ from 0.01 to 0.10.

### Post-Processing

After computing the raw PDF:

1. **Floor negative values at zero.** Small negative densities are numerical artifacts from the finite differencing. These indicate mild convexity violations in the call price function, which can arise from interpolation imperfections or data noise.

2. **Normalise to integrate to 1.** Due to truncation (we only evaluate the density over a finite range of strikes) and the flooring of negative values, the raw PDF may not integrate exactly to 1. We renormalise:

$$\tilde{\pi}_{\text{norm}}(X) = \frac{\tilde{\pi}(X)}{\int \tilde{\pi}(X) \, dX}$$

---

## 8. No-Arbitrage Conditions and Diagnostics

### Necessary Conditions on the Call Price Function

For the extracted density to be valid, the call valuation function must satisfy:

**1. Monotonicity (decreasing in strike):**

$$\frac{\partial c}{\partial X} \leq 0$$

A call becomes less valuable as the strike increases (harder to end up in the money). This is equivalent to $\tilde{\Pi}(X) \leq 1$ for all $X$.

**2. Bounded slope:**

$$\frac{\partial c}{\partial X} \geq -e^{-rT}$$

The call price cannot decrease faster than the present value of the strike increase. This is equivalent to $\tilde{\Pi}(X) \geq 0$ for all $X$.

Together, these ensure $0 \leq \tilde{\Pi}(X) \leq 1$: the CDF is a valid probability distribution.

**3. Convexity:**

$$\frac{\partial^2 c}{\partial X^2} \geq 0$$

This is equivalent to $\tilde{\pi}(X) \geq 0$: the density is non-negative. A violation would create a **butterfly arbitrage** — you could construct a butterfly spread with negative cost and non-negative payoff.

### Translating to Smile Constraints

Using the chain rule, the call price derivatives can be expressed in terms of the smile and Black-Scholes sensitivities. Let $v_X$ denote the partial derivative of the BS formula with respect to $X$, and $v_\sigma$ denote vega. Then:

$$\frac{\partial c}{\partial X} = v_X + v_\sigma \cdot \frac{d\sigma}{dX}$$

The monotonicity constraint translates to an **upper bound on the smile slope** (Malz 2014, Eq. 7):

$$\frac{d\sigma}{dX} \leq -\frac{v_X}{v_\sigma} > 0$$

And the bounded-slope constraint translates to a **lower bound** (Malz 2014, Eq. 8):

$$\frac{d\sigma}{dX} \geq -\frac{v_X + e^{-rT}}{v_\sigma} < 0$$

In practice, the upper bound is the one most likely to be violated (near the wings where vega is small and the smile may be steep).

### Diagnostic Checks

Following Malz (2014, Section 2.5), we verify:

1. **CDF bounds:** $\tilde{\Pi}(X_{\min}) \approx 0$ and $\tilde{\Pi}(X_{\max}) \approx 1$ at the extremes of our grid.

2. **PDF non-negativity:** Count how many grid points have $\tilde{\pi}(X) < 0$ before flooring. A small number is acceptable; a large number suggests the interpolation or data has problems.

3. **Mean check:** The risk-neutral mean should equal the forward price:

$$\int X \, \tilde{\pi}(X) \, dX \approx F = S_0 e^{(r-q)T}$$

This is a no-arbitrage requirement. Large deviations indicate problems with the tails of the distribution or the normalisation.

4. **Exercise-price deltas at data boundaries:**
   - At the lowest observed strike: $\partial c / \partial X \approx -e^{-rT}$ (deep ITM call has delta near $-1$ in exercise-price terms)
   - At the highest observed strike: $\partial c / \partial X \approx 0$ (deep OTM call is nearly worthless)

5. **Vega at boundaries:** Low vega at the data boundaries means the call price is insensitive to the smile value there, so flat extrapolation has minimal impact on the results.

---

## 9. Interpretation: What the Market Is Telling Us

### Moments Comparison

We compare the first four moments of the market-implied RND against the lognormal (Black-Scholes) benchmark:

| Moment | Market-Implied | Lognormal | Interpretation |
|--------|---------------|-----------|----------------|
| **Mean** | $\approx F$ | $= F$ | Both centre on the forward price (no-arbitrage) |
| **Std Dev** | Slightly different | Benchmark | Width of distribution |
| **Skewness** | Negative | Slightly negative | Market prices more downside risk |
| **Excess Kurtosis** | Positive | $\approx 0$ | Market prices fatter tails |

### The Volatility Skew and Crash Risk

The negative skewness in the market-implied distribution reflects the **volatility skew**: OTM puts (downside protection) are expensive relative to OTM calls. This means:

- The market assigns higher probability to large declines than the lognormal model predicts
- Investors are willing to pay a premium for crash protection
- This skew became pronounced after the 1987 crash and has persisted ever since (Jackwerth 2004)

### Tail Risk Ratios

For each tail event (e.g., a 10% decline), we compute:

$$\text{Tail ratio} = \frac{P_{\text{market}}(S_T < S_0 \times 0.9)}{P_{\text{lognormal}}(S_T < S_0 \times 0.9)}$$

A ratio greater than 1 means the market assigns **more** probability to that tail event than the lognormal model. Typical values for equity indices:

- 5% decline: ratio $\approx 0.8-1.2$ (close to lognormal)
- 10% decline: ratio $\approx 1.5-3.0$ (market prices significantly more probability)
- 20% decline: ratio $\approx 3-10+$ (the market's implied crash probability can be an order of magnitude higher than lognormal)

### The Pricing Kernel Puzzle

Jackwerth (2004) documents a puzzling finding: while the risk-neutral distribution has fat left tails, the *actual* (historical) distribution of S&P 500 returns looks roughly lognormal. This implies that the pricing kernel — the ratio of risk-neutral to physical densities — is **not** monotonically decreasing in wealth, contradicting standard risk aversion.

This remains an open research question. Possible explanations include:
- Crash fear that is not reflected in historical frequencies
- Institutional demand for portfolio insurance
- Market microstructure effects (illiquidity premiums for deep OTM puts)

---

## 10. Implementation Details

### Data Pipeline

1. **Fetch** option chain data for SPY from Yahoo Finance via `yfinance`
2. **Select** the expiry nearest to 30 DTE (days to expiration)
3. **Clean** the data: filter by minimum price, open interest, and moneyness range (0.7 to 1.3)
4. **Handle market-closed data**: when bid/ask are both zero (e.g., weekends/holidays), fall back to `lastPrice`
5. **Compute** implied volatilities by inverting Black-Scholes using Brent's root-finding method
6. **Construct** the smile from OTM puts ($X < S_0$) and OTM calls ($X \geq S_0$)

### Interpolation

- **Method:** `scipy.interpolate.CubicSpline` with `bc_type=((1, 0.0), (1, 0.0))` (clamped, zero slope at boundaries)
- **Extrapolation:** Flat at boundary IV values — implemented by clamping `sigma(X)` to `sigma(X_1)` for $X < X_1$ and `sigma(X_n)$ for $X > X_n$
- **Safety floor:** $\sigma(X) \geq 0.001$ to prevent numerical issues

### Strike Grid

- **Range:** 50% to 150% of spot price (well beyond observed data)
- **Resolution:** 2000 points for the smile/call function, 1500 for the RND
- **Grid spacing:** approximately \$0.34

### Black-Scholes Parameters

| Parameter | Value | Source |
|-----------|-------|--------|
| Risk-free rate $r$ | 4.3% | Approximate 3-month T-bill yield |
| Dividend yield $q$ | 1.3% | SPY trailing dividend yield |
| Time to expiry $T$ | $\text{DTE} / 365$ | Selected expiry date |

### Numerical Integration

All integrals (moments, tail probabilities, normalisation) use the **trapezoidal rule** (`numpy.trapezoid`), which is sufficient given the fine grid resolution (1500 points over the relevant range).

### Sensitivity Analysis

We show the effect of varying the finite difference step size $\Delta$ across four values:
- $\alpha = 0.010$ (finest, most noise)
- $\alpha = 0.025$ (baseline)
- $\alpha = 0.050$ (moderate smoothing)
- $\alpha = 0.100$ (heavy smoothing)

---

## 11. Multi-Expiry Analysis and the Implied Volatility Surface

The volatility smile varies systematically with time to expiry, forming the **implied volatility surface** $\sigma(X, \tau)$. This is a central object in derivatives pricing — a complete surface captures the market's forward-looking view across both strike and maturity dimensions.

### Construction

For each available expiry $\tau_j$ (targeting 4–6 expiries in the 7–180 DTE range):

1. Fetch the option chain and compute OTM implied volatilities (same procedure as for the single expiry)
2. Fit a clamped cubic spline $\sigma_j(X)$ to each expiry's smile
3. Evaluate on a common **moneyness grid** $m = K/S \in [0.80, 1.20]$

The surface is then the collection $\{\sigma(m, \tau_j)\}$ displayed as a 3D Plotly surface plot.

### Term Structure of Moments

For each expiry, we apply the Breeden-Litzenberger method and compute the risk-neutral moments (mean, standard deviation, skewness, excess kurtosis) and left-tail probability. Plotting these against maturity reveals:

- **Standard deviation** increases with $\sqrt{\tau}$ (diffusion scaling)
- **Skewness** is typically negative at all maturities but may attenuate for longer horizons
- **Excess kurtosis** is positive (fat tails) and tends to decrease with maturity as the central limit theorem takes hold
- **Left-tail probability** increases with maturity (more time for large declines to occur)

---

## 12. State Prices and Arrow-Debreu Securities

### State Price Density

The state price density $p(X)$ gives the price today of receiving \$1 if the future price is exactly $X$ (Jackwerth 2004, Eq. 7):

$$p(X) = e^{-rT} \cdot \tilde{\pi}(X)$$

The integral over all states must equal the discount factor:

$$\int_0^\infty p(X)\, dX = e^{-rT}$$

This provides a useful sanity check on the extracted RND.

### Butterfly Spread Decomposition

A butterfly spread centred at strike $X$ with wing width $\Delta$ has cost:

$$\text{Butterfly}(X, \Delta) = c(X + \Delta) + c(X - \Delta) - 2c(X)$$

In the limit $\Delta \to 0$, this payoff converges to a Dirac delta at $S_T = X$, i.e., an Arrow-Debreu security. Therefore:

$$p(X) = \lim_{\Delta \to 0} \frac{\text{Butterfly}(X, \Delta)}{\Delta^2}$$

This is the discrete analogue of the Breeden-Litzenberger second derivative (BL 1978, Theorem 1).

---

## 13. No-Arbitrage Smile Slope Constraints

### Derivation (Malz 2014, Eq. 7–8)

Since the call price depends on strike both directly and through the smile $\sigma(X)$:

$$\frac{\partial c}{\partial X} = v_X + v_\sigma \cdot \frac{d\sigma}{dX}$$

where $v_X = -e^{-rT}\Phi(d_2)$ is the exercise-price delta and $v_\sigma$ is vega.

**Monotonicity** ($\partial c / \partial X \leq 0$) requires:

$$\frac{d\sigma}{dX} \leq -\frac{v_X}{v_\sigma}$$

**Bounded slope** ($\partial c / \partial X \geq -e^{-rT}$) requires:

$$\frac{d\sigma}{dX} \geq -\frac{v_X + e^{-rT}}{v_\sigma}$$

### Interpretation

- Violations of the upper bound produce **negative densities** (butterfly arbitrage)
- Violations of the lower bound produce **CDF values outside [0,1]**
- The constraints are tightest near the money (where vega is large) and most easily violated in the wings (where vega is small and the smile may be steep)

The clamped cubic spline interpolation (with flat extrapolation) is designed to satisfy these constraints by construction.

---

## 14. Mixture of Lognormals

### Model (Jackwerth 2004, Exhibit 1)

A mixture of two lognormals prices calls as:

$$c_{\text{mix}}(K) = w \cdot \text{BS}(K, \sigma_1) + (1-w) \cdot \text{BS}(K, \sigma_2)$$

The corresponding density is:

$$f_{\text{mix}}(S_T) = w \cdot f_{\text{LN}}(S_T; \sigma_1) + (1-w) \cdot f_{\text{LN}}(S_T; \sigma_2)$$

where $f_{\text{LN}}$ is the lognormal density with drift $(r - q - \sigma^2/2)T$.

### Calibration

We fit the three parameters $(w, \sigma_1, \sigma_2)$ by minimising the sum of squared implied volatility errors:

$$\min_{w, \sigma_1, \sigma_2} \sum_{i} \left[\sigma_{\text{mix}}^{\text{imp}}(K_i) - \sigma_{\text{market}}(K_i)\right]^2$$

This is solved via L-BFGS-B (bounded optimisation). The mixture model can capture the volatility skew because the two components have different volatilities — the higher-volatility component adds probability mass to the tails.

---

## 15. Pricing Kernel Extraction

### Definition (Jackwerth 2004, Eq. 12)

The pricing kernel (stochastic discount factor) connects risk-neutral and physical densities:

$$m(S_T) = \frac{\tilde{\pi}(S_T)}{e^{rT} \cdot f^P(S_T)}$$

Under standard expected utility with a concave, increasing utility function, the pricing kernel must be **monotonically decreasing** in wealth $S_T$. Intuitively: an additional dollar is worth more in bad states than in good states.

### Physical Density Estimation

We estimate $f^P(S_T)$ from historical data:

1. Fetch 3 years of daily SPY closing prices
2. Compute overlapping $T$-day returns (matching the option horizon)
3. Map to future price levels: $S_T^{(i)} = S_0 \cdot R_i$ where $R_i = S_{t+T}^{(i)} / S_t^{(i)}$
4. Fit a Gaussian kernel density estimator (Silverman bandwidth)

### The Pricing Kernel Puzzle

Jackwerth (2004, pp. 54–56) documents that the empirically estimated pricing kernel for S&P 500 options is **not** monotonically decreasing. Over some range (typically near the money), it increases — implying that the representative agent would have locally risk-seeking preferences, which contradicts standard economic theory.

Possible explanations include:
- **Crash fear** not captured by historical frequencies
- **Institutional demand** for portfolio insurance (OTM puts)
- **Heterogeneous beliefs** among market participants
- **Estimation error** in the physical density

---

## 16. Term Structure of Risk-Neutral Moments

By computing the RND at multiple expiries, we can study how the market's forward-looking risk assessment varies with the investment horizon:

| Moment | Typical Pattern |
|--------|----------------|
| Std Dev | Increases with $\sqrt{\tau}$ (diffusion scaling) |
| Skewness | Negative at all maturities; may attenuate at longer horizons |
| Excess Kurtosis | Positive (fat tails); decreases toward zero for long maturities |
| Left-tail probability | Increases with maturity |

Comparing market-implied moments against the lognormal benchmark at each maturity quantifies the **maturity dependence** of the market's departure from Black-Scholes assumptions.

---

## 17. References

1. **Breeden, D.T. and Litzenberger, R.H.** (1978). "Prices of State-Contingent Claims Implicit in Option Prices." *Journal of Business*, 51(4), 621-651.

   - The foundational paper establishing that state price densities equal the second derivative of call prices with respect to strike. Proves sufficiency of call options for spanning Arrow-Debreu securities under standard preference assumptions.

2. **Malz, A.M.** (2014). "A Simple and Reliable Way to Compute Option-Based Risk-Neutral Distributions." *Federal Reserve Bank of New York Staff Reports*, No. 677.

   - The operational cookbook for computing RNDs. Specifies the clamped cubic spline interpolation, finite difference formulas, step-size considerations, no-arbitrage conditions on the volatility smile, and diagnostic procedures.

3. **Jackwerth, J.C.** (2004). "Option-Implied Risk-Neutral Distributions and Risk Aversion." *Research Foundation of CFA Institute*.

   - Comprehensive survey of methods for recovering risk-neutral distributions from options. Covers parametric (mixture, expansion, generalised distribution) and nonparametric (entropy, kernel, curve-fitting) methods. Documents the post-1987 skew and the pricing kernel puzzle.

4. **Black, F. and Scholes, M.** (1973). "The Pricing of Options and Corporate Liabilities." *Journal of Political Economy*, 81(3), 637-654.

5. **Arrow, K.J.** (1964). "The Role of Securities in the Optimal Allocation of Risk-Bearing." *Review of Economic Studies*, 31(2), 91-96.

6. **Debreu, G.** (1959). *Theory of Value: An Axiomatic Analysis of Economic Equilibrium.* Yale University Press.
