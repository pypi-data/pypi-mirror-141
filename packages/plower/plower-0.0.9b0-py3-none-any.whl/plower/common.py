"""
This file contains general functions used by other functions
"""

import xml.etree.ElementTree as ET
from collections import deque

# import argparse
# import sys
# from functools import partial
from pathlib import Path
from time import gmtime, strftime

import pandas as pd

# import numpy as np

__author__ = "Chaitanya Kesanapalli"
__copyright__ = "Chaitanya Kesanapalli"
__license__ = "BSD 3-Clause"


def add_logpath(logger, log_file_prefix, log_dir="logs", **kwargs):
    """
    Update Logger with log file path.

    Here the log file has date and time as suffix.

    Parameters
    ----------
    logger : loguru.logger
        logger object
    log_dir: str or Path, optional
        Directory of the log file, default is "log"
    log_file_prefix : str
        Prefix of the log file
    """
    (log_dir := Path(log_dir)).mkdir(parents=True, exist_ok=True)
    time_str = strftime("%Y_%m_%d_%H_%M_%S", gmtime())
    logger.add(log_dir / f"{log_file_prefix}_{time_str}.log", **kwargs)


def count(iterable):
    """
    Count the number of items that `iterable` yields.
    Equivalent to the expression `len(iterable)`

    Author: Wouter Bolsterlee

    Parameters
    ----------
    iterable : iterable

    Returns
    -------
    count : int
    """
    if hasattr(iterable, "__len__"):
        count = len(iterable)

    d = deque(enumerate(iterable, 1), maxlen=1)
    count = d[0][0] if d else 0
    return count


def get_heading(logger, title, level=0, total_len=79):
    """
    Converts 'string' to a heading ('== string ==')

    Parameters
    ----------
    logger : loguru.logger
        logger object
    title : str
        title string before formatting
    level : int, optional
        Heading type ranging from 0 to 2, by default 0
    total_len : int, optional
        Maximum desired length of heading, by default 79

    Returns
    -------
    logger.info
        Outputs logger.info(string)
    """
    title_len = len(title)

    if title_len > total_len:
        logger.warning(
            f"Title length ({title_len}) is greater than Total length ({total_len})"
        )
        title_len = total_len - 2

    line1_len = (total_len - title_len) // 2
    line2_len = total_len - (title_len + line1_len)

    if level == 0:
        line_chr = "="
    elif level == 1:
        line_chr = "-"
    elif level == 2:
        line_chr = ":"
    else:
        line_chr = "."

    line1 = line_chr * line1_len
    line2 = line_chr * line2_len
    formated_heading = " ".join([line1, title, line2])

    return logger.info(formated_heading)


def xrmax(dataset, full_dataset=None):
    """
    Return maxima of the dataset with all coordinates

    Parameters
    ----------
    dataset : scalar, array, Variable, DataArray or Dataset
        dataset
    full_dataset : scalar, array, Variable, DataArray or Dataset, optional
        superset of the dataset, by default dataset

    Returns
    -------
    dataset_maxima : float
        maxima of the dataset
    """
    if not full_dataset:
        full_dataset = dataset
    dataset_maxima = full_dataset.where(
        full_dataset == dataset.max(), drop=True
    ).squeeze()
    return dataset_maxima


def xml2dict(xml, *args, **kwargs):
    """Converts xml of list element to dict of list"""
    xml_str = ET.tostring(xml)
    xml_dict = pd.read_xml(xml_str).to_dict(*args, **kwargs)
    return xml_dict
