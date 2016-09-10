#!/usr/bin/env python
# -*- coding:utf8 -*-

#__author__ == 'godlikeme'


import time
def timefunc(isMethod=False):
    def _timefunc(func):
        def wrapper(*args, **kwargs):
            now = time.time() * 1000
            func(*args, **kwargs)
            if not isMethod:
                print "call %s, time consumes: %0.2fms" % (func.__name__, time.time() * 1000 - now)
            else:
                print "call %s.%s, time consumes: %0.2fms" % (type(args[0]), func.__name__, time.time() * 1000 - now)


        return wrapper
    return _timefunc

@timefunc(isMethod=False)
def func_Test(a, b):
    print "%s: %s" % (a, b)
    time.sleep(1)


class B(object):
    @timefunc(isMethod=True)
    def method_test(self, a, b):
        print "%s: %s" % (a, b)
        time.sleep(2)


if __name__ == "__main__":
    func_Test("1", "2")
    b = B()
    b.method_test(3, 4)

