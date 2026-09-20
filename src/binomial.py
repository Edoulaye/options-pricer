import numpy as np


def binomial_price(S, K, T, r, sigma, n=500, option_type="call",
                   exercise="european"):
    """
    Prix d'une option par arbre binomial de Cox-Ross-Rubinstein.

    Parametres
    ----------
    S : float          prix actuel du sous-jacent
    K : float          strike
    T : float          maturite en annees
    r : float          taux sans risque annualise, composition continue
    sigma : float      volatilite annualisee
    n : int            nombre de pas de temps
    option_type : str  "call" ou "put"
    exercise : str     "european" ou "american"

    Retour
    ------
    float : prix de l'option
    """
    if option_type not in ("call", "put"):
        raise ValueError(f"option_type invalide : {option_type}")
    if exercise not in ("european", "american"):
        raise ValueError(f"exercise invalide : {exercise}")

    dt = T / n
    u = np.exp(sigma * np.sqrt(dt))
    d = 1.0 / u
    q = (np.exp(r * dt) - d) / (u - d)
    actualisation = np.exp(-r * dt)

    # prix du sous-jacent aux n+1 noeuds terminaux
    # le noeud j a fait j hausses et (n-j) baisses
    j = np.arange(n + 1)
    prix_finaux = S * u**j * d**(n - j)

    # payoffs a l'echeance
    if option_type == "call":
        valeurs = np.maximum(prix_finaux - K, 0.0)
    else:
        valeurs = np.maximum(K - prix_finaux, 0.0)

    # recursion arriere, couche par couche
    for i in range(n - 1, -1, -1):
        valeurs = actualisation * (q * valeurs[1:] + (1 - q) * valeurs[:-1])

        if exercise == "american":
            j = np.arange(i + 1)
            prix_noeuds = S * u**j * d**(i - j)
            if option_type == "call":
                exercice = np.maximum(prix_noeuds - K, 0.0)
            else:
                exercice = np.maximum(K - prix_noeuds, 0.0)
            valeurs = np.maximum(valeurs, exercice)

    return float(valeurs[0])