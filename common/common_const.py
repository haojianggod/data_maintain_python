#!/usr/bin/env python
# -*- coding:utf8 -*-


class DBConfig(object):
    HOST = "h16,h9,h11"
    COUPON2B_STOCK_DB_URL = "mongodb://htw:htw@%s/coupon2b_stock" % HOST
    HD_PLAY_INFO_DB_URL = "mongodb://htw:htw@%s/hd_play_info" % HOST

