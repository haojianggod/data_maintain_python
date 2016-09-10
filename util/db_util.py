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
    
    
class Coupon_receive_info_db_util(Base_db_util):
    def __init__(self):
        super(Coupon_receive_info_db_util, self).__init__(DBConfig.COUPON2B_STOCK_DB_URL, "coupon2b_stock", "coupon_receive_info")

    def getIdsByConsumerId(self, consumeId):
        docs = self.collection.find({"consumeId": consumeId})
        rs = [doc["_id"] for doc in docs]
        return rs


class Coupon_item_db_util(Base_db_util):
    def __init__(self):
        super(Coupon_item_db_util, self).__init__(DBConfig.COUPON2B_STOCK_DB_URL, "coupon2b_stock", "coupon_item")

    def get_define_id_by_id(self, _id):
        doc = self.collection.find_one({"_id", _id})
        if not doc:
            return
        return doc.get("couponDefineId","")


class Coupon2b_define_db_util(Base_db_util):
    def __init__(self):
        super(Coupon2b_define_db_util, self).__init__(DBConfig.COUPON2B_DEFINE_DB_URL, "coupon2b_define", "coupon_2b_define")

    def check_ReceiveRuleType_with_id(self, id, ruleType):
        doc = self.collection.find_one({"_id": id})
        receiveRuleList = doc.get("receiveRuleList", [])
        for receiveRule in receiveRuleList:
            if receiveRule["ruleType"] == ruleType:
                return True

        return False


