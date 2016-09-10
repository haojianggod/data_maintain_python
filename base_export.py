#!/usr/bin/env python
# -*- coding:utf8 -*-

#__author__ == 'godlikeme'

from util.db_util import Coupon_receive_info_db_util, Coupon2b_define_db_util, Coupon_item_db_util

class BaseExport(object):
    def __init__(self):
        self.coupon_receive_info_db_util = Coupon_receive_info_db_util()
        self.coupon2b_define_db_util = Coupon2b_define_db_util()
        self.coupon_item_db_util = Coupon_item_db_util()

