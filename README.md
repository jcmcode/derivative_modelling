# Derivative Modelling

## Project Goal
Extract the probability distribution the market is implying from option prices, then see where it differs from standard assumptions (lognormal returns, Black-Scholes).

## What We're Doing
1. Collect market prices for calls and puts across different strikes and expiries.
2. Calculate implied volatility and build the volatility smile.
3. Use the Breeden-Litzenberger method to recover the risk-neutral probability density from option prices.
4. Compare the market-implied distribution to textbook models to identify tail risk and skew.

## Why It Matters
Market prices contain the collective forward view of where an asset can go and how much traders charge for extreme moves. This project extracts that signal instead of assuming normal returns.
