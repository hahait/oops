#!/usr/bin/env python
#coding=utf-8

# 此脚本用于获取 linux 服务器信息，如: CPU,内存,磁盘,网卡,制造商,型号和系统信息
# 基于 python 2.x
# 系统需要安装软件包：yum -y install python-devel dmidecode; 如果是物理机 还需要 yum -y install ipmitool
# Python 需要安装的模块：pip install psutil
# 如果是 阿里云 ECS ,那么要安装 sdk: pip install aliyun-python-sdk-core; pip install aliyun-python-sdk-ecs

import psutil
import sys
import os
import subprocess
import socket
import platform
import time
import logging
import requests
import random
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

reload(sys)
sys.setdefaultencoding('utf8')

virtual_platform_list = ["KVM","VMware Virtual Platform"]
cloud_platform_list = ["Alibaba Cloud ECS"]

def myLog():
    ''' 打印日志 '''
    format = '%(asctime)s-[%(levelname)s]-%(message)s'
    log_format = logging.Formatter(format)
    log_handler = logging.FileHandler('/var/log/system_info_post.log', encoding='utf8')
    log_handler.setFormatter(log_format)
    mylog_logger = logging.getLogger('system_info')
    mylog_logger.handlers = []
    mylog_logger.addHandler(log_handler)
    mylog_logger.setLevel(logging.INFO)
    return mylog_logger

