import  sys
import logging
import requests
import json


def myLog():
    format = '%(asctime)s-[%(levelname)s]-%(message)s'
    log_format = logging.Formatter(format)
    log_handler = logging.FileHandler('/tmp/zabbix_test.txt', encoding='utf8')
    log_handler.setFormatter(log_format)
    mylog_logger = logging.getLogger('zabbixAlert')
    mylog_logger.handlers = []
    mylog_logger.addHandler(log_handler)
    mylog_logger.setLevel(logging.INFO)
    return mylog_logger

class zabbixReportAlert(object):
    def __init__(self,url,title,message):
        self.url = url
        self.title = title
        self.message = message

    def reportAlert(self):
        ret = {"status": 0}
        alert_data = {"source": "zabbix"}
        alert_data["title"] = self.title
        myLog().info("获取zabbix原始的告警信息: %s" %(self.message))
        mymsg = self.message
        try:
            alert_data.update(eval(mymsg))
            ret["data"] = alert_data
            myLog().info('POST 到 API 接口的告警信息: %s' % (ret["data"]))
        except Exception as e:
            ret["status"] = 1
            myLog().error('转换zabbix信息失败, 错误信息: %s' % (e.args))
        return ret

    def sendZabbixData(self):
        url = self.url
        headers = {'content-type': 'application/json'}
        ret = self.reportAlert()

        if ret.get("status") == 1:
            myLog().error('获取zabbix告警信息失败,因此不能 post 到相应的 API 接口')
            return

        try:
            r = requests.post(url, headers=headers, data=json.dumps(ret.get("data")))
        except Exception as e:
            myLog().error("访问运维平台 API 接口失败.....")
            return
        if int(r.status_code) == 201:
            myLog().info('Zabbix告警信息 post 到 API 接口成功.....')
        else:
            myLog().error('Zabbix告警信息 post 到 API 接口失败,错误信息: %s' %(r.content))

if __name__ == "__main__":
    url = "http://192.168.0.23:20018/monitor/alert/"
    title = sys.argv[1]
    message = sys.argv[2]
    if not (title and message):
        myLog().error('未传入Zabbix告警信息, 请检查 zabbix 控制台配置项 action')

    zra_obj = zabbixReportAlert(url,title,message)
    zra_obj.sendZabbixData()
