import numpy as np


def mc_price(S, K, T, r, sigma, n_sim=100_000, option_type="call",
             antithetic=False, seed=None):
  
    if option_type not in ("call", "put"):
        raise ValueError(f"option_type invalide : {option_type}")

    rng = np.random.default_rng(seed)

    if antithetic:
    
        n_tirages = n_sim // 2
        Z_base = rng.standard_normal(n_tirages)
        Z = np.concatenate([Z_base, -Z_base])
    else:
        Z = rng.standard_normal(n_sim)
    S_T = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)

    if option_type == "call":
        payoffs = np.maximum(S_T - K, 0.0)
    else:
        payoffs = np.maximum(K - S_T, 0.0)

    payoffs_actualises = np.exp(-r * T) * payoffs

    if antithetic:
        n_paires = len(payoffs_actualises) // 2
        echantillon = 0.5 * (payoffs_actualises[:n_paires]
                             + payoffs_actualises[n_paires:])
    else:
        echantillon = payoffs_actualises

    prix = float(echantillon.mean())
    erreur_type = float(echantillon.std(ddof=1) / np.sqrt(len(echantillon)))

    return prix, erreur_type
