import re
from datetime import datetime, timedelta

time_pattern = re.compile(r"\d+")
day_pattern = re.compile(r"\w+")

day_dict = {
    "hétfő": 0,
    "kedd": 1,
    "szerda": 2,
    "csütörtök": 3,
    "péntek": 4,
    "szombat": 5,
    "vasárnap": 6,
}


def parse_time(date_str: str):
    return [int(t) for t in time_pattern.findall(date_str)]


def parse_today(date_str: str):
    now = datetime.now()
    return datetime(now.year, now.month, now.day, *parse_time(date_str))


def parse_dow(date_str: str):
    return day_dict[day_pattern.match(date_str).group(0)]


def parse_daystring(date_str: str):
    now = datetime.now()
    dow = parse_dow(date_str)
    if dow == now.weekday():
        day_delta = 7
    elif dow < now.weekday():
        day_delta = now.weekday() - dow
    else:
        day_delta = 7 - (dow - now.weekday())
    return datetime(now.year, now.month, now.day, *parse_time(date_str)) - timedelta(
        days=day_delta
    )


def parse_datestring(date_str: str):
    if len(parse_time(date_str)) == 5:
        return datetime(*parse_time(date_str))
    elif date_str.startswith("ma"):
        return parse_today(date_str)
    else:
        return parse_daystring(date_str)
