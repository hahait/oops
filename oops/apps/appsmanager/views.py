from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from appsmanager.models import AppConfigModel
from .filter import AppConfigFilter
from .serializers import AppConfigWithRealteSerializer,AppConfigSimpleSerializer

class AppConfigWithRelateViewSet(viewsets.ModelViewSet):
    '''
            list            : 获取 应用 列表
            create          : 创建 应用 对象
            update          : 修改指定 应用 对象
            delete          : 删除指定 应用 对象
            read            : 获取指定 应用 对象
            partial_update  : 部分修改指定 应用 对象
        '''
    queryset = AppConfigModel.objects.all().order_by("id")
    serializer_class = AppConfigWithRealteSerializer
    filterset_class = AppConfigFilter
    permission_classes = (AllowAny,)

class AppConfigSimpleViewSet(viewsets.ReadOnlyModelViewSet):
    '''
        list            : 获取 应用 列表
    '''
    queryset = AppConfigModel.objects.all().order_by("id")
    serializer_class = AppConfigSimpleSerializer
    permission_classes = (AllowAny,)