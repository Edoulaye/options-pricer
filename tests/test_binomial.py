import numpy as np
import pytest
from src.black_scholes import bs_price
from src.binomial import binomial_price

PARAMS = dict(S=42, K=40, T=0.5, r=0.10, sigma=0.20)


@pytest.mark.parametrize("option_type", ["call", "put"])
def test_convergence_vers_bs(option_type):
    """Avec beaucoup de pas, l'europeenne converge vers Black-Scholes."""
    bino = binomial_price(**PARAMS, n=2000, option_type=option_type,
                          exercise="european")
    bs = bs_price(**PARAMS, option_type=option_type)
    assert bino == pytest.approx(bs, abs=0.01)


def test_erreur_decroit():
    """L'erreur diminue quand n augmente."""
    bs = bs_price(**PARAMS, option_type="call")
    err_10 = abs(binomial_price(**PARAMS, n=10, option_type="call") - bs)
    err_500 = abs(binomial_price(**PARAMS, n=500, option_type="call") - bs)
    assert err_500 < err_10


def test_americain_superieur_europeen():
    """Une americaine vaut au moins autant qu'une europeenne."""
    p = dict(S=100, K=110, T=1.0, r=0.05, sigma=0.30)
    eur = binomial_price(**p, n=200, option_type="put", exercise="european")
    ame = binomial_price(**p, n=200, option_type="put", exercise="american")
    assert ame >= eur


def test_call_americain_egale_europeen():
    """Sans dividendes, il n'est jamais optimal d'exercer un call
    americain avant l'echeance : les deux prix coincident."""
    eur = binomial_price(**PARAMS, n=200, option_type="call", exercise="european")
    ame = binomial_price(**PARAMS, n=200, option_type="call", exercise="american")
    assert ame == pytest.approx(eur, rel=1e-6)


@pytest.mark.parametrize("S,K,T,r,sigma", [
    (100, 100, 1.0, 0.05, 0.20),
    (120, 100, 0.5, 0.03, 0.35),
])
def test_parite_binomial(S, K, T, r, sigma):
    """La parite doit tenir aussi sur l'arbre."""
    c = binomial_price(S, K, T, r, sigma, n=500, option_type="call")
    p = binomial_price(S, K, T, r, sigma, n=500, option_type="put")
    assert c - p == pytest.approx(S - K * np.exp(-r * T), abs=0.01)