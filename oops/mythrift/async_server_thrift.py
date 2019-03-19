import json
import os
import sys
import django
pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, pathname)
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oops.settings")
django.setup()

import thriftpy
from thriftpy.rpc import make_server
import time

sleep_thrift = thriftpy.load("sleep.thrift", module_name="sleep_thrift")

class Dispatcher(object):
    def sleep(self, seconds):
        print("I'm going to sleep %d seconds" % seconds)
        time.sleep(seconds)
        print("Sleep over!")


def main():
    server = make_server(sleep_thrift.Sleep, Dispatcher(),'192.167.0.23', 9090)
    print("serving...")
    server.serve()


if __name__ == '__main__':
    main()