from celery import shared_task
from celery.utils.log import get_task_logger
from utils.oops_log import logError,logInfo
import time
from resources.models import ServerModel,IdcModel
from appsmanager.models import AppConfigModel
from thirdapi.aliyun_ecs import aLiYunEcs
import requests
import json
from celery import group,chunks,chain
from utils.time_transform import utc_minute_time_to_local

logger = get_task_logger(__name__)

def resources_route_task(name, args, kwargs, options, task=None, **kw):
    if name.startswith('resources'):
        return {"queue": "resources"}
    else:
        return None

@shared_task(bind=True,name="resources.tasks.updateCmdbInstanceInfo",ignore_result=False)
def updateCmdbInstanceInfo(self,manager_ip,status,online_time,expired_time,charge_type,instance_id,instance_name,instance_type,public_ip):
    try:
        s_obj = ServerModel.objects.get(manager_ip__exact=manager_ip)
        s_obj.status = status
        s_obj.online_time = utc_minute_time_to_local(online_time)
        s_obj.expired_time = utc_minute_time_to_local(expired_time)
        s_obj.charge_type = charge_type
        s_obj.instance_id = instance_id
        s_obj.instance_name = instance_name
        s_obj.instance_type = instance_type
        s_obj.public_ip = public_ip
        s_obj.save(update_fields=["status","online_time","expired_time","charge_type","instance_id",
                                  "instance_name","instance_type","public_ip","last_update_time"])
        msg = "ServerModel 中更新 manager_ip: %s 的实例信息成功...." %(manager_ip)
        logger.info(msg)
    except Exception as e:
        msg = "ServerModel 中更新 manager_ip: %s 的实例信息失败, 错误信息: %s" %(manager_ip,e.args)
        logger.error(msg)
    return msg

@shared_task(bind=True,name="resources.tasks.aLiYunCmdb",ignore_result=False)
def aLiYunCmdbAdd(self,server_info):
    try:
        r = requests.post("http://oops.service.oops:20018/server/auto/",
                          headers={'content-type': 'application/json'},
                          data=json.dumps(server_info))
    except Exception as e:
        logger.error("访问运维平台 API 接口失败.....")
        return
    if int(r.status_code) == 201:
        logger.info("服务器: %s 信息 post 到 API 接口成功" %(server_info.get("manager_ip")))
        return "服务器: %s 添加成功" %(server_info.get("manager_ip"))
    else:
        logger.error('服务器: %s 信息 post 到 API 接口失败,错误信息: %s' % (r.content,server_info.get("manager_ip")))

@shared_task(bind=True,name="resources.tasks.updateAliYunCmdbList",ignore_result=False)
def updateAliYunCmdbList(self):
    local_aliyun_server_list = list(ServerModel.objects.filter(type__exact='cloud').values_list("manager_ip",flat=True))
    local_aliyun_server_add = []
    local_aliyun_server_delete = []

    try:
        aliyun_list = aLiYunEcs().aliyunDescribeInstances()
    except Exception as e:
        logger.error("从 阿里云API 获取服务器信息失败,错误信息: %s" %(e.args))
        return
    else:
        aliyun_ecs_list = list(aliyun_list.keys())
        local_aliyun_server_add = list(set(aliyun_ecs_list).difference(set(local_aliyun_server_list)))
        local_aliyun_server_delete = list(set(local_aliyun_server_list).difference(set(aliyun_ecs_list)))
        update_server_list = list(set(local_aliyun_server_list).intersection(set(aliyun_ecs_list)))
        update_instance_info = [(mi,
                                 aliyun_list[mi]["status"],
                                 aliyun_list[mi]["online_time"],
                                 aliyun_list[mi]["expired_time"],
                                 aliyun_list[mi]["charge_type"],
                                 aliyun_list[mi]["instance_id"],
                                 aliyun_list[mi]["instance_name"],
                                 aliyun_list[mi]["instance_type"],
                                 aliyun_list[mi]["public_ip"],
                               ) for mi in update_server_list]
        update_apps_info = [(mi,aliyun_list[mi]["instance_name"]) for mi in update_server_list]
        logger.info("update_apps_info: %s" %(update_apps_info))
    try:
        idc_obj = IdcModel.objects.get(name__exact="cn-beijing-a")
    except:
         idc_obj = IdcModel.objects.first()

    if local_aliyun_server_add:
        ''' 添加服务器到本地 ServerModel 模型；同时更新服务器与app的关联关系 '''
        server_add_task = group(chain(aLiYunCmdbAdd.s(aliyun_list[ip]),
                                      aLiYunCmdbUpdateApps.si(ip,aliyun_list[ip]["instance_name"])
                                      ) for ip in local_aliyun_server_add)
        server_add_task.delay()
        for s in local_aliyun_server_add:
            try:
                with open("/etc/ansible/hosts", 'a+') as f:
                    f.seek(0)
                    if "%s\n" % (s) not in f.readlines():
                        f.write("%s\n" % (s))
            except Exception as e:
                logger.error("自动添加服务器: %s 到 ansible host 文件失败,错误信息: %s" %(s, e.args))
                continue

    if local_aliyun_server_delete:
        ''' 将在阿里云上不存在的服务器,从本地的 ServerModel 模型中删除 '''
        try:
            ServerModel.objects.filter(manager_ip__in=local_aliyun_server_delete).delete()
        except Exception as e:
            logger.error("自动删除服务器: %s,错误信息: %s" %(','.join(local_aliyun_server_delete), e.args))
        else:
            logger.info("服务器: %s 自动删除成功" %(','.join(local_aliyun_server_delete)))

    if update_server_list:
        ''' 
        批量更新服务器的状态;如果服务器挂了,那么服务器上的定时脚本是不能更新状态的,所以有如下方法实现更新状态:
        <1> 使用这种阿里云的 api，定期的更新 云服务器状态
        <2> 对于 IDC 的服务器，只能根据 zabbix 的不可达告警 或者 判断 服务器信息的更新时间来 更新状态
       '''
        update_instance_server = updateCmdbInstanceInfo.chunks(update_instance_info,10)
        update_instance_server.delay()
        ''' 更新服务器与 APP 的关联'''
        update_apps_server = aLiYunCmdbUpdateApps.chunks(update_apps_info,10)
        update_apps_server.delay()

