from .models import IdcModel,CabinetModel,ServerManufacturerModel,ServerModelModel,ServerModel,NetworkCardModel,IpAddrModel
from .serializers import IdcSerializer,CabinetSerializer,ServerManufacturerSerializer,ServerModelSerializer,\
                            ServerSerializer,ServerAutoServializer,NetworkCardSerializer,IpAddrSerializer,ServerForRelateSerializer
from rest_framework import viewsets
from rest_framework import mixins
from .filter import IdcFilter,CabinetFilter,ServerManufacturerFilter,ServerModelFilter,NetworkCardFilter,IpAddrFilter,ServerFilter
from  rest_framework.authentication import BasicAuthentication,SessionAuthentication
from rest_framework.reverse import reverse
from rest_framework.permissions import AllowAny
from django.forms.models import model_to_dict
import json
import time
class IdcViewSet(viewsets.ModelViewSet):
    '''
        list            : 获取IDC 列表
        create          : 创建 IDC 对象
        update          : 修改指定 IDC 对象
        delete          : 删除指定 IDC 对象
        read            : 获取指定 IDC 对象
        partial_update  : 部分修改指定 IDC 对象
    '''
    queryset = IdcModel.objects.all()
    serializer_class = IdcSerializer
    filterset_class = IdcFilter
    # extra_permission = {
    #     'GET': ['resources.view_idc'],
    # }

class CabinetViewSet(viewsets.ModelViewSet):
    '''
        list            : 获取 机柜 列表
        create          : 创建 机柜 对象
        update          : 修改指定 机柜 对象
        delete          : 删除指定 机柜 对象
        read            : 获取指定 机柜 对象
        partial_update  : 部分修改指定 机柜 对象
    '''
    queryset = CabinetModel.objects.all()
    serializer_class = CabinetSerializer
    filterset_class = CabinetFilter

class ServerManufacturerViewSet(viewsets.ModelViewSet):
    '''
        list            : 获取 服务器制造商 列表
        create          : 创建 服务器制造商 对象
        update          : 修改指定 服务器制造商 对象
        delete          : 删除指定 服务器制造商 对象
        read            : 获取指定 服务器制造商 对象
        partial_update  : 部分修改指定 服务器制造商 对象
    '''
    queryset = ServerManufacturerModel.objects.all()
    serializer_class = ServerManufacturerSerializer
    filterset_class = ServerManufacturerFilter

class ServerModelViewSet(viewsets.ModelViewSet):
    '''
        list            : 获取 服务器型号 列表
        create          : 创建 服务器型号 对象
        update          : 修改指定 服务器型号 对象
        delete          : 删除指定 服务器型号 对象
        read            : 获取指定 服务器型号 对象
        partial_update  : 部分修改指定 服务器型号 对象
    '''
    queryset = ServerModelModel.objects.all()
    serializer_class = ServerModelSerializer
    filterset_class = ServerModelFilter

class ServerAutoViewSet(mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
    '''
        create          : 创建 服务器 对象
        update          : 修改指定 服务器 对象
        delete          : 删除指定 服务器 对象
        partial_update  : 部分修改指定 服务器 对象
    '''
    queryset = ServerModel.objects.all()
    serializer_class = ServerAutoServializer
    permission_classes = (AllowAny,)

class ServerViewSet(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,
                    mixins.ListModelMixin,viewsets.GenericViewSet):
    '''
        list            : 获取 服务器 列表
        update          : 修改指定 服务器 对象
        delete          : 删除指定 服务器 对象
        read            : 获取指定 服务器 对象
        partial_update  : 部分修改指定 服务器 对象
    '''
    queryset = ServerModel.objects.all()
    serializer_class = ServerSerializer
    filterset_class = ServerFilter
    permission_classes = [AllowAny,]

class ServerForRelateViewSet(viewsets.ReadOnlyModelViewSet):
    '''
        list            : 获取 服务器 列表
    '''
    queryset = ServerModel.objects.all().order_by('id')
    serializer_class = ServerForRelateSerializer
    permission_classes = [AllowAny,]

class NetworkCardViewSet(viewsets.ReadOnlyModelViewSet):
    '''
        list            : 获取 网卡 列表
        read            : 获取指定 网卡 对象
    '''
    queryset = NetworkCardModel.objects.all()
    serializer_class = NetworkCardSerializer
    filterset_class = NetworkCardFilter

class IpAddrViewSet(viewsets.ReadOnlyModelViewSet):
    '''
        list            : 获取 IP 列表
        read            : 获取指定 IP 对象
    '''
    queryset = IpAddrModel.objects.all()
    serializer_class = IpAddrSerializer
    filterset_class = IpAddrFilter

class CmdbThriftService():
    def get_cmdb_info(self,server_id):
        try:
            server_obj = ServerModel.objects.get(id__exact=server_id)
        except:
            return {}
        else:
            server_info = model_to_dict(server_obj)
            server_info.pop("expired_time")
            server_info.pop("online_time")
            return json.dumps(server_info)

class IdcThriftService():
    def get_idc_info(self,idc_id):
        try:
            idc_obj = IdcModel.objects.get(id__exact=idc_id)
        except:
            data =  {"aa":"我是空的"}
        else:
            idc_info = model_to_dict(idc_obj)
            data = idc_info

        return json.dumps(data)