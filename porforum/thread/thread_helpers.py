import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bs4 import BeautifulSoup

    from .selectors import SelectorClass


def parse_last_thread(soup: "BeautifulSoup", selector: "SelectorClass") -> int:
    pagination_elem = soup.find("ul", class_=selector.pagination)
    if pagination_elem is None:
        return 1
    pages = pagination_elem.find_all("li", class_=selector.page_item)
    pages = [int(page.text) for page in pages if re.search(r"\d", page.text)]
    return max(pages)


def parse_topic_urls(soup: "BeautifulSoup"):
    forum_elem = soup.find("div", class_="forumOperations")
    filter_elem = forum_elem.find("div", class_="filter")
    thread_elems = filter_elem.find_all("a", class_=None)
    return [(thread.text.casefold(), thread["href"]) for thread in thread_elems]
