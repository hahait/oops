import json
import os
import sys
import django
pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, pathname)
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oops.settings")
django.setup()

import thriftpy2
from thriftpy2.protocol import TBinaryProtocolFactory
from thriftpy2.server import TThreadedServer
from thriftpy2.thrift import TProcessor, TMultiplexedProcessor
from thriftpy2.transport import TBufferedTransportFactory, TServerSocket
from resources.views import CmdbThriftService,IdcThriftService


cmdb_thrift = thriftpy2.load("cmdb.thrift", module_name="cmdb_thrift")
idc_thrift = thriftpy2.load("idc.thrift", module_name="idc_thrift")

cmdb_proc = TProcessor(cmdb_thrift.CmdbManagerService, CmdbThriftService())
idc_proc = TProcessor(idc_thrift.IdcManagerService, IdcThriftService())

mux_proc = TMultiplexedProcessor()
mux_proc.register_processor("cmdb_thrift", cmdb_proc)
mux_proc.register_processor("idc_thrift", idc_proc)
app = mux_proc
