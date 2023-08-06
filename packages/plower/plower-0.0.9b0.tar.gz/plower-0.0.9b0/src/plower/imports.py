"""Imports the NDBC data and converts to pandas.DataFrame and perform statistics."""

# from functools import partial
# from pathlib import Path
import xml.etree.ElementTree as ET

# from io import StringIO
from collections.abc import Iterable
from itertools import chain

import numpy as np
import pandas as pd
import requests
from loguru import logger

import plower as plw

__author__ = "Chaitanya Kesanapalli"
__copyright__ = "Chaitanya Kesanapalli"
__license__ = "BSD 3-Clause"


def get_ndbc_db_url(station_id, year):
    """
    Return URL to the NDBC database of the buoy.

    Parameters
    ----------
    station_id : str
        Buoy station ID (5 lettered ID may contains numbers or alphabet).
    year : int
        year of the database

    Returns
    -------
    ndbc_db_url : str
        URL to the NDBC database of the buoy
    """
    ndbc_db_url = "".join(
        [
            "https://www.ndbc.noaa.gov/view_text_file.php?filename=",
            f"{station_id}h{year}.txt.gz&dir=data/historical/stdmet/",
        ]
    )
    return ndbc_db_url


def get_ndbc_df(path, tp_range=(0, 24), hs_range=(0, 10), additional_data_names=[]):
    """
    Return the NDBC buoy data for a range of peak period (tp) and significant
    height (hs).
    The description of data is available at https://www.ndbc.noaa.gov/measdes.shtml.


    Parameters
    ----------
    path : str
        URL of an year NDBC buoy database
    tp_range : tuple, optional
        Minimum and Maximum of peak periods, by default (0,21)
    hs_range : tuple, optional
        Minimum and Maximum of significant heights, by default (0,10)
    additional_data_names : iterable
        Names of the data to include in output apart from ("DPD", "WVHT", "MWD").
        The data names details are available at https://www.ndbc.noaa.gov/measdes.shtml.

    Returns
    -------
    buoy_db : pandas.DataFrame
        Dataframe of an year NDBC buoy database.
        By default returns ("DPD", "WVHT", "MWD").

    Notes
    -----
        The default tp and hs ranges are choosen according to SAM software
        https://sam.nrel.gov/marine-energy.html

    """
    columns = list(set(chain(["DPD", "WVHT", "MWD"], additional_data_names)))
    try:
        buoy_db = pd.read_csv(path, sep=r"\s+", skiprows=[1]).loc[:, columns]
    except Warning:
        logger.warning(f"Given path contains no data\n{path}")
        return None
    buoy_db = buoy_db[buoy_db["DPD"] >= tp_range[0]]
    buoy_db = buoy_db[buoy_db["DPD"] <= tp_range[1]]
    buoy_db = buoy_db[buoy_db["WVHT"] >= hs_range[0]]
    buoy_db = buoy_db[buoy_db["WVHT"] <= hs_range[1]]

    # To make the angle range -180 to 180 deg
    buoy_db.loc[buoy_db["MWD"] > 180.0, "MWD"] -= 360

    return buoy_db


def get_sam_dataset():
    """
    Returns a sample significant height, energy period and mean
    direction ranges based on the SAM model wave resource ranges.
    https://sam.nrel.gov/marine-energy.html

    """
    sam_dataset = {
        "hs_edges": np.arange(0, 10.5, 0.5),
        "tp_edges": np.arange(0.0, 22.0, 1.0),
        "dir_edges": np.arange(-180, 200, 20),
    }
    sam_dataset["hs_centers"] = 0.5 * (
        sam_dataset["hs_edges"][:-1] + sam_dataset["hs_edges"][1:]
    )
    sam_dataset["tp_centers"] = 0.5 * (
        sam_dataset["tp_edges"][:-1] + sam_dataset["tp_edges"][1:]
    )
    sam_dataset["dir_centers"] = 0.5 * (
        sam_dataset["dir_edges"][:-1] + sam_dataset["dir_edges"][1:]
    )
    return sam_dataset


