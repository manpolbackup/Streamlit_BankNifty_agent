# tools.py

from nsepython import *

import pandas as pd

# Tool 1: Option Chain Fetcher
from langchain_core.tools import tool

@tool
def get_option_chain(symbol: str):
    """Fetches the full option chain data, spot price, and timestamp for a given symbol using NSEPython."""

    df, spot, timestamp = oi_chain_builder(
        symbol,
        "latest",
        "full"
    )

    return {
        "spot": spot,
        "timestamp": timestamp,
        "data": df.to_json()
    }

# Tool 2: ATM Finder
from langchain_core.tools import tool

@tool
def find_atm(spot, strikes):
    """Finds the At-The-Money (ATM) strike price closest to the spot price from a list of strikes."""
    # Ensure spot is a float
    spot_val = float(spot)
    
    # Convert strikes to float, filtering out any invalid values if necessary
    numeric_strikes = []
    for s in strikes:
        try:
            numeric_strikes.append(float(s))
        except (ValueError, TypeError):
            continue

    # Find the closest strike price
    atm = min(
        numeric_strikes,
        key=lambda x: abs(x - spot_val)
    )

    return atm

#Tool 3: PCR Calculator

@tool
def calculate_pcr(df, atm):
    """Calculates the Put-Call Ratio (PCR) by comparing PE OI below ATM and CE OI above ATM."""

    # Custom logic here

    return {
        "put_sum": put_sum,
        "call_sum": call_sum,
        "pcr": pcr
    }

#Tool 4: Sentiment Engine

@tool
def market_sentiment(pcr):
    """Determines the market sentiment (Strong Bullish, Bullish, Neutral, or Bearish) based on the Put-Call Ratio (PCR) value."""

    if pcr >= 1.5:
        return "Strong Bullish"

    elif pcr >= 1.2:
        return "Bullish"

    elif pcr >= 0.8:
        return "Neutral"

    else:
        return "Bearish"

