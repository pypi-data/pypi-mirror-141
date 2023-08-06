"""
This file contains functions to compute wave spectrums
"""

# import argparse
# import logging
# import sys
# from functools import partial
# from pathlib import Path

import numpy as np
import scipy as sp
import xarray as xr
from scipy.integrate import simpson

# from plower import __version__

__author__ = "Chaitanya Kesanapalli"
__copyright__ = "Chaitanya Kesanapalli"
__license__ = "BSD 3-Clause"

# _logger = logging.getLogger(__name__)

# =============================================================================
# Pierson-Moskowitz Spectrum
# =============================================================================


def get_pm_coef(hs, tp):
    """
    Compute the Coefficient of Pierson-Moskowitz Spectrum.

    Parameters
    ----------
    hs : scalar, array, Variable, DataArray or Dataset
        Significant Height.
    tp : scalar, array, Variable, DataArray or Dataset
        Peak Period.

    Returns
    -------
    pm_coef : scalar, array, Variable, DataArray or Dataset
        Coefficient of Pierson-Moskowitz Spectrum.

    """
    pm_coef = (5 / (32 * np.pi)) * hs**2 * tp
    return pm_coef


def get_pm_unit_spectrum(norm_omega):
    """
    Compute the proportional term of Pierson-Moskowitz Spectrum.

    Parameters
    ----------
    norm_omega : scalar, array, Variable, DataArray or Dataset
        Frequency normalized with spectrum peak frequency.

    Returns
    -------
    pm_unit_spectrum : scalar, array, Variable, DataArray or Dataset
        Proportional term of Pierson-Moskowitz Spectrum.

    """
    with np.errstate(divide="ignore", invalid="ignore"):
        pm_unit_spectrum = xr.where(
            norm_omega != 0.0,
            np.power(norm_omega, -5.0) * np.exp(-1.25 * np.power(norm_omega, -4.0)),
            0.0,
        )
    return pm_unit_spectrum


def get_pm_spectrum(hs, tp, omega):
    """
    Compute the Pierson-Moskowitz Spectrum.


    Parameters
    ----------
    hs : scalar, array, Variable, DataArray or Dataset
        Significant Height.
    tp : scalar, array, Variable, DataArray or Dataset
        Peak Period.
    omega : scalar, array, Variable, DataArray or Dataset
        Frequency (rad/s).

    Returns
    -------
    pm_spectrum : scalar, array, Variable, DataArray or Dataset
        Pierson-Moskowitz Spectrum.

    References
    ----------
        Jensen, J. J. (2001). Load and global response of ships. Elsevier.


    """
    norm_omega = omega * tp / (2 * np.pi)
    pm_spectrum = get_pm_coef(hs, tp) * get_pm_unit_spectrum(norm_omega)
    return pm_spectrum


def get_pm_spectrum_te(hs, te, omega):
    """
    Compute the Pierson-Moskowitz Spectrum.


    Parameters
    ----------
    hs : scalar, array, Variable, DataArray or Dataset
        Significant Height.
    tpe : scalar, array, Variable, DataArray or Dataset
        Energy Period.
    omega : scalar, array, Variable, DataArray or Dataset
        Frequency (rad/s).

    Returns
    -------
    pm_spectrum : scalar, array, Variable, DataArray or Dataset
        Pierson-Moskowitz Spectrum.

    References
    ----------
        Jensen, J. J. (2001). Load and global response of ships. Elsevier.

    """

    pm_spectrum = (
        131.5 * hs**2 * te**-4 * omega**-5 * np.exp(-1054 * (te * omega) ** -4)
    )
    return pm_spectrum


