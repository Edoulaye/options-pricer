import numpy as np
import pytest
from src.black_scholes import bs_price

def test_hull_call():
    prix = bs_price(S=42, K=40, T=0.5, r=0.10, sigma=0.20, option_type="call")
    assert prix == pytest.approx(4.76, abs=0.01)


def test_hull_put():
    prix = bs_price(S=42, K=40, T=0.5, r=0.10, sigma=0.20, option_type="put")
    assert prix == pytest.approx(0.81, abs=0.01)

def test_maturite_nulle_call_itm():
    """T=0 : le prix est le payoff immediat."""
    prix = bs_price(S=110, K=100, T=0, r=0.05, sigma=0.20, option_type="call")
    assert prix == pytest.approx(10.0)


def test_maturite_nulle_call_otm():
    prix = bs_price(S=90, K=100, T=0, r=0.05, sigma=0.20, option_type="call")
    assert prix == pytest.approx(0.0)


def test_vol_nulle_call():
    """sigma=0 : le prix est le forward actualise."""
    prix = bs_price(S=100, K=100, T=1, r=0.05, sigma=0, option_type="call")
    attendu = max(100 - 100 * np.exp(-0.05), 0)
    assert prix == pytest.approx(attendu)

@pytest.mark.parametrize("S,K,T,r,sigma", [
    (100, 100, 1.0, 0.05, 0.20),    
    (120, 100, 1.0, 0.05, 0.20),    
    (80, 100, 1.0, 0.05, 0.20),     
    (100, 100, 0.25, 0.03, 0.40),
    (100, 100, 5.0, 0.08, 0.15),    
    (50, 200, 2.0, 0.02, 0.60),     
    (100, 100, 1.0, 0.0, 0.20),     
])
def test_parite_put_call(S, K, T, r, sigma):
    """C - P = S - K*exp(-rT), vrai pour tout jeu de parametres."""
    call = bs_price(S, K, T, r, sigma, "call")
    put = bs_price(S, K, T, r, sigma, "put")
    assert call - put == pytest.approx(S - K * np.exp(-r * T))

@pytest.mark.parametrize("S,K,T,r,sigma", [
    (100, 100, 1.0, 0.05, 0.20),
    (120, 100, 0.5, 0.03, 0.35),
    (80, 100, 2.0, 0.06, 0.25),
])
def test_bornes_call(S, K, T, r, sigma):
    call = bs_price(S, K, T, r, sigma, "call")
    borne_inf = max(S - K * np.exp(-r * T), 0)
    assert call >= borne_inf - 1e-10
    assert call <= S


@pytest.mark.parametrize("S,K,T,r,sigma", [
    (100, 100, 1.0, 0.05, 0.20),
    (120, 100, 0.5, 0.03, 0.35),
    (80, 100, 2.0, 0.06, 0.25),
])
def test_bornes_put(S, K, T, r, sigma):
    put = bs_price(S, K, T, r, sigma, "put")
    assert put >= 0
    assert put <= K * np.exp(-r * T)