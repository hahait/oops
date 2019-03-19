from celery.signals import task_postrun,task_success,task_failure
from django.db.models.signals import post_save
from utils.oops_log import logError,logInfo
from django.dispatch import receiver
from taskschedule.models import CeleryTaskResultExtensionModel
from django_celery_results.models import TaskResult
import requests
import time
from .tasks import updateCeleryTaskResult

@receiver(post_save, sender=TaskResult)
def task_result_post_save_handler(sender,instance,**kwargs):
    t_id = instance.task_id
    if instance.task_name != 'taskschedule.tasks.updateCeleryTaskResult':
        updateCeleryTaskResult.delay(t_id,instance.status)