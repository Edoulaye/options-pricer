import time

from src.black_scholes import bs_price, bs_delta, bs_gamma, bs_vega, bs_theta, bs_rho
from src.binomial import binomial_price
from src.monte_carlo import mc_price

# Parametres de reference (Hull ch.15)
PARAMS = dict(S=42, K=40, T=0.5, r=0.10, sigma=0.20)


def comparer_methodes(option_type="call"):
    """Affiche les prix des trois methodes, avec temps et intervalles."""
    print(f"\n{'=' * 64}")
    print(f"  Option {option_type.upper()} europeenne")
    print(f"  S={PARAMS['S']}  K={PARAMS['K']}  T={PARAMS['T']}  "
          f"r={PARAMS['r']}  sigma={PARAMS['sigma']}")
    print(f"{'=' * 64}\n")

    t0 = time.perf_counter()
    prix_bs = bs_price(**PARAMS, option_type=option_type)
    t_bs = time.perf_counter() - t0

    t0 = time.perf_counter()
    prix_bin = binomial_price(**PARAMS, n=2000, option_type=option_type)
    t_bin = time.perf_counter() - t0

    t0 = time.perf_counter()
    prix_mc, err_mc = mc_price(**PARAMS, n_sim=500_000,
                               option_type=option_type, seed=42)
    t_mc = time.perf_counter() - t0

    t0 = time.perf_counter()
    prix_anti, err_anti = mc_price(**PARAMS, n_sim=500_000,
                                   option_type=option_type,
                                   antithetic=True, seed=42)
    t_anti = time.perf_counter() - t0

    print(f"{'Methode':<26}{'Prix':>10}{'Ecart/BS':>12}{'Temps (ms)':>14}")
    print("-" * 64)
    print(f"{'Black-Scholes':<26}{prix_bs:>10.4f}{'--':>12}{t_bs * 1000:>14.2f}")
    print(f"{'Binomial (n=2000)':<26}{prix_bin:>10.4f}"
          f"{prix_bin - prix_bs:>12.4f}{t_bin * 1000:>14.2f}")
    print(f"{'Monte Carlo (500k)':<26}{prix_mc:>10.4f}"
          f"{prix_mc - prix_bs:>12.4f}{t_mc * 1000:>14.2f}")
    print(f"{'MC antithetique (500k)':<26}{prix_anti:>10.4f}"
          f"{prix_anti - prix_bs:>12.4f}{t_anti * 1000:>14.2f}")

    print("\n  Intervalles de confiance a 95% :")
    print(f"    MC simple       : [{prix_mc - 1.96 * err_mc:.4f}, "
          f"{prix_mc + 1.96 * err_mc:.4f}]   erreur type = {err_mc:.5f}")
    print(f"    MC antithetique : [{prix_anti - 1.96 * err_anti:.4f}, "
          f"{prix_anti + 1.96 * err_anti:.4f}]   erreur type = {err_anti:.5f}")
    print(f"    Reduction de l'erreur type : "
          f"{(1 - err_anti / err_mc) * 100:.1f} %")


def afficher_grecques(option_type="call"):
    """Affiche les cinq grecques analytiques."""
    print(f"\n{'=' * 64}")
    print(f"  Grecques analytiques ({option_type})")
    print(f"{'=' * 64}\n")
    print(f"  Delta  {bs_delta(**PARAMS, option_type=option_type):>10.4f}")
    print(f"  Gamma  {bs_gamma(**PARAMS, option_type=option_type):>10.4f}")
    vega = bs_vega(**PARAMS, option_type=option_type)
    print(f"  Vega   {vega:>10.4f}   (par point de vol : {vega / 100:.4f})")
    theta = bs_theta(**PARAMS, option_type=option_type)
    print(f"  Theta  {theta:>10.4f}   (par jour : {theta / 365:.4f})")
    print(f"  Rho    {bs_rho(**PARAMS, option_type=option_type):>10.4f}")


def comparer_americain_europeen():
    """Montre la prime d'exercice anticipe sur un put dans la monnaie."""
    p = dict(S=90, K=100, T=1.0, r=0.05, sigma=0.30)
    eur = binomial_price(**p, n=1000, option_type="put", exercise="european")
    ame = binomial_price(**p, n=1000, option_type="put", exercise="american")

    print(f"\n{'=' * 64}")
    print("  Exercice anticipe (put dans la monnaie)")
    print(f"  S={p['S']}  K={p['K']}  T={p['T']}  r={p['r']}  sigma={p['sigma']}")
    print(f"{'=' * 64}\n")
    print(f"  Put europeen  {eur:>10.4f}")
    print(f"  Put americain {ame:>10.4f}")
    print(f"  Prime         {ame - eur:>10.4f}  "
          f"({(ame - eur) / eur * 100:.2f} % du prix europeen)")


if __name__ == "__main__":
    comparer_methodes("call")
    comparer_methodes("put")
    afficher_grecques("call")
    comparer_americain_europeen()
    print()