#!/usr/bin/env python
# -*- coding:utf8 -*-

#__author__ == 'godlikeme'

"""
       统计中秋灯谜活动人数,

       字段： hdId, shopId
   """

from base import BaseTask
from dispatcher.hd_play_info_disp import Hd_play_info_disp
from util.file_util import CsvFile
from util.other_util import TimeConver
from threading import RLock
from base_export import BaseExport
import sys
import json



class ExportMidAutumnGuessUser(BaseTask, BaseExport):
    def __init__(self, start_time, end_time, thread_cnt):
        BaseTask.__init__(self, "exportMidAutumnGuess", thread_cnt=thread_cnt)
        BaseExport.__init__(self)

        self.disp = Hd_play_info_disp({"timeStamp": {"$gte": start_time, "$lte": end_time},
                                       "hdId": "MidAutumnGuest"})

        self.save_file = CsvFile("data/%s_%s.csv" % (self._name, TimeConver.getTodayStr()))
        self.save_file.set_header(['shopId', 'hdId', "coupon2b_define_ids"])
        self.rs = {}
        self.coupon2b_define_ids = {}
        self.rs_lock = RLock()
        self.define_ids_lock = RLock()

    def append_to_rs(self, key, value):
        with self.rs_lock:
            self.rs[key] = value

    def append_to_coupon2b_define_ids(self, key, value):
        with self.define_ids_lock:
            self.coupon2b_define_ids[key] = value

    def dispatcher(self, q):
        self.disp.dipatcher(q)

    def run_job(self, job):
        if not job:
            return

        shopId = job["shopId"]
        hdId = job["hdId"]

        with self.define_ids_lock:
            if shopId not in self.coupon2b_define_ids:
                receiveCouponDefineIds = self.get_coupon_defineIds(shopId)
                if not receiveCouponDefineIds:
                    print "get_coupon_defineIds, result empty, shopId: %s" % shopId
                self.append_to_coupon2b_define_ids(shopId, receiveCouponDefineIds)

        self.append_to_rs(shopId, hdId)
        print "[+] export shoId: %s, hdId: %s" % (shopId, hdId)

    def get_coupon_defineIds(self, shopId):
        receiveCouponDefineIds = []
        receiveCouponIds = self.coupon_receive_info_db_util.getIdsByConsumerId(shopId)
        for receiveCouponId in receiveCouponIds:
            defineId, ok = self.is_guess_coupon(receiveCouponId)
            if ok:
                receiveCouponDefineIds.append(defineId)
            else:
                print "is_guess_coupon, result false, receivCouponId: %s, definID: %s" % (receiveCouponId, defineId)

        return receiveCouponDefineIds

    def is_guess_coupon(self, couponId):

        coupon_define_id = self.coupon_item_db_util.get_define_id_by_id(couponId)
        if not coupon_define_id:
            return coupon_define_id, False

        if self.coupon2b_define_db_util.check_ReceiveRuleType_with_id(coupon_define_id, "MidAutumnGuessRule"):
            return coupon_define_id, True

        return coupon_define_id, False

    def end_operation(self, *args, **kwargs):
        for key, value in self.rs.items():
            self.save_file.append_row([key, value, self.coupon2b_define_ids[key]])


def printUsage():
    print """

          export_mid_autumn_guess_user.py start_time end_time [thread_cnt]

            ex: export_mid_autumn_guess_user.py "2016-09-07 00:00:00" "2016-09-08 23:59:59"
    """


if __name__ == "__main__":
    if len(sys.argv) < 3:
        printUsage()
        exit(1)

    startTime = TimeConver.getTimeStampSecond(sys.argv[1]) * 1000
    endTime = TimeConver.getTimeStampSecond(sys.argv[2]) * 1000

    thread_cnt = 2
    if len(sys.argv) >= 4:
        thread_cnt = int(sys.argv[3])

    t = ExportMidAutumnGuessUser(startTime, endTime, thread_cnt)
    t.run()










