import numpy as np
import pytest
from src.black_scholes import bs_delta, bs_gamma, bs_vega, bs_theta, bs_rho


# Parametres de reference : Hull ch.15
PARAMS = dict(S=42, K=40, T=0.5, r=0.10, sigma=0.20)


def test_delta_call_borne():
    """Le delta d'un call est toujours entre 0 et 1."""
    d = bs_delta(**PARAMS, option_type="call")
    assert 0 <= d <= 1


def test_delta_put_borne():
    """Le delta d'un put est toujours entre -1 et 0."""
    d = bs_delta(**PARAMS, option_type="put")
    assert -1 <= d <= 0


def test_relation_delta_parite():
    """Parite derivee par rapport a S : delta_call - delta_put = 1."""
    dc = bs_delta(**PARAMS, option_type="call")
    dp = bs_delta(**PARAMS, option_type="put")
    assert dc - dp == pytest.approx(1.0)


def test_gamma_identique():
    """Gamma est le meme pour call et put."""
    gc = bs_gamma(**PARAMS, option_type="call")
    gp = bs_gamma(**PARAMS, option_type="put")
    assert gc == pytest.approx(gp)


def test_vega_identique():
    """Vega est le meme pour call et put."""
    vc = bs_vega(**PARAMS, option_type="call")
    vp = bs_vega(**PARAMS, option_type="put")
    assert vc == pytest.approx(vp)


def test_gamma_vega_positifs():
    """Gamma et vega sont toujours positifs pour une position acheteuse."""
    assert bs_gamma(**PARAMS) > 0
    assert bs_vega(**PARAMS) > 0


def test_theta_call_negatif():
    """Le theta d'un call est negatif : erosion temporelle."""
    assert bs_theta(**PARAMS, option_type="call") < 0


def test_rho_signes():
    """Rho est positif pour un call, negatif pour un put."""
    assert bs_rho(**PARAMS, option_type="call") > 0
    assert bs_rho(**PARAMS, option_type="put") < 0