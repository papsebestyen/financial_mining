from porforum.time_convert import parse_datestring


def parse_thread_stats_elem(soup):
    thread_elem = soup.find("div", class_="topic-head")
    return thread_elem


def parse_thread_stats_start(soup):
    thread_elem = parse_thread_stats_elem(soup).find("div", class_="pull-left")
    founder = thread_elem.find("a").text.strip()
    start_date = thread_elem.contents[-1].strip()
    return founder, parse_datestring(start_date)


def parse_thread_stats_title(soup):
    title_elem = parse_thread_stats_elem(soup).find("h1")
    title = title_elem.text.strip()
    summary_type = title_elem["data-target"].strip().replace("#", "")
    return title, summary_type


def parse_thread_stats_summary(soup, summary_type: str):
    summary_elem = parse_thread_stats_elem(soup).find("div", {"id": summary_type})
    [e.decompose() for e in summary_elem.find_all()]
    return summary_elem.text.strip()


def parse_thread_stats_data(soup):
    founder, start_date = parse_thread_stats_start(soup)
    title, summary_type = parse_thread_stats_title(soup)
    summary = parse_thread_stats_summary(soup, summary_type=summary_type)
    return {
        "founder": founder,
        "start_date": start_date,
        "title": title,
        "summary_type": summary_type,
        "summary": summary,
    }
