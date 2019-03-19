from django_filters import  rest_framework as filters
from .models import IdcModel,CabinetModel,ServerManufacturerModel,ServerModelModel,ServerModel,NetworkCardModel,IpAddrModel

class IdcFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name",lookup_expr="icontains",label="IDC 简称")
    class Meta:
        model = IdcModel
        fields = ["name"]


class CabinetFilter(filters.FilterSet):
    label = filters.CharFilter(field_name="label",lookup_expr='icontains',label="标签")
    idc = filters.CharFilter(field_name="idc__name", lookup_expr='icontains', label="所属 IDC")
    class Meta:
        model = CabinetModel
        fields = ["label","idc"]

class ServerManufacturerFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name",lookup_expr='icontains',label="制造商名称")
    class Meta:
        model = ServerManufacturerModel
        fields = [ "name"]

class ServerModelFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name",lookup_expr="icontains",label="设备型号")
    manufacturer = filters.CharFilter(field_name="manufacturer__name",lookup_expr="icontains",label="制造商名称")
    class Meta:
        model = ServerModelModel
        fields = ["name","manufacturer"]

class ServerFilter(filters.FilterSet):
    ip = filters.CharFilter(field_name="networkcardmodel__ipaddrmodel__ip",lookup_expr="icontains",label="服务器管理IP")
    public_ip = filters.CharFilter(field_name="public_ip", lookup_expr="icontains", label="服务器公网IP")
    hostname = filters.CharFilter(field_name="hostname",lookup_expr="icontains",label="主机名")
    instance_id = filters.CharFilter(field_name="instance_id", lookup_expr="icontains", label="实例ID")
    uuid = filters.CharFilter(field_name="uuid", lookup_expr="icontains", label="UUID")
    type = filters.CharFilter(field_name="type", lookup_expr="exact", label="类型")
    env = filters.CharFilter(field_name="env", lookup_expr="exact", label="环境")
    brand = filters.CharFilter(field_name="server_brand__name", lookup_expr="icontains", label="制造商名称")
    model = filters.CharFilter(field_name="server_model__name", lookup_expr="icontains", label="型号名称")
    idc = filters.CharFilter(field_name="idc__name", lookup_expr="icontains", label="所属 IDC")
    cabinet = filters.CharFilter(field_name="cabinet__label", lookup_expr="icontains", label="机柜信息")
    status = filters.CharFilter(field_name="status", lookup_expr="exact", label="服务器状态")
    sn = filters.CharFilter(field_name="sn_code", lookup_expr="icontains", label="SN 码")

    class Meta:
        model = ServerModel
        fields = ["hostname","env","type","brand","model", "idc","cabinet","status","sn_code","ip","public_ip","instance_id"]

class NetworkCardFilter(filters.FilterSet):
    mac = filters.CharFilter(field_name="mac",lookup_expr="icontains",label="MAC 地址")
    name = filters.CharFilter(field_name="name",lookup_expr="icontains",label="网卡名称")
    status = filters.CharFilter(field_name="status",lookup_expr="exact",label="状态")
    server = filters.CharFilter(field_name="server__hostname",lookup_expr="icontains",label="所属服务器")
    ip = filters.CharFilter(field_name="ipaddrmodel__ip",lookup_expr="icontains",label="网卡IP")
    class Meta:
        model = NetworkCardModel
        fields = ["mac","name","status","server","ip"]

class IpAddrFilter(filters.FilterSet):
    ip = filters.CharFilter(field_name="ip",lookup_expr="icontains",label="IP 地址")
    class Meta:
        model = IpAddrModel
        fields = ["ip"]