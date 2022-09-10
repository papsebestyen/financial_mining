import logging
from typing import TYPE_CHECKING

from tqdm import tqdm

from ..config import BASE_THREAD_URL
from ..helpers import get_soup
from .parse_data import parse_thread_data
from .selectors import base_selector, filtered_selector
from .thread_helpers import parse_last_thread, parse_topic_urls

if TYPE_CHECKING:
    from .selectors import SelectorClass

logging.basicConfig(format="%(asctime)s - %(message)s", datefmt="%y-%m-%d %H:%M:%S")


def get_all_thread(url: str, selector: "SelectorClass", extra_features: dict = None):
    extra_features = extra_features or dict()
    thread_data = []
    soup = get_soup(url, {selector.pages_path: 1})
    if soup is None:
        return list()
    last_thread = parse_last_thread(soup, selector=selector)
    logging.warning(f"Scrape thread info from {url} with {last_thread} page(s)")
    for page_num in tqdm(range(1, last_thread + 1)):
        soup = get_soup(url, {selector.pages_path: page_num})
        threads_soup = soup.find_all("div", class_=selector.thread_class)
        thread_data.extend(
            [
                {**parse_thread_data(thread, selector=selector), **extra_features}
                for thread in threads_soup
            ]
        )
    return thread_data


def get_thread_data():
    return get_all_thread(
        url=BASE_THREAD_URL,
        selector=base_selector,
    )


def get_topic_data():
    data_filtered = []
    for topic_name, topic_url in parse_topic_urls(get_soup(BASE_THREAD_URL)):
        data_filtered.extend(
            get_all_thread(
                url=topic_url,
                selector=filtered_selector,
                extra_features={"topic": topic_name},
            )
        )
    return data_filtered
