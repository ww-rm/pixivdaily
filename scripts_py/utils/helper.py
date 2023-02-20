import logging
import re
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


def get_original_imgurls(illust_id, url: str, page_count: int) -> list:
    illust_date = re.search(r"[0-9]{4}/[0-9]{2}/[0-9]{2}/[0-9]{2}/[0-9]{2}/[0-9]{2}", url)
    if not illust_date:
        logging.getLogger(__name__).error(f"datetime not found in {url}")
        return []

    illust_host = "https://i.pximg.net"
    illust_date = illust_date.group()
    illust_ftype = url.split(".")[-1]
    urls = []
    for i in range(page_count):
        urls.append({
            "urls": {
                "thumb_mini": f"{illust_host}/c/128x128/img-master/img/{illust_date}/{illust_id}_p{i}_square1200.{illust_ftype}",
                "small": f"{illust_host}/c/540x540_70/img-master/img/{illust_date}/{illust_id}_p{i}_master1200.{illust_ftype}",
                "regular": f"{illust_host}/img-master/img/{illust_date}/{illust_id}_p{i}_master1200.{illust_ftype}",
                "original": f"{illust_host}/img-original/img/{illust_date}/{illust_id}_p{i}.{illust_ftype}",
            },
            "width": 0,
            "height": 0
        })

    return urls
