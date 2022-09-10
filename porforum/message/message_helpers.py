from urllib.parse import parse_qs, urlparse

from bs4 import BeautifulSoup


def parse_first_page(soup):
    pagination_elem = soup.find("ul", class_="pagination")
    if not pagination_elem:
        return 1
    page_elems = pagination_elem.find_all("a", class_="page-link")
    first_url = [link for link in page_elems if link.text.find("első") != -1][0]["href"]
    first = int(
        parse_qs(urlparse(first_url).query,)[
            "oldal"
        ][0]
    )
    return first


def parse_message_elems(soup):
    return soup.find("div", class_="leftPage").find_all(
        "div", class_="comment", recursive=False
    )


def parse_message_user_ranks(soup):
    avatar = soup.find("div", class_="avatar")["data-content"]
    ranks = BeautifulSoup(avatar, "html.parser").find_all("span")
    rank_data = {
        rank.find("i")["class"][0].replace("icon-", ""): int(rank.text)
        for rank in ranks
        if rank.attrs
    }
    return rank_data