def get_probability_of_occurrence(
    station_id,
    year_range=range(2011, 2021),
    tp2te=0.892,
    hs_edges=np.arange(0, 10.5, 0.5),
    dir_edges=np.arange(-180, 200, 20),
    te_edges=np.arange(0.0, 22.0, 1.0),
    norm_factor=1.0,
):
    """
    Return probability of occurrence for a ocean wave data at a buoy location.

    Parameters
    ----------
    station_id : str
        Buoy station ID (5 lettered ID may contains numbers or alphabet).
    tp2te : float, optional
        Conversion factor from peak peroid to energy period. The default is 0.892.
    year_range : iterable, optional
        Range of year for the database selection. The default is range(2011,2021).
    hs_edges : np.ndarray, optional
        Array of significant heights. The default is np.arange(0,10.5,0.5).
    dir_edges : np.ndarray, optional
        Array of mean directions. The default is np.arange(-180,200,20).
    te_edges : np.ndarray, optional
        Array of energy periods. The default is np.arange(0.0,22.0,1.0).
    sam_wave_res_path : str or pathlib.Path, optional
        Path of the SAM wave resource datafile. The default is None.
    norm_factor : float, optional
        Histogram is normalized such that the sum of the histograms is norm_factor.
        The default is 1.0.

    Returns
    -------
    te_hs_dir_hist : np.ndarray
        Histogram of energy period, significant height and mean direction.
        Note: te_hs_dir_hist is normalized to the

    """
    noaa_url_paths = (get_ndbc_db_url(station_id, year) for year in year_range)
    noaa_db = pd.concat(get_ndbc_df(path) for path in noaa_url_paths)
    noaa_db["Te"] = tp2te * noaa_db["DPD"]

    te_hs_dir_hist, _ = np.histogramdd(
        noaa_db.loc[:, ["Te", "WVHT", "MWD"]].values,
        bins=(te_edges, hs_edges, dir_edges),
    )
    te_hs_dir_hist *= norm_factor / np.sum(te_hs_dir_hist)

    # te_hs_hist = te_hs_dir_hist.sum(axis=2).T
    # te_dir_hist = te_hs_dir_hist.sum(axis=1).T
    # dir_hs_hist = te_hs_dir_hist.sum(axis=0)

    # te_means = 0.5 * (te_edges[:-1] + te_edges[1:])
    # hs_means = 0.5 * (hs_edges[:-1] + hs_edges[1:])
    # dir_means = 0.5 * (dir_edges[:-1] + dir_edges[1:])

    return te_hs_dir_hist


def get_ndbc_buoy_details(station_id):
    """
    Returns buoy details from the NDBC website.

    The details are taken from the
    https://www.ndbc.noaa.gov/metadata/stationmetadata.xml

    Parameters
    ----------
    station_id : str or iterable
        Buoy station ID (5 lettered ID may contains numbers or alphabet).

    Returns
    -------
    station_dbs : List of dict
        Details of the NDBC buoy.
    """

    if isinstance(station_id, str):
        station_ids = (station_id,)

    elif isinstance(station_id, Iterable):
        station_ids = tuple(station_id)

        for idx, buoy_station_each in enumerate(station_ids):
            if not isinstance(buoy_station_each, str):
                raise TypeError(
                    f"station_id[{idx}]: {buoy_station_each} is not a string"
                )
    else:
        raise TypeError(f"station_id: {station_id} is neither string nor iterable")

    response = requests.get("https://www.ndbc.noaa.gov/metadata/stationmetadata.xml")

    root = ET.fromstring(response.content)

    station_dbs = [
        dict(child.attrib, **plw.xml2dict(child, "list"))
        for child in root
        for buoy_station_each in station_ids
        if child.attrib["id"] == str(buoy_station_each).upper()
    ]
    return station_dbs
