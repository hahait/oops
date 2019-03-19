#!/usr/bin/env python
import requests
from utils.oops_log import logError,logInfo
from itertools import chain
import json

class CeleryFlowerApi(object):
    def __init__(self,url="http://192.168.134.19:5555/api",headers={"content-type": "application/json"}):
        self.url = url
        self.headers = headers

    def execRequest(self,uri,method="GET",data=None):
        ret = {"result": 0}
        request_url = self.url + uri
        try:
            if method == "GET":
                r = requests.get(request_url, headers=self.headers)
            else:
                r = requests.post(request_url, headers=self.headers, data=json.dumps(data))
        except Exception as e:
            msg = "请求 flower api 接口失败,请确认 celery flower 是否运行....."
            ret["result"] = 1
            ret["msg"] = msg
            logError().error(msg)
            return ret
        if int(r.status_code) != 200:
            msg = "请求 flower api 接口的返回值是非 200,错误信息: %s" %(r.content)
            ret["result"] = 1
            ret["msg"] = msg
            logError().error(msg)
            return ret
        ret["data"] = r.json()
        return ret

    def getTaskInfo(self,uuid):
        uri = "/task/info/%s" %(uuid)
        return  self.execRequest(uri)

    def getWorkerInfo(self):
        uri = "/workers"
        return self.execRequest(uri)

    def getAllWorkerRegisterTasks(self):
        uri = "/workers"
        ret = self.execRequest(uri)
        if ret["result"] == 0:
            ret["data"] = list(set(list(chain.from_iterable([i["registered"] for i in ret["data"].values()]))))
        return ret

    def execTaskNow(self,task,data):
        uri = "/task/send-task/%s" %(task)
        return self.execRequest(uri,method="POST",data=data)
