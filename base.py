#coding=utf-8

from util import other_util as util
import Queue
import threading
import datetime
import time
# import runtime
import socket
import re
import os
import traceback
import sys


class BaseTask(object):

    class PathConfig(object):
        result_file = os.path.join(os.getcwd(), '../data/etl_result.txt')
        etl_failids_file = os.path.join(os.getcwd(), '../data/etl_failids.txt')
        toc_failids_file = os.path.join(os.getcwd(), '../data/2c_failids.txt')

    def __init__(self, task_name, queue_size=200, thread_cnt=10):
        self._queue = Queue.Queue(queue_size)
        self._thread_cnt = thread_cnt
        self._end_mark = 0
        self._name = task_name
        self._start_timet = time.time()
        self._start_datetime = None
        self._running_count = 0
        self._worker_count = 0
        self._threads = []
        self._reporter = None
        self._dispatcher = None
        self.cur_jobid = 0
        self._mjob_count = 0
        self._mjob_all = '?'
        self._log_port = 9527

        self._tls = threading.local()
        self._r_locker = threading.RLock()

    def dispatcher(self, q):
        raise NotImplementedError("virtual function called")

    def _job_runner(self, tid):
        with self._r_locker:
            self._worker_count += 1
        setattr(self._tls, 'tid', tid)
        end_this_thd = False
        while not end_this_thd:
            job, ismainjob = self._get_job()
            if job is None:
                self._dec_worker()
                return

            self.cur_jobid = job

            try:
                with self._r_locker:
                    self._running_count += 1
                self.run_job(job)
            except Exception as e:
                util.Log.error(e)
                traceback.print_exc()
            finally:
                with self._r_locker:
                    self._running_count -= 1

        self._dec_worker()

    def run_job(self, job):
        return False

    def _get_job(self):
        try:
            jobid = self._queue.get(True, 20)
            self._queue.task_done()
            if jobid is not None:
                with self._r_locker:
                    self._mjob_count += 1
            return jobid, 0
        except Queue.Empty:
            return None, None

    def _dec_worker(self):
        with self._r_locker:
            self._worker_count -= 1
            if self._worker_count == 0:
                self._end_mark = 1

    def _load_data(self):
        return

    def start_operation(self, *args, **kwargs):
        return

    def run(self):

        self.start_operation()

        self._load_data()

        if (len(self._threads) > 0 or
                    self._reporter is not None or
                    self._dispatcher is not None):
            raise RuntimeError("already run??")

        self._start_datetime = datetime.datetime.now()
        self._threads = []
        self.cur_jobid = 0
        self._end_mark = 0
        self._worker_count = 0

        self._job_count = 0
        self._mjob_count = 0
        self._mjob_all = '?'

        # 日志报告 udp查看
        self._reporter = threading.Thread(target=self.report)
        self._reporter.start()
        # runtime.Runtime.set_thread_name(self._reporter.ident, "%s.job.reporter" % self._name)

        # 任务分发
        self._dispatcher = threading.Thread(target=self.dispatcher, args=(self._queue, ))
        self._dispatcher.start()
        # runtime.Runtime.set_thread_name(self._dispatcher.ident, "%s.job.dispatcher" % self._name)

        for i in range(0, self._thread_cnt):
            t = threading.Thread(target=self._job_runner, args=(i,))
            t.start()
            # runtime.Runtime.set_thread_name(t.ident, "%s.worker.%d" % (self._name, i))
            self._threads.append(t)

        self.event_handler('STARTED', '')
        self.wait_run(True)

        self.end_operation()

    def wait_run(self, report=False):
        for t in self._threads:
            t.join()
        self._end_mark = 1
        self._dispatcher.join()
        self._reporter.join()
        self._dispatcher = None
        self._reporter = None
        self._end_mark = 0
        self._threads = []
        if report:
            endtime = datetime.datetime.now()
            timespan = str(endtime - self._start_datetime)
            reportstr = "prog:%s\nlast job is %s\nDONE time used:%s\n" % (' '.join(sys.argv), str(self.cur_jobid), timespan)
            reportstr += "mj: %d " % (self._mjob_count)
            sys.stderr.write(reportstr)
            self.event_handler('DONE', reportstr)

    def event_handler(self, evt, msg, **kwargs):
        return

    def end_operation(self, *args, **kwargs):
        return

    def report(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while 1:
            time.sleep(2)
            prog = "mj:%d/%s\n wc:%d \n rc:%d" % (self._mjob_count, self._mjob_all, self._worker_count, self._running_count)
            if isinstance(self.cur_jobid, dict) and 'url' in self.cur_jobid:
                cjstr = util.utf8str(self.cur_jobid['url'])
            else:
                cjstr = util.utf8str(self.cur_jobid)
            cjstr = re.sub(r'\r|\n', '', cjstr)
            if len(cjstr) > 100:
                cjstr = cjstr[0:100]

            message = "[pid=%d]job:%s prog:%s\n" % (os.getpid(), cjstr, prog)
            try:
                s.sendto(message, ("127.0.0.1", self._log_port))
            except Exception as e:
                pass
            if self._end_mark:
                message = "[pid=%d] DONE\n" % (os.getpid())
                try:
                    s.sendto(message, ("127.0.0.1", self._log_port))
                except:
                    pass
                return

    def wait_q(self):
        lt = 0
        while True:
            while not self._queue.empty():
               self._queue.join()
            if time.time() < lt + 1 and self._running_count==0:
                return True
            time.sleep(2)
            lt = time.time()









