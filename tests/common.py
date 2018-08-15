# -*- coding: utf-8 -*-

import datetime
from dateutil import tz


def get_new_york_utc_offset():
    return datetime.datetime.now(tz.gettz("America/New_York")).strftime("%z")


def get_new_york_utc_offset_as_int():
    return int(int(get_new_york_utc_offset()) / 100)
