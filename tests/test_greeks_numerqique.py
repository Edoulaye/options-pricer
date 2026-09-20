import numpy as np
import pytest
from src.black_scholes import (
    bs_price, bs_delta, bs_gamma, bs_vega, bs_theta, bs_rho
)

PARAMS = dict(S=42, K=40, T=0.5, r=0.10, sigma=0.20)


def derivee_centree(f, x, eps):
    """Approximation de f'(x) par difference centree."""
    return (f(x + eps) - f(x - eps)) / (2 * eps)


def derivee_seconde(f, x, eps):
    """Approximation de f''(x) par difference centree a trois points."""
    return (f(x + eps) - 2 * f(x) + f(x - eps)) / eps**2


@pytest.mark.parametrize("option_type", ["call", "put"])
def test_delta_numerique(option_type):
    p = PARAMS.copy()
    eps = 1e-4 * p["S"]
    f = lambda s: bs_price(S=s, K=p["K"], T=p["T"], r=p["r"],
                           sigma=p["sigma"], option_type=option_type)
    numerique = derivee_centree(f, p["S"], eps)
    analytique = bs_delta(**p, option_type=option_type)
    assert numerique == pytest.approx(analytique, rel=1e-4)


@pytest.mark.parametrize("option_type", ["call", "put"])
def test_gamma_numerique(option_type):
    p = PARAMS.copy()
    eps = 1e-3 * p["S"]      # plus grand : derivee seconde, plus sensible a l'arrondi
    f = lambda s: bs_price(S=s, K=p["K"], T=p["T"], r=p["r"],
                           sigma=p["sigma"], option_type=option_type)
    numerique = derivee_seconde(f, p["S"], eps)
    analytique = bs_gamma(**p, option_type=option_type)
    assert numerique == pytest.approx(analytique, rel=1e-3)


@pytest.mark.parametrize("option_type", ["call", "put"])
def test_vega_numerique(option_type):
    p = PARAMS.copy()
    eps = 1e-5
    f = lambda sig: bs_price(S=p["S"], K=p["K"], T=p["T"], r=p["r"],
                             sigma=sig, option_type=option_type)
    numerique = derivee_centree(f, p["sigma"], eps)
    analytique = bs_vega(**p, option_type=option_type)
    assert numerique == pytest.approx(analytique, rel=1e-4)


@pytest.mark.parametrize("option_type", ["call", "put"])
def test_rho_numerique(option_type):
    p = PARAMS.copy()
    eps = 1e-6
    f = lambda taux: bs_price(S=p["S"], K=p["K"], T=p["T"], r=taux,
                              sigma=p["sigma"], option_type=option_type)
    numerique = derivee_centree(f, p["r"], eps)
    analytique = bs_rho(**p, option_type=option_type)
    assert numerique == pytest.approx(analytique, rel=1e-4)


@pytest.mark.parametrize("option_type", ["call", "put"])
def test_theta_numerique(option_type):
    p = PARAMS.copy()
    eps = 1e-5
    f = lambda t: bs_price(S=p["S"], K=p["K"], T=t, r=p["r"],
                           sigma=p["sigma"], option_type=option_type)
    numerique = derivee_centree(f, p["T"], eps)
    analytique = bs_theta(**p, option_type=option_type)
    assert numerique == pytest.approx(-analytique, rel=1e-4)