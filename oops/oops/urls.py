from django.conf.urls import url,include
import rest_framework
from rest_framework import routers,urls
from accounts.views import UserViewSet,GroupViewSet,ContentTypeViewSet,GroupRelateViewSet,PermissionViewSet,UserInfoViewSet
from resources.views import IdcViewSet,CabinetViewSet,ServerManufacturerViewSet,ServerModelViewSet,\
                                ServerViewSet,ServerAutoViewSet,NetworkCardViewSet,IpAddrViewSet,ServerForRelateViewSet
from monitor.views import ZabbixValueForServerViewSet,ZabbixItemViewSet,ZabbixHostItemViewSet,MonitorAlertViewSet,\
                            MonitorAlertStatisticsViewSet,MonitorItemRelateAppsViewSet
from rest_framework.documentation import  include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token
from dashboard.views import DashboardCountStatisticsViewSet,DashboardSevenDaysStatisticsViewSet
from appsmanager.views import AppConfigWithRelateViewSet,AppConfigSimpleViewSet
from taskschedule.views import TaskResultViewSet,CrontabScheduleViewSet,IntervalScheduleViewSet,\
                                PeriodicTaskViewSet,TaskRegisteredViewSet,TaskExecImmediateViewSet

router = routers.DefaultRouter()
router.register(r'user/info',UserInfoViewSet,base_name="user_info")
router.register(r'user',UserViewSet,base_name="user")
router.register(r'group/relate',GroupRelateViewSet,base_name="group_relate")
router.register(r'group',GroupViewSet,base_name="group")
router.register(r'permission',PermissionViewSet,base_name="permission")
router.register(r'content/type',ContentTypeViewSet,base_name="content_type")
router.register(r'idc',IdcViewSet,base_name="idc")
router.register(r'cabinet',CabinetViewSet,base_name="cabinet")
router.register(r'server/relate',ServerForRelateViewSet,base_name="server_for_relate")
router.register(r'server/manufacturer',ServerManufacturerViewSet,base_name="server_manufacturer")
router.register(r'server/model',ServerModelViewSet,base_name="server_model")
router.register(r'server/auto',ServerAutoViewSet,base_name="server_auto")
router.register(r'server',ServerViewSet,base_name="server")
router.register(r'network',NetworkCardViewSet,base_name="network")
router.register(r'ip',IpAddrViewSet,base_name="ip")
router.register(r'monitor/alert/statistics',MonitorAlertStatisticsViewSet,base_name='monitor_alert_statistics')
router.register(r'monitor/alert',MonitorAlertViewSet,base_name='monitor_alert')
router.register(r'monitor/server',ZabbixHostItemViewSet,base_name='monitor_server')
router.register(r'monitor/relate/apps',MonitorItemRelateAppsViewSet,base_name='monitor_item_relate_apps')
router.register(r'monitor/config',ZabbixItemViewSet,base_name='monitor_config')
router.register(r'monitor',ZabbixValueForServerViewSet,base_name="monitor")
router.register(r'dashboard/count/statistics',DashboardCountStatisticsViewSet,base_name="dashboard_count")
router.register(r'dashboard/sevendays/statistics',DashboardSevenDaysStatisticsViewSet,base_name="dashboard_seven_days")
router.register(r'appmanager/config/relate',AppConfigWithRelateViewSet,base_name="appmanager_config_with_relate")
router.register(r'appmanager/config',AppConfigSimpleViewSet,base_name="appmanager_config")
router.register(r'task/result',TaskResultViewSet,base_name="task_result")
router.register(r'task/crontab/periodic',CrontabScheduleViewSet,base_name="task_crontab_periodic")
router.register(r'task/interval/periodic',IntervalScheduleViewSet,base_name="task_interval_periodic")
router.register(r'task/crontab/manage',PeriodicTaskViewSet,base_name="task_crontab_manage")
router.register(r'task/registered/list',TaskRegisteredViewSet,base_name="task_registered_list")
router.register(r'task/exec/immediate',TaskExecImmediateViewSet,base_name="task_exec_immediate")

urlpatterns = [
    url(r'^',include(router.urls)),
    # url(r'^auth-api',include(rest_framework.urls,namespace="rest_framework")),
    url(r'^api-token-auth',obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^docs/',include_docs_urls("运维管理平台API接口文档")),
]