# import hypothesis
import numpy as np

import plower as plw

__author__ = "Chaitanya Kesanapalli"
__copyright__ = "Chaitanya Kesanapalli"
__license__ = "BSD 3-Clause"


def test_pm_coef():
    assert plw.get_pm_coef(1, 1) == (5 / (32 * np.pi))
    assert plw.get_pm_coef(0, 0) == 0.0


def test_pm_unit_spectrum():
    assert plw.get_pm_unit_spectrum(1) == np.exp(-1.25)
    assert plw.get_pm_unit_spectrum(np.inf) == 0.0


def test_pm_spectrum():
    assert plw.get_pm_spectrum(1, 1, 2 * np.pi) == (5 / (32 * np.pi)) * np.exp(-1.25)
    assert plw.get_pm_spectrum(1, 1, np.inf) == 0.0
    assert plw.get_pm_spectrum(1, 1, 0.1) == 0.0


def test_jonswap_coef():
    hs = 1
    tp = 1
    gamma = 1
    beta = (
        0.06238
        * (1.094 - 0.01915 * np.log(gamma))
        / (0.230 + 0.0336 * gamma - 0.185 / (1.9 + gamma))
    )

    assert plw.get_jonswap_coef(hs, tp, gamma, coef_type="goda") == beta


def test_jonswap_unit_spectrum():
    assert plw.get_jonswap_unit_spectrum(1, 1) == np.exp(-1.25)
    assert plw.get_jonswap_unit_spectrum(np.inf, 1) == 0.0


def test_jonswap_spectrum():
    gamma = 1
    beta = (
        0.06238
        * (1.094 - 0.01915 * np.log(gamma))
        / (0.230 + 0.0336 * gamma - 0.185 / (1.9 + gamma))
    )

    assert plw.get_jonswap_spectrum(1, 1, 2 * np.pi, gamma) == beta * np.exp(-1.25)
    assert plw.get_jonswap_spectrum(1, 1, np.inf, 1) == 0.0
    assert plw.get_jonswap_spectrum(1, 1, 0.1, 1) == 0.0


def test_rel_dir():
    assert plw.get_rel_dir(0, np.pi) == np.pi
    assert plw.get_rel_dir(0, -np.pi / 2) == np.pi / 2
    assert plw.get_rel_dir(0, np.pi / 2) == np.pi / 2
    assert plw.get_rel_dir(0, 2 * np.pi) == 0
    assert plw.get_rel_dir(0, 1.5 * np.pi) == np.pi / 2


def test_2n_cosine_spread():
    mean_dir = 0
    wave_dir = np.linspace(0, 2 * np.pi, 100)
    rel_dir = plw.get_rel_dir(mean_dir, wave_dir)
    n = 1
    coef_db = [[1, 2 / np.pi], [2, 8 / (3 * np.pi)]]
    rtol = 1e-5
    for (n, coef) in coef_db:
        coef_func = plw.get_2n_cosine_spread(rel_dir, n)[0]
        assert np.isclose(coef, coef_func, rtol=rtol)


def test_2n_half_cosine_spread():
    mean_dir = 0
    wave_dir = np.linspace(0, 2 * np.pi, 100)
    rel_dir = plw.get_rel_dir(mean_dir, wave_dir)
    n = 1
    coef_db = [[1, 1 / np.pi], [2, 4 / (3 * np.pi)]]
    rtol = 1e-5
    for (n, coef) in coef_db:
        coef_func = plw.get_2n_half_cosine_spread(rel_dir, n)[0]
        assert np.isclose(coef, coef_func, rtol=rtol)


def test_spread_parameter():
    norm_omega = 1
    smax = 1
    assert plw.get_spread_parameter(norm_omega, smax) == 1.0
