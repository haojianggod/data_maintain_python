#!/usr/bin/env python
# -*- coding:utf8 -*-

import csv
import codecs
import threading


class CsvFile(object):
    def __init__(self, fn):
        self.fn = fn
        self.csv_file = codecs.open(fn, 'wb', 'utf-8')
        self.writer = csv.writer(self.csv_file)
        self._lock = threading.RLock()

        self.is_set_header = False

    #def __del__(self):
    #    with self._lock:
    #        self.csv_file.close()

    def set_header(self, header):
        if not isinstance(header, list):
            raise Exception('need list')

        with self._lock:
            self.writer.writerow(header)
            self.is_set_header = True

    def append_row(self, row):

        with self._lock:
            self.writer.writerow(row)

    def append_rows(self, rows):
        with self._lock:
            self.writer.writerow(rows)