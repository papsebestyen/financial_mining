import logging

import requests
from bs4 import BeautifulSoup

from .config import VERBOSE_REQUEST

logging.basicConfig(format="%(asctime)s - %(message)s", datefmt="%y-%m-%d %H:%M:%S")


def get_soup(url: str, params: dict = None, verbose: bool = VERBOSE_REQUEST):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return BeautifulSoup(response.content, "html.parser", from_encoding="utf-8")
    else:
        if verbose:
            logging.warning(f"Error {response.status_code} for {url}")
        if response.status_code == 404:
            return None
        elif response.status_code == 502:
            return get_soup(url=url, params=params)
        response.raise_for_status()
