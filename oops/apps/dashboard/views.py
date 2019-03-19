from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from resources.models import ServerModel,ServerManufacturerModel,IdcModel
from monitor.models import MonitorAlertModel
from datetime import datetime,date,timedelta
from django.db.models.functions import TruncDate
from django.db.models import Count,F
from rest_framework import  status
from appsmanager.models import AppConfigModel
from django.contrib.auth.models import Group

datetime_7days_ago = datetime.now() - timedelta(days=7)
date_7days_ago = date.today() - timedelta(days=7)

class DashboardCountStatisticsViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def list(self,request):
        dashboard_statistics = {}
        dashboard_statistics["cmdb_statistics"] = self.getCmdbStatistics()
        dashboard_statistics["app_statistics"] = self.getAppStatistics()
        dashboard_statistics["alert_count_statistics"] = self.getStatistics(MonitorAlertModel,["title", "detail","source","status"])
        dashboard_statistics["publish_count_statistics"] = self.getStatistics(MonitorAlertModel,["title", "detail", "source", "status"])
        dashboard_statistics["workform_count_statistics"] = self.getStatistics(MonitorAlertModel,["title", "detail", "source", "status"])
        return Response(data=dashboard_statistics, status=status.HTTP_200_OK)

    def getStatistics(self,model_name,fields_name_list):
        cs_obj = DashboardModelStatistics(model_name)
        cs_total_count = cs_obj.total_count_statistics()
        cs_today_add_count = cs_obj.today_add_count()
        cs_today_add_detail = cs_obj.today_add_detail(fields_name_list)
        return {"total_count": cs_total_count,"today_add_count": cs_today_add_count,"today_add_detail": cs_today_add_detail}

    def getCmdbStatistics(self):
        cs_obj = DashboardModelStatistics(ServerModel)
        cs_total_count = cs_obj.total_count_statistics()
        cs_today_add_count = cs_obj.today_add_count()
        cs_by_manufacturer = cs_obj.cmdb_by_manufacturer()
        cs_by_status = cs_obj.cmdb_by_status()
        cs_by_idc = cs_obj.cmdb_by_idc()
        cs_by_env = cs_obj.cmdb_by_env()

        return {"total_count": cs_total_count,
                "today_add_count": cs_today_add_count,
                "cmdb_by_manufacturer": cs_by_manufacturer,
                "cmdb_by_status": cs_by_status,
                "cmdb_by_env": cs_by_env,
                "cmdb_by_idc": cs_by_idc,
                }

    def getAppStatistics(self):
        ac_obj = DashboardModelStatistics(AppConfigModel)
        ac_total_count = ac_obj.total_count_statistics()
        ac_today_add_count = ac_obj.today_add_count()
        ac_by_team = ac_obj.app_by_team()
        ac_by_status = ac_obj.app_by_status()
        ac_by_env = ac_obj.app_by_env()
        ac_by_type = ac_obj.app_by_type()

        return {"total_count": ac_total_count,
                "today_add_count": ac_today_add_count,
                "app_by_team": ac_by_team,
                "app_by_status": ac_by_status,
                "app_by_env": ac_by_env,
                "app_by_type": ac_by_type,
                }

class DashboardSevenDaysStatisticsViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def list(self,request):
        dashboard_seven_days_statistics = {}
        dashboard_seven_days_statistics["cmdb_seven_days_statistics"] = self.getStatisticsDetail(ServerModel)
        dashboard_seven_days_statistics["alert_seven_days_statistics"] = self.getStatisticsDetail(MonitorAlertModel)
        dashboard_seven_days_statistics["app_seven_days_statistics"] = self.getStatisticsDetail(MonitorAlertModel)
        dashboard_seven_days_statistics["publish_seven_days_statistics"] = self.getStatisticsDetail(MonitorAlertModel)
        dashboard_seven_days_statistics["workform_seven_days_statistics"] = self.getStatisticsDetail(MonitorAlertModel)

        return Response(data=dashboard_seven_days_statistics, status=status.HTTP_200_OK)

    def getStatisticsDetail(self,model_name):
        cs_obj = DashboardModelStatistics(model_name)
        cs_7days_statistics = cs_obj.seven_days_statistics()
        return cs_7days_statistics

class DashboardModelStatistics(object):
    def __init__(self,model_name):
        self.model_name = model_name

    def total_count_statistics(self):
        return self.model_name.objects.count()

    def today_add_count(self):
        return self.model_name.objects.filter(create_time__icontains=date.today()).count()

    def today_add_detail(self,fields_name_list):
        return list(self.model_name.objects.filter(create_time__icontains=date.today()).values(*fields_name_list))

    def seven_days_statistics(self):
        xy_data_init = {(date.today()-timedelta(days=i)): 0 for i in range(7,0,-1)}
        seven_days_statistics_dict = dict(self.model_name.objects.filter(create_time__gte=date_7days_ago,create_time__lt=date.today())
                                          .annotate(mydate=TruncDate("create_time")).values("mydate").annotate(value=Count("id")).values_list("mydate","value").order_by())
        xy_data_init.update(seven_days_statistics_dict)
        seven_days_statistics_list = [{"x_data": k, "y_data": v} for k, v in xy_data_init.items()]
        return {"x_data": [k["x_data"] for k in seven_days_statistics_list], "y_data": [k["y_data"] for k in seven_days_statistics_list]}

    def cmdb_by_manufacturer(self):
        return list(ServerManufacturerModel.objects.annotate(value=Count("servermodel")).values("name","value"))

    def cmdb_by_status(self):
        return list(ServerModel.objects.annotate(name=F("status")).values('name').annotate(value=Count("id")).values("name","value").order_by("value"))

    def cmdb_by_env(self):
        return list(ServerModel.objects.annotate(name=F("env")).values('name').annotate(value=Count("id")).values("name","value").order_by("value"))

    def cmdb_by_idc(self):
        data = IdcModel.objects.annotate(value=Count("servermodel")).exclude(value__exact=0).values("cn_name","value")
        return [{"name": k.get("cn_name"), "value": k.get("value")} for k in data]

    def app_by_team(self):
        return list(Group.objects.exclude(name__exact='ops').annotate(value=Count('appconfigmodel')).exclude(value__exact=0).values('name','value'))

    def app_by_status(self):
        ss = list(AppConfigModel.objects.values('status').annotate(value=Count("id")).values("status","value").order_by())
        return [{"name": dict(AppConfigModel.STATUS_CHOICES).get(s["status"]), "value": s["value"] } for s in ss]

    def app_by_env(self):
        env_list = list(AppConfigModel.objects.values('env').annotate(value=Count("id")).values("env","value").order_by("value"))
        return [{"name": dict(AppConfigModel.ENV_CHOICES).get(e["env"]), "value": e.get("value")} for e in env_list]

    def app_by_type(self):
        type_list = list(AppConfigModel.objects.values('type').annotate(value=Count("id")).values("type","value").order_by("value"))
        return [{"name": dict(AppConfigModel.TYPE_CHOICES).get(t["type"]), "value": t.get("value")} for t in type_list]