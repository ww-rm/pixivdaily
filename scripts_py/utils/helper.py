from datetime import datetime, timedelta, timezone
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


def nowbeijing():
    return datetime.now(timezone(timedelta(hours=8)))


def pximg_reverse_proxy(url: str) -> str:
    # 反向代理, 替换 url
    return url.replace("i.pximg.net", "i.pixiv.re")


def jinja_env(temp_dir: Path, filters: dict):
    """"""
    env = Environment(loader=FileSystemLoader(temp_dir))
    env.filters.update(filters)
    return env
