import numpy as np
import pytest
from src.black_scholes import bs_price
from src.monte_carlo import mc_price

PARAMS = dict(S=42, K=40, T=0.5, r=0.10, sigma=0.20)


@pytest.mark.parametrize("option_type", ["call", "put"])
def test_mc_proche_de_bs(option_type):
    """L'estimateur MC tombe pres du prix Black-Scholes."""
    prix, _ = mc_price(**PARAMS, n_sim=500_000, option_type=option_type, seed=42)
    bs = bs_price(**PARAMS, option_type=option_type)
    assert prix == pytest.approx(bs, abs=0.02)


@pytest.mark.parametrize("option_type", ["call", "put"])
def test_bs_dans_intervalle_confiance(option_type):
    """Le prix exact tombe dans l'intervalle de confiance a 95%."""
    prix, erreur_type = mc_price(**PARAMS, n_sim=200_000,
                                 option_type=option_type, seed=7)
    bs = bs_price(**PARAMS, option_type=option_type)
    assert abs(prix - bs) < 1.96 * erreur_type


def test_reproductibilite():
    """Une meme graine donne exactement le meme resultat."""
    a, _ = mc_price(**PARAMS, n_sim=10_000, seed=123)
    b, _ = mc_price(**PARAMS, n_sim=10_000, seed=123)
    assert a == b


def test_erreur_decroit_en_racine():
    """Quadrupler n_sim divise l'erreur type par environ 2."""
    _, err_n = mc_price(**PARAMS, n_sim=50_000, seed=1)
    _, err_4n = mc_price(**PARAMS, n_sim=200_000, seed=1)
    assert err_4n == pytest.approx(err_n / 2, rel=0.15)


def test_antithetiques_reduisent_variance():
    """Les variables antithetiques reduisent l'erreur type
    a budget de tirages egal."""
    _, err_simple = mc_price(**PARAMS, n_sim=100_000, seed=5,
                             antithetic=False)
    _, err_anti = mc_price(**PARAMS, n_sim=100_000, seed=5,
                           antithetic=True)
    assert err_anti < err_simple