# -*- coding: UTF-8 -*-

from datetime import datetime, timedelta, timezone

from . import media, secrets, xsession


def nowbeijing():
    return datetime.now(timezone(timedelta(hours=8)))
