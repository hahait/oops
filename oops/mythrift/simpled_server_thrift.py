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
from resources.views import CmdbThriftService

cmdb_thrift = thriftpy.load("cmdb.thrift", module_name="cmdb_thrift")

def main():
    server = make_server(cmdb_thrift.CmdbManagerService, CmdbThriftService(),'192.167.0.23', 9090)
    print("serving...")
    server.serve()


if __name__ == '__main__':
    main()