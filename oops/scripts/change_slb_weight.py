#!/ops-data/zp/haha/dev-mysite/bin/python
# coding: utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import os
import configparser,traceback
import argparse
import json

class changeSLBWeightInfo(object):
    def __init__(self, vgroup_id, vgroup_name, server_id, server_port, weight):
        self.vgroup_id = vgroup_id
        self.vgroup_name = vgroup_name
        self.server_id = server_id
        self.server_port = server_port
        self.weight = weight
        aliyun_conf = self.get_myconf(section="aliyun_config")
        accessKeyId = aliyun_conf["mysec_conf"]["haha"]
        accessSecret = aliyun_conf["mysec_conf"]["hehe"]
        self.client = AcsClient(accessKeyId, accessSecret, 'cn-beijing')

    def get_myconf(self, config_name='/root/.ws-ops.conf', section=''):

        wsconf = configparser.ConfigParser()
        ret = {"result": 0, "msg": None}

        try:
            wsconf.read(config_name)
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = e.args
            return ret

        try:
            mysec_conf = wsconf.items(section)
        except configparser.NoSectionError:
            ret["result"] = 1
            ret["msg"] = "本地配置文件中不存在这个section: %s" % (section)
        except Exception as e:
            ret["result"] = 1
            ret["msg"] = e.args
        else:
            ret["mysec_conf"] = dict(mysec_conf)
        return ret

    def commonSLBWeightOperation(self, action,**kwargs):
        ''' 通用 slb 操作入口 '''
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('slb.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https')
        request.set_version('2014-05-15')

        request.set_action_name(action)
        request.add_query_param('RegionId', 'cn-beijing')
        if kwargs:
            for k, v in kwargs.items():
                request.add_query_param(k, v)

        response = self.client.do_action(request)

        return  str(response, encoding = 'utf-8')

    def checkVGroupBackend(self):
        ''' 检查 虚拟组内是否存在这个后端服务器, 如果不存在就添加 '''
        response = self.commonSLBWeightOperation('DescribeVServerGroupAttribute',VServerGroupId = self.vgroup_id)
        response_dict = json.loads(response)
        if not list(filter(lambda x: x["ServerId"] == self.server_id, response_dict["BackendServers"]["BackendServer"])):
            self.addBackendToVGroup()

    def addBackendToVGroup(self):
        ''' 添加后端服务器到虚拟组内 '''
        weight_attr_dict = {"VServerGroupId": self.vgroup_id,
                            "BackendServers": '[{ "ServerId": "%s", "Port": %s, "Weight": %s}]' % (self.server_id, self.server_port, self.weight)}

        response = self.commonSLBWeightOperation("AddVServerGroupBackendServers", **weight_attr_dict)

    def changeSLBWeight(self):
        ''' 修改虚拟组内指定后端服务器的权重 '''
        weight_attr_dict = {"VServerGroupId": self.vgroup_id,
                            "VServerGroupName": self.vgroup_name,
                            "BackendServers": '[{ "ServerId": "%s", "Port": %s, "Weight": %s, "Type": "ecs" }]' %(self.server_id, self.server_port, self.weight)}
        try:
            self.checkVGroupBackend()
        except Exception as e:
            print("校验SLB虚拟组中是否存在该后端服务器出错,错误信息: ", e.args)
        else:
            response = self.commonSLBWeightOperation('SetVServerGroupAttribute', **weight_attr_dict)
            response_dict = json.loads(response)
            response_dest = response_dict["BackendServers"]["BackendServer"] = list(filter(lambda x:x["ServerId"]==self.server_id, response_dict["BackendServers"]["BackendServer"]))
            print(json.dumps(response_dict, indent=4))

def parse_args():
    parser = argparse.ArgumentParser(description="解析命令行参数")
    parser.add_argument("--vgid", action='store', dest="vgroup_id", required=True, help="虚拟主机组id")
    parser.add_argument("--vgname", action='store', dest="vgroup_name", required=True, help="虚拟主机组名称")
    parser.add_argument("--insid", action='store', dest="instance_id", required=True, help="服务器的实例id")
    parser.add_argument("--bport", action='store', dest="backend_port", type=int, required=True, help="后端端口")
    parser.add_argument("--weight", action='store', dest="weight", type=int, required=True, help="权重值")

    return parser.parse_args()

if __name__ == '__main__':
    parser = parse_args()
    csw_obj = changeSLBWeightInfo(parser.vgroup_id, parser.vgroup_name, parser.instance_id, parser.backend_port, parser.weight)
    csw_obj.changeSLBWeight()