# =============================================================================
# JONSWAP Spectrum
# =============================================================================
def get_jonswap_coef(hs, tp, gamma, coef_type="abs"):
    """
    Compute the Coefficient of JONSWAP Spectrum.

    Parameters
    ----------
    hs : scalar, array, Variable, DataArray or Dataset
        Significant Height.
    tp : scalar, array, Variable, DataArray or Dataset
        Peak Period.
    gamma : scalar, array, Variable, DataArray or Dataset
        Peak Enchancement Factor.

    Returns
    -------
    jonswap_coef : scalar, array, Variable, DataArray or Dataset
        Coefficient of JONSWAP Spectrum.

    """
    g = 9.80665

    if coef_type == "goda":
        beta = (
            0.06238
            * (1.094 - 0.01915 * np.log(gamma))
            / (0.230 + 0.0336 * gamma - 0.185 / (1.9 + gamma))
        )
        jonswap_coef = beta * hs**2 * tp
    elif coef_type == "pm":
        jonswap_coef = get_pm_coef(hs, tp)
    elif coef_type == "navy":
        # Reference:
        # Lee, W. T., & Bales, S. L. (1980). A Modified JONSWAP Spectrum
        # Dependent Only On Wave Height and Period. DAVID W TAYLOR NAVAL SHIP
        # RESEARCH AND DEVELOPMENT CENTER BETHESDA MD SHIP PERFORMANCE DEPT.
        alpha = (16.942 * hs**1.375) / (g**1.375 * tp * 2.75)
        jonswap_coef = alpha * g**2 * (2 * np.pi) ** -4 * tp**5
    elif coef_type == "glenn":
        # References:
        # Ewans, K., & McConochie, J. (2021). Optimal methods for estimating
        # the JONSWAP spectrum peak enhancement factor from measured and
        # hindcast wave data. Journal of Offshore Mechanics and Arctic
        # Engineering, 143(2), 021202.

        # Amurol Jamal, S., Ewans, K., & Sheikh, R. (2014, March). Measured Wave
        # Spectra Offshore Sabah & Sarawak, Malaysia. In Offshore Technology
        # Conference-Asia. OnePetro.
        denominator = 1.15 + 0.1688 * gamma - 0.925 / (1.909 + gamma)
        jonswap_coef = (5 / 16) * hs**2 * tp / denominator

    elif coef_type == "philips":
        # References:
        # Ewans, K., & McConochie, J. (2021). Optimal methods for estimating
        # the JONSWAP spectrum peak enhancement factor from measured and
        # hindcast wave data. Journal of Offshore Mechanics and Arctic
        # Engineering, 143(2), 021202.
        alpha = 0.0081

        jonswap_coef = alpha * g**2 * tp**5 * (2 * np.pi) ** -4

    elif coef_type in ["dnv", "abs"]:
        # References:
        # DNV, Environmental Conditions and Environmental Loads, 2010.
        # [Online] Available: https://rules.dnvgl.com/docs/pdf/DNV/codes/docs/
        # 2010-10/RP-C205.pdf. Accessed on: Mar. 31, 2017.
        jonswap_coef = (1 - 0.287 * np.log(gamma)) * get_pm_coef(hs, tp)

    return jonswap_coef


def get_jonswap_unit_spectrum(norm_omega, gamma):
    """
    Compute the proportional term of JONSWAP Spectrum.

    Parameters
    ----------
    norm_omega : scalar, array, Variable, DataArray or Dataset
        Frequency normalized with spectrum peak frequency.
    gamma : scalar, array, Variable, DataArray or Dataset
        Peak Enchancement Factor.

    Returns
    -------
    jonswap_unit_spectrum : scalar, array, Variable, DataArray or Dataset
        Proportional term of JONSWAP Spectrum.

    """
    sigmas = np.where(norm_omega <= 1, 0.07, 0.09)
    jonswap_unit_spectrum = get_pm_unit_spectrum(norm_omega) * gamma ** np.exp(
        -0.5 * ((norm_omega - 1) / sigmas) ** 2
    )
    return jonswap_unit_spectrum


