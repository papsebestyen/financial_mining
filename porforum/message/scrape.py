import logging

from tqdm import tqdm

from ..config import VERBOSE_MESSAGE_ITERATION, VERBOSE_THREAD_ITERATION
from ..helpers import get_soup
from .message_helpers import parse_first_page, parse_message_elems
from .parse_message import parse_message_data

logging.basicConfig(format="%(asctime)s - %(message)s", datefmt="%y-%m-%d %H:%M:%S")


def parse_all_message(
    soup, progress: bool = False, verbose: bool = VERBOSE_MESSAGE_ITERATION
):
    data = []
    msgs = parse_message_elems(soup)
    if progress:
        msgs = tqdm(msgs)
    for msg in msgs:
        msgs_data = parse_message_data(msg)
        if verbose:
            logging.warning(f"Parsing message: {msgs_data['id']}")
        data.append(msgs_data)
    return data


def get_all_message(url: str, limit: int = 100):
    data = []
    soup = get_soup(url, params={"oldal": 1, "limit": limit})
    first_page = parse_first_page(soup)
    for page in tqdm(range(1, first_page + 1)):
        soup = get_soup(url, params={"oldal": page, "limit": limit})
        data.extend(parse_all_message(soup))
    return data


def get_thread_message_generator(
    thread_dict: dict, verbose: bool = VERBOSE_THREAD_ITERATION
):
    for thread_id, thread_url in thread_dict.items():
        logging.warning(f"Get message data from {thread_id} thread. URL: {thread_url}")
        thread_data = get_all_message(url=thread_url)
        yield thread_id, thread_data
