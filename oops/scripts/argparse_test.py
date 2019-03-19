#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(description="修改 SLB 上后端节点的 权重值")
parser.add_argument("--vgid", action='store', dest="vgroup_id", required=True, help="虚拟主机组id")
parser.add_argument("--vgname", action='store', dest="vgroup_name", required=True, help="虚拟主机组名称")
parser.add_argument("--insid", action='store', dest="instance_id", required=True, help="服务器的实例id")
parser.add_argument("--bport", action='store', dest="backend_port", type=int, required=True, help="后端端口")
parser.add_argument("-w", "--weight", action='store', dest="weight", type=int, required=True, help="权重值")
parser.add_argument("-l", "--list", action='store_true', dest="list", required=True, help="列表")

aa = parser.parse_args()
print (aa)
print(aa.vgroup_id)
print(aa.vgroup_name)
