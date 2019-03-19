import thriftpy
from thriftpy.rpc import client_context

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
    print("我现在要执行 1 ....")
    request_thrift("sleep.thrift", "Sleep", "sleep", "192.167.0.23", 9090, 1)
    print("我现在要执行 2 ....")
    request_thrift("sleep.thrift", "Sleep", "sleep", "192.167.0.23", 9090, 2)
    print("我现在要执行 3 ....")
    request_thrift("sleep.thrift", "Sleep", "sleep", "192.167.0.23", 9090, 3)