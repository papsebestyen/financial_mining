from ..time_convert import parse_datestring


def parse_message_text(soup):
    text_elem = soup.find("div", class_="text")
    if text_elem:
        return text_elem.text.strip()
    else:
        return soup.find("div", class_="prevcomment").find("i").text.strip()


def parse_message_username(soup):
    comment_data_elem = soup.find("div", class_="commentdata")
    username_elem = comment_data_elem.find("a", class_="username")
    if username_elem:
        return username_elem.text.strip()
    else:
        deleted_user_elem = comment_data_elem.find("i")
        if deleted_user_elem:
            return deleted_user_elem.text.strip()
        else:
            return comment_data_elem.find("span").text.strip()


def parse_message_date(soup):
    return parse_datestring(soup.find("span", class_="date").text)


def parse_message_id(soup):
    return int(soup.find("div", class_="id").text.replace("#", ""))


def parse_message_prev_id(soup):
    prev_message_elem = soup.find("div", class_="prevcomment")
    prev_id_elem = prev_message_elem.find("a")
    if prev_id_elem:
        return int(prev_id_elem.text.replace("#", ""))
    else:
        return prev_message_elem.text.strip()


def parse_message_like(soup):
    return int(soup.find("span", {"class": "vote", "data-vote": "1"}).text.strip())


def parse_message_unlike(soup):
    return int(soup.find("span", {"class": "vote", "data-vote": "-1"}).text.strip())


def parse_message_data(soup):
    text = parse_message_text(soup)
    username = parse_message_username(soup)
    date = parse_message_date(soup)
    comment_id = parse_message_id(soup)
    if text != "Törölt hozzászólás":
        like = parse_message_like(soup)
        unlike = parse_message_unlike(soup)
    else:
        like = unlike = None
    prev_id = parse_message_prev_id(soup)

    return {
        "text": text,
        "username": username,
        "date": date,
        "id": comment_id,
        "like": like,
        "unlike": unlike,
        "prev_id": prev_id,
    }
