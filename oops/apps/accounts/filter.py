from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group,ContentType,Permission

User = get_user_model()

class UserFilter(filters.FilterSet):
    username = filters.CharFilter(field_name="username",lookup_expr='icontains',label="用户名")
    phone = filters.CharFilter(field_name="phone", lookup_expr='icontains', label="手机号")
    group = filters.CharFilter(field_name="groups__name", lookup_expr='icontains', label="用户组名")
    class Meta:
        model = User
        fields = ["username","phone","group"]

class GroupFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name',lookup_expr='icontains',label="用户组名")
    class Meta:
        model = Group
        fields = ["name"]

class GroupRelateFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name',lookup_expr='icontains',label="用户组名")
    user = filters.CharFilter(field_name="user__username",lookup_expr='icontains',label="用户名")
    class Meta:
        model = Group
        fields = ["name","user"]

class ContentTypeFilter(filters.FilterSet):
    label = filters.CharFilter(field_name="app_label",lookup_expr='icontains',label="APP名称")
    model = filters.CharFilter(field_name="model", lookup_expr='icontains', label="模型名称")
    class Meta:
        model = ContentType
        fields = ["label","model"]

class PermissionFilter(filters.FilterSet):
    label = filters.CharFilter(field_name="content_type__app_label",lookup_expr='icontains',label="APP名称")
    model = filters.CharFilter(field_name="content_type__model", lookup_expr='icontains', label="模型名称")
    class Meta:
        model = Permission
        fields = ["label","model"]