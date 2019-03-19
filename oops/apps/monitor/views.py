from .models import History,HistoryUint,ZabbixHostItemModel,Items,ZabbixItemModel,Trends,TrendsUint,MonitorAlertModel
from resources.models import ServerModel
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
import time
from datetime import timedelta,datetime
from rest_framework.permissions import IsAuthenticated,AllowAny
from appsmanager.models import AppConfigModel
from django.db.models import F, Avg,Max,Count
from .serializers import ZabbixItemSerializer,ZabbixHostItemSerializer,MonitorAlertSerializer
from .filter import ZabbixItemFilter,ZabbixHostItemFilter,MonitorAlertFilter
from utils.oops_log import logError,logInfo

class ZabbixValueForServerViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def list(self,request):
        servers_data = {}
        app_id = request.query_params.get('app')
        item = request.query_params.get('item')
        time_one_hours_ago = self.unixtime_to_minutes_or_hours(int(time.mktime((datetime.now() - timedelta(hours=1)).timetuple())),60)
        time_begin = self.unixtime_to_minutes_or_hours(int(request.query_params.get('time_begin'))/1000,60) if request.query_params.get('time_begin') else time_one_hours_ago
        time_end = self.unixtime_to_minutes_or_hours(int(request.query_params.get('time_end'))/1000,60) if request.query_params.get('time_end') else self.unixtime_to_minutes_or_hours(time.time(),60)

        try:
            app_obj = AppConfigModel.objects.get(id__exact=app_id)
        except AppConfigModel.DoesNotExist:
            return Response(data='请选择应用或者选择的该应用已下线....',status=status.HTTP_400_BAD_REQUEST)

        try:
            zabbix_host_item_obj = ZabbixItemModel.objects.get(item__exact=item)
        except ZabbixItemModel.DoesNotExist:
            return Response(data='后端未定义该 item: %s 逻辑' % (item), status=status.HTTP_400_BAD_REQUEST)

        ret = self.getZabbixItemValue(app_obj.server.all(),time_begin,time_end,item,zabbix_host_item_obj.item_key)
        if ret["status"] == 1:
            return Response(data=ret["msg"],status=status.HTTP_400_BAD_REQUEST)
        servers_data = ret["data"]
        # print('servers_data: ', servers_data)
        return Response(data=servers_data,status=status.HTTP_200_OK)

    def unixtime_to_minutes_or_hours(self,unixtime,time_num):
        '''
            unixtime 是10位的秒数;
            根据time_num返回整分钟数或者整小时数,也就是转换为格式 %Y-%m-%d %H:%M:%S 后秒数或者分钟数为0;
            time_num 为 60 返回整分钟数
            time_num 为 3600 返回 整小时数
        '''
        return int(unixtime) - int(unixtime)%time_num

    def getZabbixItemValue(self,server_list,time_begin,time_end,item,item_key):
        ''' 获取每个 item 的值(包括 X 轴和Y 轴) '''
        zabbix_item_data = {}
        zabbix_host_server_list = list(ServerModel.objects.filter(zabbixhostitemmodel__isnull=False).distinct())
        server_list = list(set(server_list).intersection(set(zabbix_host_server_list)))
        ret = self.getZabbixItemxAxisDelay(server_list,item_key,time_begin,time_end)
        if ret["status"] == 1:
            return ret
        zabbix_item_delay = ret.pop("max_item_delay")
        zabbix_item_data["x_data"] = ret.pop("x_data")
        y_data = []
        for server_obj in server_list:
            item_data = {}
            item_data["name"] = server_obj.manager_ip
            ret = self.getZabbixValue(server_obj, item_key, time_begin, time_end, zabbix_item_delay)
            if ret["status"] == 1:
                return ret
            if item in ["cpu_idle", "memory_free"]:
                item_data["data"] = [round(100 - k["value"], 3) for k in ret['data']]
            else:
                item_data["data"] = [round(k["value"], 3) for k in ret['data']]
            y_data.append(item_data)
        zabbix_item_data["y_data"] = y_data
        ret["data"] = zabbix_item_data
        return  ret

    def getZabbixItemxAxisDelay(self,server_list,item_key,time_begin,time_end):
        '''
            根据查询的时间跨度以及监控项采集周期确定X 轴的取值范围,时间跨度和X轴数据点间隔分配关系如下:
            0-0.5 天 : 每1分钟一个点
            0.5-1 天 : 每5分钟一个点
            1-3 天   : 每10分钟一个点
            3-7 天   : 每15分钟一个点
            7-X 天   : 每60分钟一个点,直接查询 trends 表
        '''
        ret = {"status": 0}
        time_span = time_end - time_begin
        try:
            max_item_delay = int(ZabbixHostItemModel.objects.filter(server__in=server_list,item_key__exact=item_key).aggregate(item_delay_max=Max('item_delay'))["item_delay_max"])
        except Exception as e:
            ret["status"] = 1
            msg = "ZabbixHostItemModel 获取 item_key: %s 的 delay 失败" %(item_key)
            ret["msg"] = msg
            logError().error(msg)
            return ret

        if time_span <= 0.5 * 24 * 60 * 60:
            time_strftime = '%Y-%m-%d %H:%M'
            ret["max_item_delay"] = 1 * 60 if max_item_delay <= 1 * 60 else max_item_delay
        elif time_span > 0.5 * 24 * 60 * 60 and time_span <= 1 * 24 * 60 * 60:
            time_strftime = '%Y-%m-%d %H:%M'
            ret["max_item_delay"] = 5*60 if max_item_delay <= 5*60 else max_item_delay
        elif time_span > 1 * 24 * 60 * 60 and time_span <= 3 * 24 * 60 * 60:
            time_strftime = '%Y-%m-%d %H:%M'
            ret["max_item_delay"] = 10*60 if max_item_delay <= 10*60 else max_item_delay
        elif time_span > 3 * 24 * 60 * 60 and time_span <= 7 * 24 * 60 * 60:
            time_strftime = '%Y-%m-%d %H:%M'
            ret["max_item_delay"] = 15 * 60 if max_item_delay <= 15 * 60 else max_item_delay
        else:
            ret["max_item_delay"] = 60 * 60 if max_item_delay <= 60 * 60 else max_item_delay
            time_strftime = '%Y-%m-%d %H:00'
            time_begin = self.unixtime_to_minutes_or_hours(time_begin, 3600)
            time_end = self.unixtime_to_minutes_or_hours(time_end, 3600)

        ret["x_data"] = [time.strftime(time_strftime, time.localtime(i)) for i in range(time_begin, time_end, ret["max_item_delay"])]

        return ret

    def getZabbixValue(self,server_obj,item_key,time_begin,time_end,item_delay):
        ''' 获取每个 item 指定周期内 每个时间点的平均值,也就是主要获取 Y 轴的值 '''
        ret = {"status": 0}
        time_span = time_end - time_begin
        try:
            zabbix_obj = server_obj.zabbixhostitemmodel_set.get(item_key__exact=item_key)
        except ZabbixHostItemModel.DoesNotExist:
            ret["status"] = 1
            ret["msg"] = '模型 ZabbixHostItemModel 中查不到 item_key : %s 的对象' % (item_key)
            return ret
        zabbix_itemid = zabbix_obj.itemid
        if time_span <= 7 * 24 * 60 * 60:
            zabbix_get_value_model = zabbix_obj.history_model_name
            try:
                zabbix_data = eval(zabbix_get_value_model).objects.filter(itemid__exact=zabbix_itemid,clock__gte=time_begin,clock__lte=time_end).using("zabbix").\
                    values("clock","value").annotate(myclock=(F("clock")-F("clock")%item_delay)).values("myclock").annotate(value=Avg("value")).order_by("myclock")
            except Exception as e:
                ret["status"] = 1
                ret["msg"] = '模型 %s 中查不到 item_key : %s, time_begin: %s, time_end: %s 的数据列表' % (zabbix_get_value_model,item_key,time_begin,time_end)
            else:
                ret['data'] = zabbix_data
        else:
            zabbix_get_value_model = zabbix_obj.trends_model_name
            try:
                print(eval(zabbix_get_value_model).objects.filter(itemid__exact=zabbix_itemid, clock__gte=time_begin,
                                                                  clock__lte=time_end).using("zabbix").values("clock","value_avg").query)
                ''' 如果 查询时间跨度大于 7天,并且监控项采集周期大于1小时,这里会有问题,因为没有求平均值 '''
                zabbix_data = eval(zabbix_get_value_model).objects.filter(itemid__exact=zabbix_itemid, clock__gte=time_begin,clock__lte=time_end).using("zabbix").annotate(value=F("value_avg")).values("clock","value")
            except Exception as e:
                ret["status"] = 1
                ret["msg"] = '模型 %s 中查不到 item_key : %s, time_begin: %s, time_end: %s 的数据列表,错误信息: %s' % (zabbix_get_value_model, item_key, time_begin, time_end, e.args)
            else:
                ret['data'] = zabbix_data
        return  ret

class MonitorItemRelateAppsViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def list(self,request):
        app_list = ZabbixItemModel.objects.annotate(aid=F("app_name"),name=F("app_name__name")).values("aid","name").distinct()
        return Response(data=app_list,status=status.HTTP_200_OK)

class ZabbixItemViewSet(viewsets.ModelViewSet):
    '''
        list            : 获取 zabbix item 列表
        create          : 创建 zabbix item 对象
        update          : 修改指定 zabbix item 对象
        delete          : 删除指定 zabbix item 对象
        read            : 获取指定 zabbix item 对象
        partial_update  : 部分修改指定 zabbix item 对象
    '''
    queryset = ZabbixItemModel.objects.all()
    serializer_class = ZabbixItemSerializer
    filterset_class = ZabbixItemFilter
    permission_classes = [ AllowAny, ]

class ZabbixHostItemViewSet(viewsets.ReadOnlyModelViewSet):
    '''
        list            : 获取 zabbix host item 列表
        read            : 获取指定 zabbix host item 对象
    '''
    queryset = ZabbixHostItemModel.objects.all()
    serializer_class = ZabbixHostItemSerializer
    filterset_class = ZabbixHostItemFilter
    permission_classes = [ AllowAny, ]

class MonitorAlertViewSet(viewsets.ModelViewSet):
    '''
            list            : 获取 alert 列表
            create          : 创建 alert 对象
            update          : 修改指定 alert 对象
            delete          : 删除指定 alert 对象
            read            : 获取指定 alert 对象
            partial_update  : 部分修改指定 alert 对象
        '''
    queryset = MonitorAlertModel.objects.all().order_by("-start_time")
    serializer_class = MonitorAlertSerializer
    filterset_class = MonitorAlertFilter
    permission_classes = [AllowAny, ]

class MonitorAlertStatisticsViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def list(self,request):
        time_7_days_ago = int(time.mktime((datetime.now() - timedelta(days=7)).timetuple()))
        time_begin_pre = int(request.query_params.get('start_time_begin'))/1000 if request.query_params.get('start_time_begin') else time_7_days_ago
        time_end_pre = int(request.query_params.get('start_time_end'))/1000 if request.query_params.get('start_time_end') else time.time()
        time_begin = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time_begin_pre))
        time_end = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_end_pre))
        alertQuerySet = MonitorAlertModel.objects.filter(start_time__gt=time_begin,start_time__lt=time_end)
        data = {}
        data["alert_status_atatistics"] = self.alertStatisticsByStatus(alertQuerySet)
        data["alert_level_atatistics"] = self.alertStatisticsByLevel(alertQuerySet)
        data["alert_source_atatistics"] = self.alertStatisticsBySource(alertQuerySet)
        data["alert_trigger_atatistics"] =self.alertStatisticsByTriggerName(alertQuerySet)
        return Response(data=data,status=status.HTTP_200_OK)

    def alertStatisticsByStatus(self,queryset):
        return list(queryset.annotate(name=F("status")).values("name").annotate(value=Count("id")).order_by("-value"))

    def alertStatisticsByLevel(self,queryset):
        return list(queryset.annotate(name=F("level")).values("name").annotate(value=Count("id")).order_by("-value"))

    def alertStatisticsBySource(self,queryset):
        return list(queryset.annotate(name=F("source")).values("name").annotate(value=Count("id")).order_by("-value"))

    def alertStatisticsByTriggerName(self,queryset):
        return list(queryset.exclude(trigger_name__isnull=True).annotate(name=F("trigger_name")).values("name").annotate(value=Count("id")).order_by("-value")[:10])