def get_jonswap_spectrum(hs, tp, omega, gamma, coef_type="goda"):
    """
    Compute the JONSWAP Spectrum.

    Parameters
    ----------
    hs : scalar, array, Variable, DataArray or Dataset
        Significant Height.
    tp : scalar, array, Variable, DataArray or Dataset
        Peak Period.
    omega : scalar, array, Variable, DataArray or Dataset
        Frequency (rad/s).
    gamma : scalar, array, Variable, DataArray or Dataset
        Peak Enchancement Factor.

    Returns
    -------
    jonswap_spectrum : scalar, array, Variable, DataArray or Dataset
        JONSWAP Spectrum.

    References
    ----------
        Jensen, J. J. (2001). Load and global response of ships. Elsevier.

    """
    norm_omega = omega * tp / (2 * np.pi)

    if coef_type == "abs":
        # https://ww2.eagle.org/content/dam/eagle/rules-and-guides/current/offshore/238_Guidance_Notes_on_Selecting_Design_Wave_by_Long_Term_Stochastic_Method/Long_Term_Design_Wave_GN_e.pdf

        unit_spectrum = get_jonswap_unit_spectrum(norm_omega, gamma)
        unit_spectrum_int = simpson(unit_spectrum, omega)
        jonswap_coef = hs**2 / (4.004**2 * unit_spectrum_int)
        jonswap_spectrum = jonswap_coef * unit_spectrum

    else:
        jonswap_spectrum = get_jonswap_coef(
            hs, tp, gamma, coef_type=coef_type
        ) * get_jonswap_unit_spectrum(norm_omega, gamma)

    return jonswap_spectrum


# =============================================================================
# Directional Spectrum
# D(psi, theta) = coef(psi) * unit_spectrum(tp, psi, theta)
# =============================================================================


def get_rel_dir(mean_dir, wave_dir):
    """
    Relative direction with the mean direction.


    Parameters
    ----------
    mean_dir : scalar, Variable, DataArray or Dataset
        Mean wave direction.
    wave_dir : scalar, Variable, DataArray or Dataset
        Wave direction.

    Returns
    -------
    rel_dir_sym : scalar, array, Variable, DataArray or Dataset
        Relative direction with the mean direction ranging from 0 to pi.

    Note
    -----
        Input mean_dir and wave_dir as xarray variables for boardcasting
        mean_dir array and wave_dir array to a 2D rel_dir.


    """
    rel_dir = np.abs(mean_dir - wave_dir) % (2 * np.pi)
    rel_dir_sym = xr.where(rel_dir > np.pi, 2 * np.pi - rel_dir, rel_dir)
    return rel_dir_sym


def get_2n_cosine_spread(rel_dir, n):
    """
    Cosine 2l-power type directional spreading function.

    Parameters
    ----------
    rel_dir : scalar, array, Variable, DataArray or Dataset
        Relative direction with the mean direction.
    n : scalar, array, Variable, DataArray or Dataset
        Cosine power.

    Returns
    -------
    spread : scalar, array, Variable, DataArray or Dataset
        Directional spreading.

    """
    coef = np.pi**-0.5 * sp.special.gamma(1 + n) / sp.special.gamma(0.5 + n)
    spread = xr.where(
        np.abs(rel_dir) < np.pi / 2, coef * ((np.cos(rel_dir)) ** 2) ** n, 0.0
    )
    return spread


def get_2n_half_cosine_spread(rel_dir, n=1):
    """
    Half cosine 2l-power type directional spreading function.

    Parameters
    ----------
    rel_dir : scalar, array, Variable, DataArray or Dataset
        Relative direction with the mean direction.
    n : scalar, array, Variable, DataArray or Dataset
        Spreading Parameter.

    Returns
    -------
    spread : scalar, array, Variable, DataArray or Dataset
        Directional spreading.

    References
    ----------
        Yoshimi Goda (1999) A Comparative Review on the Functional Forms of
        Directional Wave Spectrum, Coastal Engineering Journal, 41:1, 1-20,
        DOI:  https://doi.org/10.1142/S0578563499000024

    """
    coef = (
        (2 ** (2 * n - 1) / np.pi)
        * (sp.special.gamma(1 + n)) ** 2
        / sp.special.gamma(2 * n + 1)
    )

    spread = coef * ((np.cos(rel_dir / 2)) ** 2) ** n

    return spread


def get_wraped_normal_spread(rel_dir, std=10):
    """
    Wrapped-normal directional spreading function.

    Parameters
    ----------
    rel_dir : scalar, array, Variable, DataArray or Dataset
        Relative direction with the mean direction.
    std : scalar, array, Variable, DataArray or Dataset
        Cosine power.

    Returns
    -------
    spread : scalar, array, Variable, DataArray or Dataset
        Directional spreading.

    """
    n_count = 9 / np.sqrt(std)
    n_list = np.arange(1, n_count)
    temp_db = xr.Dataset({}, coords={"n": n_list})
    n_coords = temp_db.coords["n"]
    exp_term = np.exp(-0.5 * (n_coords * std) ** 2) * np.cos(n_coords * rel_dir)
    spread = 1 / (2 * np.pi) + (1 / np.pi) * exp_term.sum(dim=["n"])

    return spread


