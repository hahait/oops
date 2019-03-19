from celery import shared_task
from celery.utils.log import get_task_logger
from thirdapi.rabbitmq import RabbitmqApi
from monitor.models import MonitorAlertModel
from datetime import datetime

logger = get_task_logger(__name__)

def monitor_route_task(name, args, kwargs, options, task=None, **kw):
    if name.startswith('monitor'):
        return {"queue": "monitor"}
    else:
        return None

@shared_task(bind=True,name="monitor.tasks.rabbitmqQueueLengthAndConsumerMonitor",ignore_result=False)
def rabbitmqQueueLengthAndConsumerMonitor(self):
    ret = RabbitmqApi("guest","Abcd1234").getQueueLengthAndConsumer()
    if ret.get("result") == 1:
        return  ret
    data = ret.get("data")
    monitor_obj_bulk_create_list = []
    for q_info in data:
        time_now = datetime.now().strftime("%Y-%m-%d %X")
        m_info = {}
        m_info["source"] = "others"
        m_info["level"] = "High"
        m_info["status"] = "PROBLEM"
        m_info["start_time"] = time_now
        consumer_title = "MQ 队列监控: %s 消费者全部离线" %(q_info.get("queue"))
        length_title = "MQ 队列监控: %s 消息消费堆积" % (q_info.get("queue"))
        if q_info["consumer_num"] == 0:
            m_info["title"] = consumer_title
            m_info["detail"] = "MQ 队列: %s 的消费者数量为 0" %(q_info.get("queue"))
            m_info["trigger_name"] = "MQ 队列监控消费者全部离线"
            monitor_obj_bulk_create_list.append(MonitorAlertModel(**m_info))
            continue

        if q_info["messages_ready"] >= 10 or q_info["messages_total"] >= 10 or q_info["messages_unacknowledged"] >= 10:
            m_info["title"] = length_title
            m_info["detail"] = "MQ 队列: %s 的消息消费堆积, 详情: %s" % (q_info.get("queue"), q_info)
            m_info["trigger_name"] = "MQ 队列监控消息消费堆积"
            monitor_obj_bulk_create_list.append(MonitorAlertModel(**m_info))
        else:
            MonitorAlertModel.objects.filter(title__in=[consumer_title,length_title],status__exact="PROBLEM").update(status="OK", end_time=time_now)
            continue
    if not monitor_obj_bulk_create_list:
        return "MQ 队列正常"
    try:
        MonitorAlertModel.objects.bulk_create(monitor_obj_bulk_create_list)
    except Exception as e:
        logger.error("MonitorAlertModel 批量创建对象: %s 失败,错误信息: %s" %(monitor_obj_bulk_create_list,e.args))
    else:
        logger.info("MonitorAlertModel 批量创建对象: %s 成功" %(monitor_obj_bulk_create_list))