#!/usr/bin/env python
# coding=utf8

import multiprocessing
import os
import time

def haha(i):
    time.sleep(1)
    print("我获得的 i: ", i )
    return i

def mycallback(aa):
    print("我获得的 aa: ", aa)

pool = multiprocessing.Pool(processes=3)
for i in range(10):
    pool.apply_async(func=haha,args=(i,),callback=mycallback)
    # pool.apply(func=haha,args=(i,))

pool.close()
pool.join()

print("我执行完了...")