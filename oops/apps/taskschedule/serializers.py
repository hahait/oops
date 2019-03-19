from rest_framework import serializers
from .models import CeleryTaskResultExtensionModel
from django_celery_beat.models import CrontabSchedule,IntervalSchedule,PeriodicTask
import pytz

class CeleryTaskResultSerializer(serializers.ModelSerializer):
    '''
        任务执行结果 序列化
    '''
    class Meta:
        model = CeleryTaskResultExtensionModel
        fields = ["uuid","name","state","args","kwargs","result","traceback","started","runtime","worker"]

class CrontabScheduleSerializer(serializers.ModelSerializer):
    '''
         执行任务周期(crontab)序列化
    '''
    class Meta:
        model = CrontabSchedule
        fields = "__all__"

    def validate(self, attrs):
        if CrontabSchedule.objects.filter(minute__exact=attrs.get("minute"),hour__exact=attrs.get("hour"),
                                          day_of_month__exact=attrs.get("day_of_month"),month_of_year__exact=attrs.get("month_of_year"),
                                          day_of_week__exact=attrs.get("day_of_week")):
            raise serializers.ValidationError("该任务周期在 CrontabSchedule 已经存在,请勿重复添加....")
        return  attrs

    def to_internal_value(self, data):
        data["timezone"] = pytz.timezone('Asia/Shanghai')
        return  data

    def to_representation(self, instance):
        ret = super(CrontabScheduleSerializer,self).to_representation(instance)
        ret["timezone"] = str(instance.timezone) if instance.timezone else ''
        return ret

class IntervalScheduleSerializer(serializers.ModelSerializer):
    '''
         执行任务周期(interval)序列化
    '''
    class Meta:
        model = IntervalSchedule
        fields = "__all__"

    def validate(self, attrs):
        if IntervalSchedule.objects.filter(every__exact=attrs.get("every"),period__exact=attrs.get("period")):
            raise serializers.ValidationError("该任务周期在 IntervalSchedule 已经存在,请勿重复添加....")
        return  attrs

class PeriodicTaskSerializer(serializers.ModelSerializer):
    '''
         定时任务序列化
    '''
    class Meta:
        model = PeriodicTask
        fields = "__all__"
        extra_kwargs = {'last_run_at': {'format': '%Y-%m-%d %H:%M:%S'},
                        'date_changed': {'format': '%Y-%m-%d %H:%M:%S'},
                        'start_time': {'format': '%Y-%m-%d %H:%M:%S'}
                        }

    def to_internal_value(self, data):
        if data.get("schedule_policy") == "Crontab":
            data["interval"] = None
            data["crontab"] = CrontabSchedule.objects.get(id__exact=data.get("crontab"))
        elif data.get("schedule_policy") == "Interval":
            data["crontab"] = None
            data["interval"] = IntervalSchedule.objects.get(id__exact=data.get("interval"))
        del data["schedule_policy"]
        if data.get("schedule_period"): del data["schedule_period"]

        data["enabled"] = eval(data["enabled"])
        return data

    def to_representation(self, instance):
        ret = super(PeriodicTaskSerializer,self).to_representation(instance)
        if instance.interval:
            ret["schedule_period"] = "%s %s" %(instance.interval.every, instance.interval.period)
            ret["schedule_policy"] = "Interval"
        else:
            c_obj = instance.crontab
            ret["schedule_period"] = "%s %s %s %s %s" %(c_obj.minute,c_obj.hour,c_obj.day_of_month,c_obj.month_of_year,c_obj.day_of_week)
            ret["schedule_policy"] = "Crontab"
        ret["enabled"] = str(ret["enabled"])
        return  ret