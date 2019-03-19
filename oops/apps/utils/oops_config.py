#!/usr/bin/env python
#coding=utf8

import os
import configparser,traceback

conf = configparser.ConfigParser()

def getMyConf(config_name='/root/.ws-ops.conf',section=''):

    ret = {"result":0,"msg":None}

    try:
        conf.read(config_name)
    except Exception as e:
        ret["result"] = 1
        ret["msg"] = e.args
        return ret

    try:
        oops_conf = conf.items(section)
    except configparser.NoSectionError:
        ret["result"] = 1
        ret["msg"] = "本地配置文件中不存在这个section: %s" %(section)
    except Exception as e:
        ret["result"] = 1
        ret["msg"] = e.args
    else:
        ret["oops_conf"] = dict(oops_conf)
    return ret

if __name__ == '__main__':
    haha = getMyConf(section="ldap_config")
    print(haha["result"])