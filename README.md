# Derivative Modelling: Reconstructing Market Probabilities

Standard option models assume stock returns follow a normal distribution. They don't. This project is a technical deep-dive into how the market actually prices "tail risk" and directional bias.

I am building this to understand the mechanics of the **Volatility Smile** and how to extract a **Probability Density Function (PDF)** directly from market prices.

## The Core Logic
1. **The IV Surface:** Collect market prices for Calls/Puts across all strikes and expiries.
2. **The "Smile":** Calculate Implied Volatility for each. If the market followed Black-Scholes, this would be a flat line. It’s actually a curve, showing the market overprices "crashes" (Downside Skew).
3. **Breeden-Litzenberger Identity:** This is the "Magic" step. It proves that the probability of a stock landing at a certain price is hidden in the curvature of the option's price graph:
   $$P(S_T = K) \propto \frac{\partial^2 C}{\partial K^2}$$
   By taking the second derivative of the Call price relative to the Strike ($K$), we get the **Market-Implied Probability.**

## Project Workflow
- **Data:** Scraping live Option Chains (Strike, Bid, Ask, Expiry).
- **Interpolation:** Market data is "gappy." I'm using **Cubic Splines** to create a smooth price curve so I can actually calculate derivatives.
- **PDF Extraction:** Converting that smooth curve into a probability distribution.
- **Visualization:** Plotting the "Bell Curve" the market is *actually* betting on vs. what a standard model predicts.

## Key Questions This Project Answers
* **Skewness:** Why is a $90 Put more expensive than a $110 Call when the stock is at $100? (Answer: The market fears the downside more).
* **Fat Tails:** How much "extra" probability is the market pricing into a 20% crash compared to a normal distribution?
* **Term Structure:** How does the market's expectation of risk change between 1 week from now and 6 months from now?