def get_spread_parameter(norm_omega, smax):
    """
    Compute the spread parameter.

    Parameters
    ----------
    norm_omega : scalar, array, Variable, DataArray or Dataset
        Frequency normalized with spectrum peak frequency.
    smax : scalar, array, Variable, DataArray or Dataset
        Maximum spread parameter.

    Returns
    -------
    spread_parameter : scalar, array, Variable, DataArray or Dataset
        Spread parameter.

    Note
    ----
        Input norm_omega and smax as xarray variables for boardcasting.

    References
    -----------
        Mitsuyasu, Hisashi, et al. "Observations of the directional spectrum of
        ocean WavesUsing a cloverleaf buoy." Journal of Physical Oceanography
        5.4 (1975): 750-760.

    """
    with np.errstate(divide="ignore", invalid="ignore"):
        spread_parameter = smax * xr.where(
            norm_omega <= 1, norm_omega**5, norm_omega**-2.5
        )
    return spread_parameter


def get_mitsuyasu_spread(
    rel_dir, wave_dir_name, smax=12.5, spectrum_type="PM", gamma=1.0
):
    """
    Compute the Mitsuyasu directional unnormalized spreading function.

    Parameters
    ----------
    rel_dir : scalar, array, Variable, DataArray or Dataset
        Relative direction with the mean direction.
    smax : float, optional
        Maximum spread parameter. The default is 10.
    spectrum : {"PM", "JONSWAP"}, optional
        spectrum type. The default is "PM".

    Returns
    -------
    unit_spread : scalar, array, Variable, DataArray or Dataset
        unnormalized spread function.

    """
    norm_omega = np.arange(0, 40, 0.1)
    temp_db = xr.Dataset({}, coords={"local_omega": norm_omega})
    temp_db["rel_dir"] = rel_dir

    if spectrum_type == "PM":
        spectrum = get_pm_unit_spectrum(temp_db.local_omega)
    elif spectrum_type == "JONSWAP":
        spectrum = get_jonswap_unit_spectrum(temp_db.local_omega, gamma)

    n = get_spread_parameter(temp_db.local_omega, smax)
    full_spread = spectrum * get_2n_half_cosine_spread(temp_db.rel_dir, n)

    unnorm_spread = xr.apply_ufunc(
        simpson,
        full_spread,
        input_core_dims=[["local_omega"]],
        kwargs={"x": temp_db.local_omega},
        output_dtypes=float,
    )

    unnorm_spread_int = xr.apply_ufunc(
        simpson,
        unnorm_spread,
        input_core_dims=[[wave_dir_name]],
        kwargs={"x": temp_db[wave_dir_name]},
        output_dtypes=float,
    )

    spread = unnorm_spread / unnorm_spread_int

    return spread


def get_avail_power_simple(hs, tp, density=1000, g=9.80665, kh=np.inf, tp2te=0.8):
    """
    Compute the Available Power in the ocean waves with respect to significant
    height and wave period

    Parameters
    ----------
    hs : scalar, array, Variable, DataArray or Dataset
        ignificant Height.
    tp : scalar, array, Variable, DataArray or Dataset
        Peak Peroid.
    density : scalar, optional
        Water Density (kg/m^3). The default is 1000.
    g : scalar, optional
        Gravity. The default is 9.80665.
    kh : scalar, optional
        wave number to depth ratio. The default is np.inf (deep water).

    Returns
    -------
    avail_power : scalar, array, Variable, DataArray or Dataset
        Available Power in the ocean wave spectrum.

    References
    ----------
        Pecher, A., & Kofoed, J. P. (2017). Handbook of ocean wave energy.
        Springer Nature. pg. 59

    """
    te = tp * tp2te

    pwave_deep = density * g**2 * hs**2 * te / (64 * np.pi)

    return pwave_deep
