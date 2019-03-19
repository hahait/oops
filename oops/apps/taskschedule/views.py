from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import CeleryTaskResultSerializer,CrontabScheduleSerializer,IntervalScheduleSerializer,PeriodicTaskSerializer
from .models import CeleryTaskResultExtensionModel
from .filter import CeleryTaskResultFilter,CrontabTaskFilter
from django_celery_beat.models import CrontabSchedule,IntervalSchedule,PeriodicTask
from rest_framework.response import Response
from rest_framework import status
from utils.oops_log import logError,logInfo
from thirdapi.celeryflower import CeleryFlowerApi
from itertools import chain

class TaskResultViewSet(viewsets.ReadOnlyModelViewSet):
    '''
        list            : 获取任务执行结果列表
        read            : 获取指定任务执行结果对象
    '''
    queryset = CeleryTaskResultExtensionModel.objects.all().order_by("-id")
    serializer_class = CeleryTaskResultSerializer
    filterset_class = CeleryTaskResultFilter
    permission_classes = (AllowAny,)

class  CrontabScheduleViewSet(viewsets.ModelViewSet):
    '''
        list            : 获取 Crontab 周期列表
        read            : 获取指定的 Crontab 周期对象
        create          : 创建 Crontab 周期对象
        update          : 修改指定 Crontab 周期对象
        delete          : 删除指定 Cronntab 周期对象
        partial_update  : 部分修改指定 Crontab 周期对象
    '''
    queryset = CrontabSchedule.objects.all().order_by("-id")
    serializer_class = CrontabScheduleSerializer
    permission_classes = (AllowAny,)


class  IntervalScheduleViewSet(viewsets.ModelViewSet):
    '''
        list            : 获取 Crontab 周期列表
        read            : 获取指定的 Crontab 周期对象
        create          : 创建 Crontab 周期对象
        update          : 修改指定 Crontab 周期对象
        delete          : 删除指定 Cronntab 周期对象
        partial_update  : 部分修改指定 Crontab 周期对象
    '''
    queryset = IntervalSchedule.objects.all().order_by("-id")
    serializer_class = IntervalScheduleSerializer
    permission_classes = (AllowAny,)

class  PeriodicTaskViewSet(viewsets.ModelViewSet):
    '''
        list            : 获取 定时任务 列表
        read            : 获取指定的 定时任务 对象
        create          : 创建 定时任务 对象
        update          : 修改指定 定时任务 对象
        delete          : 删除指定 定时任务 对象
        partial_update  : 部分修改指定 定时任务 对象
    '''
    queryset = PeriodicTask.objects.all().order_by("-id")
    serializer_class = PeriodicTaskSerializer
    filterset_class = CrontabTaskFilter
    permission_classes = (AllowAny,)

class TaskRegisteredViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def list(self,request):
        ret = CeleryFlowerApi().getAllWorkerRegisterTasks()
        if ret["result"] == 1:
            logError().error(ret["msg"])
            return Response(data=ret["msg"],status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        registered_tasks_list = ret["data"]
        return Response(data=registered_tasks_list, status=status.HTTP_200_OK)

class TaskExecImmediateViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def create(self,request):
        print("request.data: ", request.data)
        if not request.data.get("task"):
            return Response(data="前端未传入参数 task",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        task = request.data.get("task")
        data = {}
        data["args"] = eval(request.data.get("args"))
        data["kwargs"] = eval(request.data.get("kwargs"))
        ret = CeleryFlowerApi().execTaskNow(task,data)
        if ret["result"] == 1:
            logError().error(ret["msg"])
            return Response(data=ret["msg"],status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        registered_tasks_list = ret["data"]
        return Response(data=registered_tasks_list, status=status.HTTP_200_OK)