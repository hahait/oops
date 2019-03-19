from rest_framework import serializers
from appsmanager.models import AppConfigModel


class AppConfigWithRealteSerializer(serializers.ModelSerializer):
    '''
        应用配置序列化,包含关联关系的字段
    '''
    class Meta:
        model = AppConfigModel
        fields = '__all__'
        read_only_fields = ["id", "create_time", "last_update_time"]
        extra_kwargs = {'create_time': {'format': '%Y-%m-%d %H:%M:%S'},
                        'last_update_time': {'format': '%Y-%m-%d %H:%M:%S'}}

    def to_representation(self, instance):
        ret = super(AppConfigWithRealteSerializer,self).to_representation(instance)
        ret["server"] = [{"id": s.id, "manager_ip": s.manager_ip} for s in instance.server.all()]
        ret["manage_team"] = [{"id": mt.id, "name": mt.name} for mt in instance.manage_team.all()]
        return  ret

class AppConfigSimpleSerializer(serializers.ModelSerializer):
    '''
        应用配置序列化,仅包含 id 和 name 字段
    '''
    class Meta:
        model = AppConfigModel
        fields = ["id","name"]
        read_only_fields = ["id"]