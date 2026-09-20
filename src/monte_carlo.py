import numpy as np


def mc_price(S, K, T, r, sigma, n_sim=100_000, option_type="call",
             antithetic=False, seed=None):
    """
    Prix d'une option europeenne par simulation de Monte Carlo.

    Parametres
    ----------
    S : float           prix actuel du sous-jacent
    K : float           strike
    T : float           maturite en annees
    r : float           taux sans risque annualise, composition continue
    sigma : float       volatilite annualisee
    n_sim : int         nombre total de trajectoires simulees
    option_type : str   "call" ou "put"
    antithetic : bool   si True, utilise des variables antithetiques
    seed : int or None  graine du generateur, pour la reproductibilite

    Retour
    ------
    (prix, erreur_type) : tuple de floats
        prix        : estimateur du prix de l'option
        erreur_type : ecart-type de l'estimateur (pour l'intervalle de confiance)
    """
    if option_type not in ("call", "put"):
        raise ValueError(f"option_type invalide : {option_type}")

    rng = np.random.default_rng(seed)

    if antithetic:
        # on tire n_sim/2 normales et on ajoute leurs opposees
        n_tirages = n_sim // 2
        Z_base = rng.standard_normal(n_tirages)
        Z = np.concatenate([Z_base, -Z_base])
    else:
        Z = rng.standard_normal(n_sim)

    # solution de l'EDS a l'echeance
    S_T = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)

    if option_type == "call":
        payoffs = np.maximum(S_T - K, 0.0)
    else:
        payoffs = np.maximum(K - S_T, 0.0)

    payoffs_actualises = np.exp(-r * T) * payoffs

    if antithetic:
        # on moyenne chaque paire (Z, -Z) avant d'estimer
        n_paires = len(payoffs_actualises) // 2
        echantillon = 0.5 * (payoffs_actualises[:n_paires]
                             + payoffs_actualises[n_paires:])
    else:
        echantillon = payoffs_actualises

    prix = float(echantillon.mean())
    erreur_type = float(echantillon.std(ddof=1) / np.sqrt(len(echantillon)))

    return prix, erreur_type