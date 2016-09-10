#!/usr/bin/env python
# -*- coding:utf8 -*-


class DBConfig(object):
    HOST = "192.168.1.36"
    COUPON2B_STOCK_DB_URL = "mongodb://htw:htw@%s/coupon2b_stock" % HOST
    COUPON2B_DEFINE_DB_URL = "mongodb://htw:htw@%s/coupon2b_define" % HOST
    HD_PLAY_INFO_DB_URL = "mongodb://htw:htw@%s/hd_play_info" % HOST