@shared_task(bind=True,name="resources.tasks.aLiYunCmdbUpdateApps",ignore_result=False)
def aLiYunCmdbUpdateApps(self,manager_ip,instance_name):
    '''
        根据 CmdbModel 模型中的 instance_name 字段自动添加 CMDB,如果没有该字段则不能自动添加 CMDB,
        因此该方法适用于 Aliyun 上的服务器，IDC中的服务器需要手动添加，该方法也不会修改IDC服务器 CMDB 的信息
    '''
    try:
        s_obj = ServerModel.objects.get(manager_ip__exact=manager_ip)
        app_name_list = instance_name.split("_")[-2::-1]
    except Exception as e:
        logger.error("传入的值有误,或者获取服务器对象失败，传入值: %s, %s" %(manager_ip,instance_name))
        return

    if not app_name_list:
        logger.error("阿里云上服务器: %s 配置实例名 %s 格式不正确" % (manager_ip, instance_name))
        return

    app_obj_list = []
    for app_name in app_name_list:
        try:
            app_obj = AppConfigModel.objects.get(name__exact=app_name)
        except AppConfigModel.DoesNotExist:
            app_obj = AppConfigModel.objects.create(**{"name": app_name})

        app_obj_list.append(app_obj)

    try:
        s_obj.appconfigmodel_set.set(app_obj_list)
    except Exception as e:
        logger.error("更新服务器: %s 的 APP 信息失败,错误信息: %s" %(manager_ip,e.args))
    else:
        logger.info("更新服务器: %s 的 APP 信息成功" %(manager_ip))

    return {manager_ip: app_name_list}

@shared_task(bind=True,name="resources.tasks.addTest",ignore_result=False)
def add(self,x,y):
    log_str = '''
        task_id: %s,
        task_group: %s,
        task_chord: %s,
        task_root_id: %s,
        task_parent_id: %s,
        task_worker_name: %s,
        task_queue_name: %s,
        task_delivery_info: %s
    ''' %(self.request.id,self.request.group,self.request.chord,
          self.request.root_id,self.request.parent_id,self.request.hostname,
          self.request.reply_to,self.request.delivery_info)

    logger.info(log_str)
    return x + y,10

@shared_task(bind=True,name="resources.tasks.sumTest",ignore_result=False)
def mysum(self,x):
    log_str = '''
        task_id: %s,
        task_group: %s,
        task_chord: %s,
        task_root_id: %s,
        task_parent_id: %s,
        task_worker_name: %s,
        task_queue_name: %s,
        task_delivery_info: %s
    ''' %(self.request.id,self.request.group,self.request.chord,self.request.root_id,self.request.parent_id,self.request.hostname,self.request.reply_to,self.request.delivery_info)
    logger.info(log_str)
    logger.info("我收到的参数: %s" %(x))
    return sum(x)

@shared_task(bind=True,name="resources.tasks.mulTest",ignore_result=False)
def mymul(self,x,y):
    log_str = '''
        task_id: %s,
        task_group: %s,
        task_chord: %s,
        task_root_id: %s,
        task_parent_id: %s,
        task_worker_name: %s,
        task_queue_name: %s,
        task_delivery_info: %s
    ''' %(self.request.id,self.request.group,self.request.chord,
          self.request.root_id,self.request.parent_id,self.request.hostname,
          self.request.reply_to,self.request.delivery_info)
    logger.info(log_str)
    logger.info("我收到的 X 参数: %s" %(x))
    logger.info("我收到的 Y 参数: %s" %(y))
    return x * y
