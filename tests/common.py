# -*- coding: utf-8 -*-

import datetime
from dateutil import tz


def get_new_york_utc_offset():
    return _get_tz_str("America/New_York")


def get_new_york_utc_offset_as_int():
    return _get_tz_int("America/New_York")


def _get_tz_str(tz_name):
    return datetime.datetime.now(tz.gettz(tz_name)).strftime("%z")


def _get_tz_int(tz_name):
    return int(int(_get_tz_str(tz_name)) / 100)


def get_berlin_utc_offset():
    return _get_tz_str("Europe/Berlin")


def get_berlin_utc_offset_as_int():
    return _get_tz_int("Europe/Berlin")


def get_london_utc_offset():
    return _get_tz_str("Europe/London")


def get_london_utc_offset_as_int():
    return _get_tz_int("Europe/London")


def get_istanbul_utc_offset():
    return _get_tz_str("Europe/Istanbul")


def get_istanbul_utc_offset_as_int():
    return _get_tz_int("Europe/Istanbul")


def get_tokyo_utc_offset():
    return _get_tz_str("Asia/Tokyo")


def get_tokyo_utc_offset_as_int():
    return _get_tz_int("Asia/Tokyo")
