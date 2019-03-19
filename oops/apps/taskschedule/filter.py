from django_filters import  rest_framework as filters
from .models import CeleryTaskResultExtensionModel
from django_celery_beat.models import PeriodicTask

class CeleryTaskResultFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name",lookup_expr="icontains",label="任务名称")
    uuid = filters.CharFilter(field_name="uuid", lookup_expr="icontains", label="任务ID")
    args = filters.CharFilter(field_name="args", lookup_expr="icontains", label="任务位置参数")
    kwargs = filters.CharFilter(field_name="kwargs", lookup_expr="icontains", label="任务关键字参数")
    result = filters.CharFilter(field_name="result", lookup_expr="icontains", label="任务执行结果")

    class Meta:
        model = CeleryTaskResultExtensionModel
        fields = ["name","uuid","args","kwargs","result"]


class CrontabTaskFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name",lookup_expr="icontains",label="任务名称")
    task = filters.CharFilter(field_name="task", lookup_expr="icontains", label="任务Task")

    class Meta:
        model = PeriodicTask
        fields = ["name","task"]