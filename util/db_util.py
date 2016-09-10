#!/usr/bin/env python
# -*- coding:utf8 -*-

import pymongo
from common.common_const import DBConfig


class Base_db_util(object):
    def __init__(self, mongourl, db_name, coll_name):
        self.db_name = db_name
        self.coll_name = coll_name
        self.client = pymongo.MongoClient(mongourl)
        self.collection = self.client[self.db_name][self.coll_name]


class Hd_play_info_db_util(Base_db_util):
    def __init__(self):
        super(Hd_play_info_db_util, self).__init__(DBConfig.HD_PLAY_INFO_DB_URL, "hd_play_info", "hd_play_info")

    def find(self, key):
        if key is None:
            return None
        return self.collection.find(key)
    
    
