import yfinance as yf
import pandas as pd

def fetch_option_chain(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    # Fetch the nearest monthly expiry
    expiry = ticker.options[0] 
    chain = ticker.option_chain(expiry)
    
    calls = chain.calls[['strike', 'lastPrice', 'impliedVolatility', 'ask', 'bid']]
    calls['mid'] = (calls['ask'] + calls['bid']) / 2
    
    # Store underlying price for the model
    underlying_price = ticker.history(period="1d")['Close'].iloc[-1]
    
    return calls, underlying_price, expiry
