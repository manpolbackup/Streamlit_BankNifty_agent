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

    print(df.columns.tolist())

    print(df[["Strike Price","CALLS_OI","PUTS_OI"]].head())

    df_small = df[
        ["Strike Price", "CALLS_OI", "PUTS_OI"]
    ]

    return {
        "spot": spot,
        "data": df_small.to_json(orient="records")
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
def calculate_pcr(df_json: str, atm: float):
    """Calculates the PCR ratio based on the 10 strikes above and below ATM.
   Calculate PCR using:
    - PE OI for 10 strikes below ATM
    - CE OI for 10 strikes above ATM
    """

    import pandas as pd

    import json

    print(type(df_json))
    print(df_json[:200])

    print(df_json)

    df = pd.DataFrame(json.loads(df_json))


    print("Columns:")
    print(df.columns.tolist())

    print("Head:")
    print(df.head())

    required_cols = ["Strike Price", "CALLS_OI", "PUTS_OI"]

    missing = [c for c in required_cols if c not in df.columns]

    if missing:
    	raise ValueError(
            f"Missing columns {missing}. "
            f"Available columns: {list(df.columns)}"
        )


    df["Strike Price"] = pd.to_numeric(
        df["Strike Price"],
        errors="coerce"
    )

    # Put OI: 10 strikes below ATM
    put_side = (
        df[df["Strike Price"] < atm]
        .sort_values(
            "Strike Price",
            ascending=False
        )
        .head(10)
    )

    put_sum = put_side["PUTS_OI"].sum()

    # Call OI: 10 strikes above ATM
    call_side = (
        df[df["Strike Price"] > atm]
        .sort_values(
            "Strike Price",
            ascending=True
        )
        .head(10)
    )



    print("ATM:", atm)

    print("PUT SIDE")
    print(put_side[["Strike Price", "PUTS_OI"]])

    print("CALL SIDE")
    print(call_side[["Strike Price", "CALLS_OI"]])

    call_sum = call_side["CALLS_OI"].sum()

    if call_sum == 0:
        pcr = 0
    else:
        pcr = round(
            put_sum / call_sum,
            2
        )

    return {
        "put_sum": int(put_sum),
        "call_sum": int(call_sum),
        "pcr": pcr
    }

#Tool 4: Sentiment Engine

@tool
def market_sentiment(pcr: float):
    """ Market Sentiments based on the PCR Ratio.
    """

    if pcr >= 1.5:
        return "Strong Bullish"

    elif pcr >= 1.2:
        return "Moderately Bullish"

    elif pcr >= 1.0:
        return "Mildly Bullish"

    elif pcr >= 0.8:
        return "Neutral"

    elif pcr >= 0.6:
        return "Moderately Bearish"

    else:
        return "Strong Bearish"