class GetSystemInfo(object):

    def execShellCmd(self,shell_cmd):
        shell_cmd_result = subprocess.Popen(shell_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = shell_cmd_result.communicate()
        assert result[0], result[1]
        return result[0]

    def aLiYunApiForEcs(self,private_ip):
        client = AcsClient('*******', '*********', 'cn-beijing')
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('ecs.aliyuncs.com')
        request.set_method('POST')
        request.set_version('2014-05-26')
        request.set_action_name('DescribeInstances')
        request.add_query_param('PrivateIpAddresses', '["%s"]' %(private_ip))
        response = client.do_action_with_exception(request)
        ecs_info = json.loads(response)["Instances"]["Instance"][0]
        ret = {
            "online_time": ecs_info["CreationTime"],
            "expired_time": ecs_info["ExpiredTime"],
            "charge_type": ecs_info["InstanceChargeType"],
            "instance_id": ecs_info["InstanceId"],
            "instance_name": ecs_info["InstanceName"],
            "instance_type": ecs_info["InstanceType"],
            "public_ip": ecs_info["PublicIpAddress"].get("IpAddress")[0] if ecs_info["PublicIpAddress"].get("IpAddress") else ecs_info["EipAddress"]["IpAddress"]
        }
        return ret

    def getCpuInfo(self):
        ''' 获取 CPU 数量 '''
        return '%s 核' %(psutil.cpu_count())

    def getMemInfo(self):
        ''' 获取内存大小'''
        return '%.2f GB' %(psutil.virtual_memory().total/1024.0/1024.0/1024.0)

    def getSwapInfo(self):
        ''' 获取 SWAP 空间 '''
        return '%.2f GB' %(psutil.swap_memory().total/1024.0/1024.0/1024.0)

    def getDisk(self):
        ''' 获取 物理磁盘信息 '''
        shell_cmd = ''' /sbin/fdisk -l | grep 'Disk' | grep -e '/dev/vd*' -e '/dev/sd*'|awk -F',' '{print $1}'| sed 's/Disk //g' '''
        return self.execShellCmd(shell_cmd).strip('\n').replace('\n','</br>')

    def getDiskMountInfo(self):
        ''' 获取磁盘挂载信息 '''
        disk_mount_list = ['[%s] - %s: %.2f GB' %(i.mountpoint,i.device,psutil.disk_usage(i.mountpoint).total/1024.0/1024.0/1024.0) for i in psutil.disk_partitions()]
        return '</br>'.join(disk_mount_list)

    def getNetworkCardInfo(self):
        ''' 获取网卡信息'''
        network = []
        for k, v in psutil.net_if_addrs().items():
            nc = {}
            ips = []
            ''' 过滤掉 lo 网口和 docker 的桥接网卡 '''
            if k in ['lo'] or k.startswith('veth'):continue
            nc["name"] = k

            ''' 设置网卡为 bond4:1 这样类型的 mac 地址 '''
            if ':' in k:
                for i in psutil.net_if_addrs()[k.split(':')[0]]:
                    if i.family == 17:
                        nc["mac"] = i.address

            nc['status'] = 'up' if psutil.net_if_stats()[k.split(':')[0]].isup else 'down'
            for n in v:
                if n.family == 17:
                    nc["mac"] = n.address
                elif n.family == 2:
                    ips.append({"ip": n.address, "netmask": n.netmask})
            nc["ips"] = ips
            network.append(nc)
        return network

    def getServerManufacturer(self):
        ''' 获取服务器的制造商 '''
        shell_cmd = '/usr/sbin/dmidecode --string system-manufacturer'
        return self.execShellCmd(shell_cmd).strip('\n')

    def getServerModel(self):
        ''' 获取服务器的型号 '''
        shell_cmd = '/usr/sbin/dmidecode --string system-product-name'
        return self.execShellCmd(shell_cmd).strip('\n')

    def getUuid(self):
        ''' 获取 服务器 UUID '''
        shell_cmd = '/usr/sbin/dmidecode --string system-uuid'
        return self.execShellCmd(shell_cmd).strip('\n')

    def getSnCode(self):
        ''' 获取 服务器 SN 码 '''
        shell_cmd = '/usr/sbin/dmidecode --string system-serial-number'
        return self.execShellCmd(shell_cmd).strip('\n')

    def getIdracIP(self):
        ''' 获取服务器的远程管理卡 IP(虚拟机不适合) '''
        shell_cmd = '/usr/bin/ipmitool lan print | grep "IP Address"| grep -Eo "192.168.[0-9]{1,3}.[0-9]{1,3}"'
        ret = self.execShellCmd(shell_cmd).strip('\n')
        return ret if ret else '0.0.0.0'

    def getManagerIp(self,network):
        for nw in network:
            if nw["ips"] and nw["status"] == 'up':
                manager_ip = nw["ips"][0]["ip"]
                break
        assert manager_ip, '未获取到管理IP,请检查....'
        return  manager_ip

    def getHostName(self):
        ''' 获取主机名 '''
        return socket.gethostname()

    def getOsVersion(self):
        ''' 获取系统版本 '''
        return ' '.join(platform.linux_distribution())

    def run(self):
        begin_time = int(round(time.time() * 1000))
        system_info = {}
        try:
            system_info["uuid"] = self.getUuid()
            system_info["hostname"] = self.getHostName()
            system_info["server_brand"] = self.getServerManufacturer()
            system_info["server_model"] = self.getServerModel()
            system_info["sn_code"] = self.getSnCode().upper() if system_info["server_model"] not in (virtual_platform_list + cloud_platform_list) else ''
            system_info["os_version"] = self.getOsVersion()
            system_info["cpu_count"] = self.getCpuInfo()
            system_info["mem"] = self.getMemInfo()
            system_info["swap"] = self.getSwapInfo()
            system_info["disk"] = self.getDisk()
            system_info["disk_mount"] = self.getDiskMountInfo()
            system_info["idrac_ip"] = self.getIdracIP() if system_info["server_model"] not in (virtual_platform_list + cloud_platform_list) else '0.0.0.0'
            system_info["network"] = self.getNetworkCardInfo()
            system_info['manager_ip'] = self.getManagerIp(system_info.get("network"))
            system_info["idc"] = 'cn-beijing-a'

            if system_info["server_model"] in cloud_platform_list:
                aliyun_ecs_info = self.aLiYunApiForEcs(system_info['manager_ip'])
                system_info["type"] = 'cloud'
                system_info.update(aliyun_ecs_info)
            elif system_info["server_model"] in virtual_platform_list:
                system_info["type"] = 'virtual'
            else:
                system_info["type"] = 'physical'
            end_time = int(round(time.time() * 1000))
        except Exception as e:
            myLog().error('获取服务器属性失败,错误信息: %s' %(e.args))
        else:
            myLog().info('获取服务器信息成功,信息为: %s; 共耗时: %s ms' % (system_info,end_time-begin_time))
            return system_info

    def sendSystemInfo(self):
        url = "http://oops.service.oops:20018/server/auto/"
        headers = {'content-type': 'application/json'}
        data = self.run()
        if not data:
            myLog().error('获取服务器某个属性失败,因此不能 post 到相应的 API 接口')
            return
        try:
            r = requests.post(url, headers=headers, data=json.dumps(data))
        except Exception as e:
            myLog().error("访问运维平台 API 接口失败.....")
            return
        if int(r.status_code) == 201:
            myLog().info('服务器信息 post 到 API 接口成功.....')
        else:
            myLog().error('服务器信息 post 到 API 接口失败,错误信息: %s' %(r.content))

if __name__ == '__main__':
    random_time = random.randint(1,120)
    time.sleep(random_time)
    myLog().info('获取服务器信息任务随机等待了 %s 秒后开始执行.....' %(random_time))
    sysinfo = GetSystemInfo()
    sysinfo.sendSystemInfo()