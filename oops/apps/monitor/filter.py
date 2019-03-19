from django_filters import  rest_framework as filters
from .models import ZabbixItemModel,ZabbixHostItemModel,MonitorAlertModel
import time

class ZabbixItemFilter(filters.FilterSet):
    item_name = filters.CharFilter(field_name="item_name", lookup_expr='icontains', label="监控项名称")
    item_key = filters.CharFilter(field_name="item_key", lookup_expr='icontains', label="监控项 Key")

    class Meta:
        model = ZabbixItemModel
        fields = ["item_name", "item_key"]

class ZabbixHostItemFilter(filters.FilterSet):
    server = filters.CharFilter(field_name="server__manager_ip", lookup_expr='icontains', label="服务器")
    item_key = filters.CharFilter(field_name="item_key", lookup_expr='icontains', label="监控项 Key")

    class Meta:
        model = ZabbixHostItemModel
        fields = ["server", "item_key"]

class MonitorAlertFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr='icontains', label="告警标题")
    source = filters.CharFilter(field_name="source", lookup_expr='exact', label="告警来源")
    # trigger_name = filters.CharFilter(field_name="trigger_name", lookup_expr='icontains', label="告警触发器的名称")
    level = filters.CharFilter(field_name="level", lookup_expr='exact', label="告警级别")
    status = filters.CharFilter(field_name="status", lookup_expr='exact', label="告警状态")
    # start_time_begin = filters.CharFilter(field_name="start_time", lookup_expr='ge', label="告警时间起始")
    # start_time_end = filters.CharFilter(field_name="start_time", lookup_expr='le', label="告警时间终止")
    start_time_begin = filters.CharFilter(field_name="start_time", label="告警时间起始", method='begin_unixtime_to_datetime')
    start_time_end = filters.CharFilter(field_name="start_time", label="告警时间终止", method='end_unixtime_to_datetime')
    server = filters.CharFilter(field_name="server__manager_ip", lookup_expr='icontains', label="服务器")

    class Meta:
        model = MonitorAlertModel
        fields = ["title","source","level","status","server", "start_time_begin","start_time_end"]

    def begin_unixtime_to_datetime(self,queryset, name, value):
        value = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(value)/1000))
        return queryset.filter(start_time__gt=value)

    def end_unixtime_to_datetime(self,queryset, name, value):
        value = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(value)/1000))
        return queryset.filter(start_time__lt=value)
