from django_filters import  rest_framework as filters
from appsmanager.models import AppConfigModel

class AppConfigFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains", label="应用名称")
    server = filters.CharFilter(field_name="server__manager_ip", lookup_expr="icontains", label="应用所在的服务器IP")
    manage_team = filters.CharFilter(field_name="manage_team__name", lookup_expr="icontains", label="应用管理组")
    env = filters.CharFilter(field_name="env", lookup_expr="exact", label="应用所属环境")
    way = filters.CharFilter(field_name="way", lookup_expr="exact", label="应用部署方式")
    port = filters.CharFilter(field_name="ports", lookup_expr="icontains", label="应用监听的端口")

    class Meta:
        model = AppConfigModel
        fields = ["name","server","manage_team","env","way","port"]