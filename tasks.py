from pathlib import Path

import pandas as pd
from invoke import task

from porforum.message.scrape import get_thread_message_generator
from porforum.thread.scrape import get_thread_data, get_topic_data

DATA_PATH = Path("data")
DATA_PATH.mkdir(exist_ok=True)
MESSAGES_PATH = DATA_PATH / "messages"
MESSAGES_PATH.mkdir(exist_ok=True)


@task(aliases=["dt"])
def download_thread_data(cli, with_topics=True):
    thread_data = get_thread_data()
    df = pd.DataFrame(thread_data).set_index("thread_id")
    df.to_parquet(DATA_PATH / "threads.parquet")
    if with_topics:
        topic_data = get_topic_data()
        topic_df = pd.DataFrame(topic_data).set_index("thread_id")[["topic"]]
        topic_df.to_parquet(DATA_PATH / "topics.parquet")


@task(aliases=["dm"])
def download_message_data(cli, update=False, verbose=True):
    thread_dict = pd.read_parquet(DATA_PATH / "threads.parquet")["thread_url"].to_dict()
    if not update:
        [(thread_dict.pop(int(p.stem))) for p in MESSAGES_PATH.iterdir()]
    for thread_id, thread_data in get_thread_message_generator(
        thread_dict, verbose=verbose
    ):
        thread_data = pd.DataFrame(thread_data)
        if not thread_data.empty:
            thread_data.astype({"prev_id": "string"}).set_index("id").to_parquet(
                MESSAGES_PATH / f"{thread_id}.parquet"
            )
