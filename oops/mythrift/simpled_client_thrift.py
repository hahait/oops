import thriftpy
from thriftpy.rpc import client_context

# cmdb_thrift = thriftpy.load("cmdb.thrift", module_name="cmdb_thrift")
# def main():
#     with client_context(cmdb_thrift.CmdbManagerService, '192.167.0.23', 9090) as c:
#         res = c.get_cmdb_info(23)
#         print(res)

def request_thrift(thrift_name,service, method, url, port, *args, **kwargs):
    ''' 通用的 simpled rpc client '''
    module_name = thrift_name.replace('.', '_')
    thrift_module = thriftpy.load(thrift_name, module_name=module_name)
    thrift_service = getattr(thrift_module, service)
    with client_context(thrift_service, url, port) as rt:
        res = getattr(rt, method)(*args, **kwargs)
        print(res)

if __name__ == '__main__':
    # main()
    request_thrift("cmdb.thrift", "CmdbManagerService", "get_cmdb_info", "192.167.0.23", 9090, 23)