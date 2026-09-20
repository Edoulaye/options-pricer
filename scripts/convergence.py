"""Graphiques du pricer : convergence binomiale et prime d'exercice anticipe."""

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from src.black_scholes import bs_price
from src.binomial import binomial_price

# Parametres de reference (Hull ch.15)
PARAMS = dict(S=42, K=40, T=0.5, r=0.10, sigma=0.20)


def _sauvegarder(fichier):
    """Cree le dossier de destination si besoin, puis enregistre la figure."""
    Path(fichier).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(fichier, dpi=150)
    print(f"Figure enregistree : {fichier}")
    plt.close()


def graphique_convergence(n_max=200, fichier="figures/convergence.png"):
    """Prix binomial en fonction du nombre de pas, avec Black-Scholes en reference."""
    n_values = np.arange(1, n_max + 1)
    prix_bino = [binomial_price(**PARAMS, n=int(n), option_type="call")
                 for n in n_values]
    prix_bs = bs_price(**PARAMS, option_type="call")

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # panneau du haut : les prix
    ax1.plot(n_values, prix_bino, linewidth=0.9, label="Arbre binomial (CRR)")
    ax1.axhline(prix_bs, color="firebrick", linestyle="--", linewidth=1.5,
                label=f"Black-Scholes = {prix_bs:.4f}")
    ax1.set_ylabel("Prix du call")
    ax1.set_title("Convergence de l'arbre binomial vers Black-Scholes\n"
                  f"S={PARAMS['S']}, K={PARAMS['K']}, T={PARAMS['T']}, "
                  f"r={PARAMS['r']}, sigma={PARAMS['sigma']}")
    ax1.legend()
    ax1.grid(alpha=0.3)

    # panneau du bas : erreur absolue, echelle logarithmique
    erreurs = np.abs(np.array(prix_bino) - prix_bs)
    ax2.semilogy(n_values, erreurs, linewidth=0.9, color="darkslategray")
    ax2.set_xlabel("Nombre de pas n")
    ax2.set_ylabel("Erreur absolue (echelle log)")
    ax2.grid(alpha=0.3, which="both")

    plt.tight_layout()
    _sauvegarder(fichier)


def graphique_prime_americaine(fichier="figures/prime_americaine.png"):
    """Compare put americain et europeen selon le prix du sous-jacent."""
    p = dict(K=100, T=1.0, r=0.05, sigma=0.30)
    spots = np.linspace(60, 140, 60)

    eur = [binomial_price(S=s, **p, n=300, option_type="put",
                          exercise="european") for s in spots]
    ame = [binomial_price(S=s, **p, n=300, option_type="put",
                          exercise="american") for s in spots]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(spots, eur, label="Put europeen")
    ax.plot(spots, ame, label="Put americain")
    ax.plot(spots, np.array(ame) - np.array(eur),
            label="Prime d'exercice anticipe", linestyle=":", color="firebrick")
    ax.axvline(p["K"], color="gray", linestyle="--", alpha=0.5)
    ax.set_xlabel("Prix du sous-jacent")
    ax.set_ylabel("Prix de l'option")
    ax.set_title(f"Valeur de l'exercice anticipe (put)\n"
                 f"K={p['K']}, T={p['T']}, r={p['r']}, sigma={p['sigma']}")
    ax.legend()
    ax.grid(alpha=0.3)

    plt.tight_layout()
    _sauvegarder(fichier)


if __name__ == "__main__":
    graphique_convergence()
    graphique_prime_americaine()