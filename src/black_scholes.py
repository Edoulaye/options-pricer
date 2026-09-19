import numpy as np
from scipy.stats import norm


def bs_price(S, K, T, r, sigma, option_type="call"):
    """..."""
    if option_type not in ("call", "put"):
        raise ValueError(f"option_type invalide : {option_type}")
    if T <= 0 or sigma <= 0:
        strike_actualise = K * np.exp(-r * T)
        if option_type == "call":
            return max(S - strike_actualise, 0.0)
        else:
            return max(strike_actualise - S, 0.0)

    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == "call":
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)