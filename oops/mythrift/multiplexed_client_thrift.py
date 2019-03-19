import thriftpy
from thriftpy.rpc import client_context
from thriftpy.protocol import (
    TBinaryProtocolFactory,
    TMultiplexedProtocolFactory
    )

# cmdb_thrift = thriftpy.load("cmdb.thrift", module_name="cmdb_thrift")
# idc_thrift = thriftpy.load("idc.thrift", module_name="idc_thrift")
#
# def main():
#     binary_factory = TBinaryProtocolFactory()
#     cmdb_factory = TMultiplexedProtocolFactory(binary_factory, "cmdb_thrift")
#     with client_context(cmdb_thrift.CmdbManagerService, '192.167.0.23', 9090,
#                         proto_factory=cmdb_factory) as cmdb:
#         res_cmdb = cmdb.get_cmdb_info(23)
#         print(res_cmdb)
#
#     idc_factory = TMultiplexedProtocolFactory(binary_factory, "idc_thrift")
#     with client_context(idc_thrift.IdcManagerService, '192.167.0.23', 9090,
#                         proto_factory=idc_factory) as idc:
#         # play table tennis like a champ
#         res_idc = idc.get_idc_info(30)
#         print(res_idc)

def request_thrift(thrift_name,service, method, url, port, *args, **kwargs):
    ''' 通用的 multiplexed '''
    module_name = thrift_name.replace('.', '_')
    thrift_module = thriftpy.load(thrift_name, module_name=module_name)
    thrift_service = getattr(thrift_module, service)
    binary_factory = TBinaryProtocolFactory()
    thrift_factory = TMultiplexedProtocolFactory(binary_factory, module_name)
    with client_context(thrift_service, url, port, proto_factory=thrift_factory) as rt:
        res = getattr(rt, method)(*args, **kwargs)
        print(res)

if __name__ == '__main__':
    #main()
    request_thrift("cmdb.thrift", "CmdbManagerService", "get_cmdb_info", "192.167.0.23", 9090, 23)