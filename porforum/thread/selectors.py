from dataclasses import dataclass


@dataclass
class SelectorClass:
    pages_path: str = None
    thread_name: str = "topicname"
    thread_class: str = "topic"
    comment_count: str = "commentcount"
    pagination: str = "pagination"
    page_item: str = "page-item"


base_selector = SelectorClass(pages_path="o")
filtered_selector = SelectorClass(pages_path="oldal")
