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


def _d1_d2(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return d1, d2


def bs_delta(S, K, T, r, sigma, option_type="call"):
    d1, _ = _d1_d2(S, K, T, r, sigma)
    if option_type == "call":
        return norm.cdf(d1)
    return norm.cdf(d1) - 1


def bs_gamma(S, K, T, r, sigma, option_type="call"):
    d1, _ = _d1_d2(S, K, T, r, sigma)
    return norm.pdf(d1) / (S * sigma * np.sqrt(T))


def bs_vega(S, K, T, r, sigma, option_type="call"):
    d1, _ = _d1_d2(S, K, T, r, sigma)
    return S * norm.pdf(d1) * np.sqrt(T)


def bs_theta(S, K, T, r, sigma, option_type="call"):
    d1, d2 = _d1_d2(S, K, T, r, sigma)
    terme_commun = -S * norm.pdf(d1) * sigma / (2 * np.sqrt(T))
    if option_type == "call":
        return terme_commun - r * K * np.exp(-r * T) * norm.cdf(d2)
    return terme_commun + r * K * np.exp(-r * T) * norm.cdf(-d2)


def bs_rho(S, K, T, r, sigma, option_type="call"):
    _, d2 = _d1_d2(S, K, T, r, sigma)
    if option_type == "call":
        return K * T * np.exp(-r * T) * norm.cdf(d2)
    return -K * T * np.exp(-r * T) * norm.cdf(-d2)