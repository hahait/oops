from rest_framework import serializers
from .models import ZabbixItemModel,Items,ZabbixHostItemModel,Interface,MonitorAlertModel,Events,Triggers,Functions
from appsmanager.models import AppConfigModel
from utils.oops_log import logError,logInfo
from resources.models import ServerModel
from rest_framework.response import Response
from rest_framework import status
import time
from datetime import datetime

class ZabbixItemSerializer(serializers.ModelSerializer):
    '''
        Zabbix 监控项序列化
    '''
    class Meta:
        model = ZabbixItemModel
        fields = '__all__'
        read_only_fields = ["id", "create_time", "last_update_time"]
        extra_kwargs = {'create_time': {'format': '%Y-%m-%d %H:%M:%S'},
                        'last_update_time': {'format': '%Y-%m-%d %H:%M:%S'}}

    def to_representation(self, instance):
        zabbix_item_obj = instance
        ret = super(ZabbixItemSerializer, self).to_representation(instance)
        ret["app_name"] = [{"id": app_obj.id, "name": app_obj.name} for app_obj in instance.app_name.all()]
        ret["server_count"] = ServerModel.objects.filter(appconfigmodel__in=instance.app_name.all()).distinct().count()
        return ret

    def validate_item_key(self,item_key):
        if Items.objects.filter(key_field__exact=item_key).using("zabbix").count() == 0:
            raise serializers.ValidationError("zabbix 中不存在这个 key, 请检查 zabbix 相关模板或者自定义 key 的配置....")
        return item_key

    def update(self, instance, validated_data):
        if len(validated_data) == 1 and  'app_name' in validated_data:
            previous_apps = instance.app_name.all()
            current_apps = validated_data.get('app_name')
            new_add_apps = list(set(current_apps).difference(set(previous_apps)))
            new_delete_apps = list(set(previous_apps).difference(set(current_apps)))
            for add_app_obj in  new_add_apps:
                ret = self.add_servers_relate_monitor_items(add_app_obj,instance.item_key)
                if ret["status"] == 1:
                    return Response(data=ret["msg"],status=status.HTTP_400_BAD_REQUEST,exception=True)
            for delete_app_obj in new_delete_apps:
                ret = self.delete_servers_relate_monitor_items(delete_app_obj)
                if ret["status"] == 1:
                    return Response(data=ret["msg"], status=status.HTTP_400_BAD_REQUEST)

        return super(ZabbixItemSerializer,self).update(instance, validated_data)

    def delete_servers_relate_monitor_items(self,app_obj):
        '''
            由于应用混布,所以同一个服务器会关联多个应用，因此删除 服务器关联的监控项时要考虑这个服务器是否被其他应用使用
            删除仅属于本应用的服务器与监控项的关联，而不影响 同属于其他应用下的某个服务器与监控项的关联
        '''
        ret = {"status": 0}
        monitor_item_relate_apps = AppConfigModel.objects.filter(zabbixitemmodel__isnull=False).exclude(name__exact=app_obj.name)
        delete_server_obj_list = [server for server in app_obj.server.all() for app in server.appconfigmodel_set.exclude(name__exact=app_obj.name) if app not in monitor_item_relate_apps]
        try:
            ZabbixHostItemModel.objects.filter(server__in=delete_server_obj_list).delete()
        except Exception as e:
            ret["status"] = 1
            ret["msg"] = "ZabbixHostItemModel 删除 app: %s 关联 server 的监控项失败,请查看日志...." %(app_obj.name)
            logError().error("ZabbixHostItemModel 删除 app: %s 关联的 server： %s 失败, 错误信息: %s" %(app_obj.name,delete_server_obj_list,e.args))
        return ret

    def add_servers_relate_monitor_items(self,app_obj,item_key):
        '''
            添加服务器与监控项的关联：
            1. 先检查这个服务器是否已经被关联了；
            2. 要去 zabbix 上获取 该服务器的相关配置信息，如：itemid,hostid,delay,units,value_type 以及存储在哪个表
        '''
        ret = {"status":0}
        add_server_obj_list = [server for server in app_obj.server.all() if server not in ServerModel.objects.filter(zabbixhostitemmodel__isnull=False,zabbixhostitemmodel__item_key__exact=item_key).distinct()]
        for server_obj in add_server_obj_list:
            try:
                host_obj = Interface.objects.db_manager("zabbix").get(ip__exact=server_obj.manager_ip,port__exact=10050)
            except Interface.DoesNotExist:
                ret["status"] = 1
                msg = "Zabbix 上 Interface 表中查不到 IP: %s 端口: 10050 的对象,请检查 zabbix 是否接入了该主机以及zabbix_agent 的端口是不是 10050...." %(server_obj.manager_ip)
                ret["msg"] = msg
                logError().error(msg)
                continue

            try:
                item_obj = Items.objects.db_manager("zabbix").get(hostid__exact=host_obj.hostid,key_field__exact=item_key)
            except Items.DoesNotExist:
                ret["status"] = 1
                msg = "Zabbix 上 Items 表中查不到 hostid: %s key_: %s 的对象,请检查 zabbix 该主机是否添加了该监控项...." %(host_obj.hostid,item_key)
                ret["msg"] = msg
                logError().error(msg)
                return ret

            ret = self.server_relate_monitor_item(item_obj,server_obj)
            if ret["status"] == 1:
                break

        return ret

    def server_relate_monitor_item(self,item_obj,server_obj):
        ret = {"status": 0}

        zabbix_host_item_data = {}
        zabbix_host_item_data["itemid"] = item_obj.itemid
        zabbix_host_item_data["hostid"] = item_obj.hostid.hostid
        zabbix_host_item_data["item_key"] = item_obj.key_field
        zabbix_host_item_data["item_name"] = item_obj.name
        zabbix_host_item_data["value_type"] = item_obj.value_type
        zabbix_host_item_data["item_units"] = item_obj.units
        zabbix_host_item_data["server"] = server_obj

        if item_obj.value_type == 0:
            zabbix_host_item_data["history_model_name"] = 'History'
            zabbix_host_item_data["trends_model_name"] = 'Trends'
        elif item_obj.value_type == 1:
            zabbix_host_item_data["history_model_name"] = 'HistoryStr'
        elif item_obj.value_type == 2:
            zabbix_host_item_data["history_model_name"] = 'HistoryLog'
        elif item_obj.value_type == 3:
            zabbix_host_item_data["history_model_name"] = 'HistoryUint'
            zabbix_host_item_data["trends_model_name"] = 'TrendsUint'
        else:
            zabbix_host_item_data["history_model_name"] = 'HistoryText'

        if item_obj.delay.lower().endswith('h'):
            zabbix_host_item_data["item_delay"] = eval(item_obj.delay[:-1]) * 3600
        elif item_obj.delay.lower().endswith('m'):
            zabbix_host_item_data["item_delay"] = eval(item_obj.delay[:-1]) * 60
        elif item_obj.delay.lower().endswith('s'):
            zabbix_host_item_data["item_delay"] = eval(item_obj.delay[:-1])
        else:
            zabbix_host_item_data["item_delay"] = eval(item_obj.delay)

        print("zabbix_host_item_data: ", zabbix_host_item_data)

        try:
            zabbix_host_item_obj = ZabbixHostItemModel.objects.create(**zabbix_host_item_data)
        except Exception as e:
            ret["status"] = 1
            msg = "ZabbixHostItemModel 创建 服务器: %s 关联 item: %s 的对象失败, 错误信息: %s" %(server_obj.manager_ip, item_obj.key_field, e.args)
            ret["msg"] = msg
            logError().error(msg)
        return ret

class ZabbixHostItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = ZabbixHostItemModel
        fields = '__all__'
        read_only_fields = ["id", "create_time", "last_update_time"]
        extra_kwargs = {'create_time': {'format': '%Y-%m-%d %H:%M:%S'}}

    def to_representation(self, instance):
        server_obj = instance.server
        ret = super(ZabbixHostItemSerializer,self).to_representation(instance)
        ret["server"] = {"id": server_obj.id, "manager_ip": server_obj.manager_ip}
        return ret

class MonitorAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitorAlertModel
        fields = "__all__"
        read_only_fields = ["id", "create_time", "last_update_time"]
        extra_kwargs = {'create_time': {'format': '%Y-%m-%d %H:%M:%S'},
                        'last_update_time': {'format': '%Y-%m-%d %H:%M:%S'},
                        'start_time': {'format': '%Y-%m-%d %H:%M:%S'},
                        'end_time': {'format': '%Y-%m-%d %H:%M:%S'}
                        }

    def to_internal_value(self, data):
        if data.get("source") != 'zabbix':
            return data
        try:
            event_obj = Events.objects.db_manager("zabbix").get(eventid__exact=data.get("eventid"))
            data["detail"] = ' last value: %s' %(data.pop("last_value"))
            if data.get("status") == 'PROBLEM':
                server_ip = data.pop("hostip")
                server_ip = server_ip if server_ip != '127.0.0.1' else '192.168.1.79'
                server_obj = ServerModel.objects.get(manager_ip__exact=server_ip)
                trigger_obj = Triggers.objects.db_manager("zabbix").get(triggerid__exact=event_obj.objectid)
                data["server"] = server_obj
                data["trigger_name"] = trigger_obj.description
                data["start_time"] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(event_obj.clock))
            else:
                data["status"] = "OK"
                data["end_time"] = datetime.strptime(data.get("end_time"),"%Y.%m.%d %H:%M:%S")
        except Exception as e:
            msg = "初始化 zabbix post 过来的数据异常,错误信息: %s" %(e.args)
            logError().error(msg)
            raise serializers.ValidationError(msg)

        return data

    def create(self,validated_data):
        if validated_data.get("source") != "zabbix":
            return super(MonitorAlertSerializer,self).create(validated_data)
        eventid = validated_data.get("eventid")
        status = validated_data.get("status")
        try:
            alert_obj = MonitorAlertModel.objects.get(eventid__exact=eventid)
        except MonitorAlertModel.DoesNotExist:
            return super(MonitorAlertSerializer, self).create(validated_data)

        if alert_obj.status != status:
            alert_obj.status = status
            alert_obj.end_time = validated_data.get("end_time")
            alert_obj.save(update_fields=["status","end_time","last_update_time"])
        return alert_obj

    def to_representation(self, instance):
        ret = super(MonitorAlertSerializer, self).to_representation(instance)
        if ret.get("server"):
            ret["server"] = instance.server.manager_ip
        return ret