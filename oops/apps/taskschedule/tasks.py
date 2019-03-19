from celery import shared_task
from celery.utils.log import get_task_logger
import time
import requests
from .models import CeleryTaskResultExtensionModel
from thirdapi.celeryflower import CeleryFlowerApi

logger = get_task_logger(__name__)

def taskschedule_route_task(name, args, kwargs, options, task=None, **kw):
    if name.startswith('taskschedule'):
        return {"queue": "taskschedule"}
    else:
        return None

@shared_task(bind=True,name="taskschedule.tasks.updateCeleryTaskResult",ignore_result=False)
def updateCeleryTaskResult(self,uuid,status):

    i = 0
    while i <= 60:
        i = i + 1
        time.sleep(5)
        ret = CeleryFlowerApi().getTaskInfo(uuid)
        if ret["result"] == 1:
            return  ret
        task_result_data = ret["data"]
        task_result_data["received"] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(task_result_data["received"]))) if task_result_data.get("received") else ''
        task_result_data["succeeded"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(task_result_data["succeeded"]))) if task_result_data.get("succeeded") else ''
        task_result_data["started"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(task_result_data["started"]))) if task_result_data.get("started") else ''
        task_result_data["timestamp"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(task_result_data["timestamp"]))) if task_result_data.get("timestamp") else ''
        task_result_data["runtime"] = round(task_result_data["runtime"], 2) if task_result_data.get("runtime") else ''

        if task_result_data.get("state") == status:
            break
    try:
        CeleryTaskResultExtensionModel.objects.update_or_create(defaults=task_result_data, **{"uuid": uuid})
    except Exception as e:
        logger.error( "CeleryTaskResultExtension 保存task_id: %s 的 信息: %s 失败,错误信息: %s" % (uuid, task_result_data, e.args))
    else:
        logger.info("CeleryTaskResultExtension 保存task_id: %s 的 信息成功" % (uuid))