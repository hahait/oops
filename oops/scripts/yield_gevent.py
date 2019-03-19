#!/usr/bin/env python

def haha():
    r = 0
    while True:
        print("我执行了 haha ...")
        n = yield r
        print("我收到的 n 值: ", n)
        r = n

ha = haha()
ha.__next__()

for i in range(10):
    n = ha.send(i)
    print("返回的 n 是: ",n)

