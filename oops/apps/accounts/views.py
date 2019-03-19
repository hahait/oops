from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from .serializers import UserSerializer,GroupSerializer,ContentTypeSerializer,GroupRelateSerializer,PermissionSerializer
from .models import UserProfileModel
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import  Group,ContentType,Permission
from utils.pagination import MyPagination
from .filter import UserFilter,GroupFilter,ContentTypeFilter,GroupRelateFilter,PermissionFilter
from rest_framework.response import Response
from rest_framework import  mixins
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import status
from django.forms.models import model_to_dict

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    '''
        list            : 获取用户 列表
        create          : 创建 用户 对象
        update          : 修改指定 用户 对象
        delete          : 删除指定 用户 对象
        read            : 获取指定 用户 对象
        partial_update  : 部分修改指定 用户 对象
    '''
    queryset = UserProfileModel.objects.all()
    serializer_class = UserSerializer
    filterset_class = UserFilter
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        serializer.validated_data["password"] = make_password(serializer.validated_data.get("password"))
        serializer.save()

    def perform_update(self, serializer):
        # print("get_obj: ",self.get_object())
        print("serializer.validated_data: ",serializer.validated_data)
        if serializer.validated_data.get("password"):
            serializer.validated_data["password"] = make_password(serializer.validated_data.get("password"))
        serializer.save()

class UserInfoViewSet(viewsets.ViewSet):
    '''
        list            : 获取登陆用户信息
    '''
    permission_classes = (IsAuthenticated,)
    def list(self, request, *args, **kwargs):
        data = model_to_dict(request.user,exclude=["first_name","last_name","password","date_joined","is_staff"])
        data["role"] = request.user.get_role_display()
        data["is_superuser"] = '是' if request.user.is_superuser else '否'
        data["last_login"] = data["last_login"].strftime("%Y-%m-%d %X")
        data["last_update_time"] = request.user.last_update_time.strftime("%Y-%m-%d %X")
        data["is_active"] = '正常' if request.user.is_active else '锁定'
        data['groups'] = [ {"id": group.id, "name": group.name} for group in data.get('groups') ]
        data['user_permissions'] = [{"id": perm.id, "name": perm.name} for perm in data.get('user_permissions')]
        return Response(data=data,status=status.HTTP_200_OK)

class GroupViewSet(viewsets.ModelViewSet):
    '''
        list            : 获取 用户组 列表
        create          : 创建 用户组 对象
        update          : 修改指定 用户组 对象
        delete          : 删除指定 用户组 对象
        read            : 获取指定 用户组 对象
        partial_update  : 部分修改指定 用户组 对象
    '''

    queryset = Group.objects.all().order_by('id')
    serializer_class = GroupSerializer
    filterset_class = GroupFilter

class GroupRelateViewSet(viewsets.ReadOnlyModelViewSet,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    '''
        list            : 获取 用户组 关联的 用户 和 权限列表
        update          : 修改指定 用户组 关联的 用户 和 权限
        delete          : 删除指定 用户组 关联的 用户 和 权限
        read            : 获取指定 用户组 关联的 用户 和 权限
        partial_update  : 部分修改指定 用户组 关联的 用户 和 权限
    '''

    queryset = Group.objects.all()
    serializer_class = GroupRelateSerializer
    filterset_class = GroupRelateFilter

    # def perform_update(self, serializer):
    #     g_obj = self.get_object()
    #     if serializer.validated_data.get("user"):
    #         print("group_user: ",user)
    #     if serializer.validated_data.get("permissions"):
    #         print("group_permissions: ", permissions)
    #     serializer.save()

class ContentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    '''
        list            : 获取 权限 列表
        create          : 创建 权限 对象
        update          : 修改指定 权限 对象
        delete          : 删除指定 权限 对象
        read            : 获取指定 权限 对象
        partial_update  : 部分修改指定 权限 对象
    '''

    queryset = ContentType.objects.all().order_by("id")
    serializer_class = ContentTypeSerializer
    filterset_class = ContentTypeFilter

class PermissionViewSet(viewsets.ReadOnlyModelViewSet,mixins.UpdateModelMixin):
    '''
        list            : 获取 权限 列表
        update          : 修改指定 权限 对象
        read            : 获取指定 权限 对象
        partial_update  : 部分修改指定 权限 对象
    '''

    queryset = Permission.objects.all().order_by("id")
    serializer_class = PermissionSerializer
    filterset_class = PermissionFilter