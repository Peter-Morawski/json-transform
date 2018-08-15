# -*- coding: utf-8 -*-

import time


def get_new_york_utc_offset():
    local_time = time.localtime()
    if local_time.tm_isdst == 1:
        return "-0400"

    return "-0500"


def get_new_york_utc_offset_as_int():
    local_time = time.localtime()
    if local_time.tm_isdst == 1:
        return -4

    return -5
