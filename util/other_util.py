#coding=utf-8

from email.header import Header
from email.mime.text import MIMEText
import smtplib
import json
import time
import sys
import re
import csv
import datetime
import hashlib
import os


def my_scp(host, src, dest):
    cmd = "scp %s:%s %s" % (host, src, dest)
    print "====== cmd: %s ==========" % cmd
    os.system(cmd)
    print "====== cmd execute complete ========="

def utf8str(obj):
    if isinstance(obj, unicode):
        return obj.encode('utf-8')
    if isinstance(obj, str):
        return obj
    if isinstance(obj, dict) or isinstance(obj, list):
        return utf8str(json.dumps(obj, ensure_ascii=False, sort_keys=True))
    return utf8str(str(obj))

def processMsgPrint(msg):
    print "[process %d]: %s" % (os.getpid(), msg)


def md5(obj, remove_space=False):
    if isinstance(obj, unicode):
        obj = obj.encode('utf-8')
    if isinstance(obj, str):
        return hashlib.md5(obj).hexdigest()

    if isinstance(obj, list):
        for index, el in enumerate(obj):
            if isinstance(el, unicode):
                obj[index] = el.encode('utf-8')
                # 去除空格
                if remove_space:
                    obj[index] = el.strip()

        content = ''.join(obj)
        return hashlib.md5(content).hexdigest()

    else:
        raise Exception('unknown type')

def print_list(fd, v):
    idx = 0
    for i in v:
        if isinstance(i, unicode):
            i = i.encode('utf-8')
            if idx > 0:
                fd.write(' ')
                fd.write(str(i))
                idx += 1
        fd.write("\n")


def get_date_with_day_duration(days=0):
    now = datetime.datetime.now()
    duration = datetime.timedelta(days=days)
    need_day = now + duration

    return need_day


def check_dir(target):
    if not os.path.exists(target):
        os.makedirs(target)

def check_and_clear(target):
    # 存储前， 清空样本
    if not os.path.exists(target):
        os.mkdir(target)
    else:
        os.system('rm -rf %s/*' % target)
        time.sleep(2)

def untar(src, dest=None):

    if not os.path.exists(dest):
        os.makedirs(dest)

    sep = os.path.splitext(src)[1]
    if 'gz' in sep:
        cmd = 'tar -xzf %s ' % src
        if dest:
            cmd += '-C %s' % dest
    elif 'tar' in sep:
        cmd = 'tar -xf %s ' % src
        if dest:
            cmd += '-C %s' % dest
    elif 'zip' in sep:
        if dest:
            cmd = 'unzip -o -d %s %s' % (dest, src)
        else:
            cmd = 'unzip -o %s' % src
    else:
        raise Exception('unknown tar file')

    os.system(cmd)


def send_email(email, title, message):
    username = 'notify@ipin.com'
    password = '4c4b5e4dfF'
    smtphost = 'smtp.exmail.qq.com'
    smtpport = 465

    if isinstance(message, unicode):
        message = message.encode('utf-8')
    if isinstance(title, unicode):
        title = message.encode('utf-8')

    msg = MIMEText(message, 'plain', 'utf-8')
    msg['Subject'] = Header(title, 'utf-8')
    msg['From'] = username

    if isinstance(email, list):
        msg['To'] = '; '.join(email)
        tolist = email
    else:
        msg['To'] = email
        tolist = [email]

    for i in range(0, len(tolist)):
        m = re.search('<([a-z0-9_@\-.]*)>\s*$', tolist[i], re.I)
        if m:
            tolist[i] = m.group(1)

    print "sending mail to", tolist
    print msg.as_string()
    s = smtplib.SMTP_SSL(smtphost, smtpport)
    s.login(username, password)
    s.sendmail(username, tolist, msg.as_string())
    s.quit()


def remove_empty_key(dt, except_keys=()):
    if not isinstance(dt, dict):
        raise Exception("need dict type")

    for key,value in dt.items():
        if key in except_keys:
            continue
        if not value:
            del dt[key]
    return dt

class Log(object):
    fd = sys.stdout

    @staticmethod
    def error(*v):
        ts = [time.strftime('%Y-%m-%d %H:%M:%S')]
        ts.extend(v)
        print_list(Log.fd, ts)


class ExcelFileSave(object):
    def __init__(self, fn):
        self._fn = fn
        self._csv_file = open(fn, 'wb')
        self._spamwrite = csv.writer(self._csv_file, dialect='excel',delimiter='#' )

    def append(self, raw):
        assert isinstance(raw, list)
        for index, e in enumerate(raw):
            raw[index] = utf8str(e)
        self._spamwrite.writerow(raw)


def statistic_line(file_name):
    total_line = 0
    with open(file_name, 'rb') as f:
        for line in f:
            line = line.strip()
            if line:
                total_line += 1

    return total_line


class TimeConver(object):

    @classmethod
    def SecondToStr(cls, seconds):

        retval = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(seconds))
        return retval

    @classmethod
    def getTimeStampSecond(cls, strtime, formatstring=None):
        """strtime: 2016-06-21 23:59:59
           formatstring: %Y-%m-%d %H:%M:%S
        """

        if not formatstring:
            formatstring = "%Y-%m-%d %H:%M:%S"

        t = time.strptime(strtime, formatstring)
        return time.mktime(t)

    @classmethod
    def getTimeBefore(cls, day):
        """timestamp seconds before day"""
        now = time.time()
        before = time.time() - 3600 * 24 * day
        return before

    @classmethod
    def getTodayStr(cls):
        "20160102"
        now = time.localtime()
        return "%04d%02d%02d" % (now.tm_year, now.tm_mon, now.tm_mday)


if __name__ == '__main__':
    # e = ExcelFileSave('test.txt')
    # e.append(['1,2,3', '2', '3', '4'])
    print TimeConver.getTimeStampSecond("2016-07-14 23:59:59")




