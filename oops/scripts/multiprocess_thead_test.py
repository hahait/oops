#!/usr/bin/env python

import time
from multiprocessing.dummy import Pool as ThreadPool

def haha(i):
    time.sleep(1)
    print("我要走了....")
    return "我执行了 %s ...." %(i)

def mycallback(str):
    print(str)

pool = ThreadPool(processes=3)

aa = pool.map(haha,range(10))

pool.close()
pool.join()

print("我执行完了...")
print(aa)