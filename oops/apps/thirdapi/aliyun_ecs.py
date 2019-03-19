#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore import client
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526 import DescribeInstanceAutoRenewAttributeRequest
from utils.oops_config import getMyConf
from utils.oops_log import logError,logInfo
import json
import os

class aLiYunEcs(object):
    def __init__(self):
        aliyun_conf = getMyConf(section="aliyun_config")
        if aliyun_conf["result"] == 0:
            accessKeyId = aliyun_conf["oops_conf"]["haha"]
            accessSecret = aliyun_conf["oops_conf"]["hehe"]
        else:
            logError().error(aliyun_conf["msg"])
            accessKeyId = ''
            accessSecret = ''
        self.clt = client.AcsClient(accessKeyId, accessSecret, 'cn-beijing')

    def aliyunDescribeInstances(self, **kwargs):
        '''
            获取 ECS 所有实例的详细信息
            者指定实例的详细信息： 通过传参 InstanceIds = ["实例id"]
        '''
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        request.set_accept_format('json')
        request.add_query_param('PageSize', 100)

        if kwargs:
            for k,v in kwargs.items():
                request.add_query_param(str(k), str(v))
        try:
            response = self.clt.do_action_with_exception(request)
        except Exception as e:
            logError().error("获取阿里云上 ECS 实例信息异常,错误信息: %s" %(e))
            return
        ret = {i["NetworkInterfaces"]["NetworkInterface"][0]["PrimaryIpAddress"]:{
            "idc": i["ZoneId"],
            "cpu_count": "%s 核" %(i["Cpu"]),
            "online_time": i["CreationTime"],
            "expired_time" : i["ExpiredTime"],
            "charge_type": i["InstanceChargeType"],
            "instance_id": i["InstanceId"],
            "instance_name": i["InstanceName"],
            "instance_type": i["InstanceType"],
            "mem": "%.2f GB" %(i["Memory"]/1024.0),
            "os_version": i["OSName"],
            "uuid": "%s" %(i["SerialNumber"].upper()),
            "server_brand": "Alibaba Cloud",
            "server_model": "Alibaba Cloud ECS",
            "type": "cloud",
            "idrac_ip": "0.0.0.0",
            "status": i["Status"],
            "hostname": i["HostName"],
            "public_ip": i["PublicIpAddress"].get("IpAddress")[0] if i["PublicIpAddress"].get("IpAddress") else i["EipAddress"]["IpAddress"],
            "manager_ip": i["NetworkInterfaces"]["NetworkInterface"][0]["PrimaryIpAddress"],
            "network": [{"status": "up",
                       "ips": [{"ip": i["NetworkInterfaces"]["NetworkInterface"][0]["PrimaryIpAddress"],"netmask": "255.255.240.0"}],
                       "mac": i["NetworkInterfaces"]["NetworkInterface"][0]["MacAddress"],
                       "name": "eth0"
                       }]
          } for i in json.loads(response)["Instances"]["Instance"]}
        return ret

if __name__ == "__main__":
    result = aLiYunEcs().aliyunDescribeInstances()
    ecs_list = [i["NetworkInterfaces"]["NetworkInterface"][0]["PrimaryIpAddress"] for i in result]