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
import sys


class ExportMidAutumnGuessUser(BaseTask):
    def __init__(self, start_time, end_time, thread_cnt):
        BaseTask.__init__(self, "exportMidAutumnGuess", thread_cnt=thread_cnt)

        self.disp = Hd_play_info_disp({"timeStamp": {"$gte": start_time, "$lte": end_time},
                                       "hdId": "MidAutumnGuest"})

        self.save_file = CsvFile("data/%s_%s.csv" % (self._name, TimeConver.getTodayStr()))
        self.save_file.set_header(['shopId', 'hdId'])
        self.rs = {}
        self.rs_lock = RLock()

    def append_to_rs(self, key, value):
        with self.rs_lock:
            self.rs[key] = value

    def dispatcher(self, q):
        self.disp.dipatcher(q)

    def run_job(self, job):
        if not job:
            return

        shopId = job["shopId"]
        hdId = job["hdId"]

        self.append_to_rs(shopId, hdId)
        print "[+] export shoId: %s, hdId: %s" % (shopId, hdId)

    def end_operation(self, *args, **kwargs):
        for key, value in self.rs.items():
            self.save_file.append_row([key, value])


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










