#!/usr/bin/env python
import json
import os
import sys
import django
import argparse

pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, pathname)
sys.path.insert(0, os.path.abspath(os.path.join(pathname, '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oops.settings")
django.setup()

from appsmanager.models import AppConfigModel

def get_all_hosts():
    myhosts = {app.name: list(app.server.values_list("manager_ip", flat=True)) for app in AppConfigModel.objects.filter(env__exact="online")}
    return json.dumps(myhosts, indent=4)

def get_host_info(host):
    return json.dumps({}, indent=4)

def parse_args():
    parser = argparse.ArgumentParser(description="解析命令行参数")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list", action="store_true",help="显示所有的主机列表")
    group.add_argument ("--host", help="显示主机的详细信息")

    return parser.parse_args()

def main():
    parser = parse_args()
    if parser.list:
        print(get_all_hosts())
    else:
        print(get_host_info(parser.host))


if __name__ == "__main__":
   main()

