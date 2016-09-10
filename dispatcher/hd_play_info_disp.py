#!/usr/bin/env python
# -*- coding:utf8 -*-

#__author__ == 'godlikeme'

from util.db_util import Hd_play_info_db_util


class Hd_play_info_disp(object):
    def __init__(self, key):

        assert(isinstance(key, dict))
        self.key = key
        self.hd_play_info_db_util = Hd_play_info_db_util()

    def dipatcher(self, q):
        for item in self.hd_play_info_db_util.find(self.key):
            q.put(item)
