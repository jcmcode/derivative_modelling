# Derivative Modelling: Inferring Market-Implied Probabilities

Goal: reconstruct the probability distribution the market is implying from option prices, then compare it to textbook assumptions (normal returns, Black-Scholes) to see where tail risk and directional bias actually sit.

## What this builds
- Implied volatility surface from listed calls and puts across strikes/expiries.
- Smooth price curves (cubic splines) so second derivatives are stable.
- Breeden-Litzenberger extraction of the risk-neutral density: $$P(S_T = K) \propto \frac{\partial^2 C}{\partial K^2}$$
- Visuals of the market-implied PDF vs. a lognormal/normal benchmark.

## Workflow
1) Ingest option chains (strike, bid, ask, expiry, underlying spot/rates/dividends).
2) Compute IVs and build the smile/surface; flag obvious bad quotes.
3) Interpolate/extrapolate to a smooth call price function in strike space.
4) Take second derivatives to back out the risk-neutral density; normalize to a PDF.
5) Plot and compare the implied distribution to the standard model, focusing on skew and tail fatness.

## Questions this answers
- How steep is downside skew vs. upside? Are puts structurally richer?
- How much extra probability mass is priced into 2-3 sigma moves relative to a normal curve?
- How does the implied distribution shift across maturities (1w vs. 6m)?

## Why it matters
Market prices embed the consensus forward view (under risk-neutral measure). Recovering that distribution shows where traders think the asset can go and how much they charge for tails, instead of relying on an assumed normal world.