import json
import requests
from utils.oops_log import logError,logInfo

class RabbitmqApi(object):
    def __init__(self,user,passwd,
                 vhost = "/celery",
                 url = "http://192.168.134.19:15672/api",
                 headers = {"content-type": "application/json"}):
        self.user = user
        self.password = passwd
        self.vhost = vhost.replace("/","%2f") if vhost.find("/") != -1 else vhost
        self.url = url
        self.headers = headers
    def execRequest(self,uri,method="GET",data=None):
        ret = {"result": 0}
        request_url = self.url + uri
        try:
            if method == "GET":
                r = requests.get(request_url, headers=self.headers, auth=(self.user, self.password))
            else:
                r = requests.post(request_url, headers=self.headers, data=json.dumps(data), auth=(self.user, self.password))
        except Exception as e:
            msg = "请求 RabbitMQ API 接口失败,请确认 RabbitMQ 是否运行....."
            ret["result"] = 1
            ret["msg"] = msg
            logError().error(msg)
            return ret
        if int(r.status_code) != 200:
            msg = "请求 RabbitMQ API 接口的返回值是非 200,错误信息: %s" %(r.content)
            ret["result"] = 1
            ret["msg"] = msg
            logError().error(msg)
            return ret
        ret["data"] = r.json()
        return ret

    def getQueueLengthAndConsumer(self,queue_name=''):
        uri = '/queues/%s/%s' %(self.vhost,queue_name)
        ret = self.execRequest(uri)
        if ret["result"] == 1:
            return  ret
        queue_data = ret["data"]
        if queue_name:
            ret["data"] = {"queue": queue_data["name"],
                            "messages_total": queue_data["messages"],
                            "messages_ready": queue_data["messages_ready"],
                            "consumer_num": queue_data["consumers"],
                            "messages_unacknowledged": queue_data["messages_unacknowledged"]}

        ret["data"] = [{"queue": queue["name"],
                        "messages_total": queue["messages"],
                        "messages_ready": queue["messages_ready"],
                         "consumer_num": queue["consumers"],
                        "messages_unacknowledged": queue["messages_unacknowledged"]}
                        for queue in queue_data if not (queue["name"].startswith('celeryev') or queue["name"].endswith("celery.pidbox"))]
        return ret