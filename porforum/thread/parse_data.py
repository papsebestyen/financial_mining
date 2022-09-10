from bs4 import BeautifulSoup

from ..time_convert import parse_datestring
from .selectors import SelectorClass


def parse_thread_name(soup: BeautifulSoup, selector: SelectorClass) -> str:
    return soup.find("div", class_=selector.thread_name).find("a").text.strip()


def parse_thread_url(soup: BeautifulSoup, selector: SelectorClass) -> str:
    return soup.find("div", class_=selector.thread_name).find("a")["href"]


def parse_thread_id(soup: BeautifulSoup, selector: SelectorClass) -> int:
    return int(
        soup.find("div", class_=selector.thread_name).find("a")["href"].split("/")[-1]
    )


def parse_thread_comment_count(soup: BeautifulSoup, selector: SelectorClass) -> int:
    return int(
        soup.find("div", class_=selector.comment_count).text.strip().replace(" ", "")
    )


def parse_thread_date_user(soup: BeautifulSoup):
    date_elem = soup.find("div", class_="date").find("div")
    if date_elem.find("a"):
        user = date_elem.find("a").text.strip()
    elif date_elem.find("i"):
        user = date_elem.find("i").text.strip()
    [e.extract() for e in date_elem.find_all(["br", "a", "i"])]
    date = parse_datestring(date_elem.text.strip())
    return date, user


def parse_thread_data(soup: BeautifulSoup, selector: SelectorClass) -> dict:
    thread_name = parse_thread_name(soup, selector=selector)
    thread_id = parse_thread_id(soup, selector=selector)
    thread_url = parse_thread_url(soup, selector=selector)
    thread_comment_count = parse_thread_comment_count(soup, selector=selector)
    date, user = parse_thread_date_user(soup)
    return {
        "thread_id": thread_id,
        "thread_name": thread_name,
        "thread_url": thread_url,
        "thread_comment_count": thread_comment_count,
        "date": date,
        "user": user,
    }
