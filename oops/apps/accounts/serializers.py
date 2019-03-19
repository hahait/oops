from .models import UserProfileModel
from rest_framework import serializers
import re
from django.contrib.auth.models import Group,Permission,ContentType
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    '''
        用户信息序列化
    '''
    password_repeat = serializers.CharField(required=True,min_length=8,write_only=True)
    groups = serializers.PrimaryKeyRelatedField(required=False,queryset=Group.objects.all(),many=True)

    class Meta:
        model = UserProfileModel
        fields = ('id','username','groups','password','password_repeat','email','is_superuser',
                  'is_active','cn_name','role','phone','last_update_time','date_joined')
        read_only_fields = ('id','last_update_time','date_joined')
        extra_kwargs = {'password': {'write_only': True,'min_length':8},
                        'date_joined': {'format': '%Y-%m-%d %H:%M:%S'},
                        'last_update_time': {'format': '%Y-%m-%d %H:%M:%S'}}

    def validate_password(self,password):
        # try:
        #    re.match("\D",password).group()
        # except Exception as e:
        #    raise forms.ValidationError("密码必须以字母开头")

        try:
            re.search('[A-Z]', password).group()
            re.search('[a-z]', password).group()
            re.search('[0-9]', password).group()
            re.search('[!@#$%^&*()_\.;\"\',\?]', password).group()
        except Exception as e:
            raise serializers.ValidationError("密码必须包含大写字母、小写字母、数字和特殊字符('!@#$%^&*()_')")
        else:
            return password

    def validate_phone(self, phone):
        try:
            re.match("1[3,4,5,7,8]\d{9}$", phone).group()
        except Exception as e:
            raise serializers.ValidationError("输入的手机号格式不正确")
        else:
            return phone

    def validate(self, attrs):
        print("groups: ",attrs)
        if attrs.get('password'):
            if attrs.get('password') != attrs.get('password_repeat'):
                raise serializers.ValidationError("两次输入密码不一致,请重新输入")
            del attrs['password_repeat']
        return attrs

    def to_representation(self, instance):
        ret = super(UserSerializer,self).to_representation(instance)
        ret["groups"] = [{"id": group.id,"name": group.name} for group in instance.groups.all()]
        return  ret

class GroupSerializer(serializers.ModelSerializer):
    '''
         用户组序列化
    '''
    class Meta:
        model = Group
        fields = ("id","name")

class GroupRelateSerializer(serializers.ModelSerializer):
    '''
         用户组序列化,包含与用户和权限的关联关系
    '''
    user = serializers.PrimaryKeyRelatedField(source="user_set", required=False,
                                              queryset=UserProfileModel.objects.all(), many=True)
    permissions = serializers.PrimaryKeyRelatedField(required=False, queryset=Permission.objects.all(), many=True)

    class Meta:
        model = Group
        fields = ("id","name", "user", "permissions")

    def to_representation(self, instance):
        group_obj = instance
        ret = super(GroupRelateSerializer,self).to_representation(instance)
        ret["user"] = [{"id": user.id,"username": user.username,"cn_name":user.cn_name,"is_active":user.is_active} for user in group_obj.user_set.all()]
        ret["permissions"] = [{"id": perm.id, "name": perm.name, "codename": perm.codename} for perm in group_obj.permissions.all()]
        return ret

class ContentTypeSerializer(serializers.ModelSerializer):
    '''
        权限序列化
    '''
    permission = serializers.PrimaryKeyRelatedField(source="permission_set",required=False, queryset=Permission.objects.all(), many=True)

    class Meta:
        model = ContentType
        fields = ["app_label","model","permission"]

    def to_representation(self, instance):
        ct_obj = instance
        ret = super(ContentTypeSerializer,self).to_representation(instance)
        ret["permission"] = [{"id":perm.id,"codename":perm.codename,"name":perm.name} for perm in ct_obj.permission_set.all()]
        return ret

class PermissionSerializer(serializers.ModelSerializer):
    '''
        权限表序列化
    '''
    class Meta:
        model = Permission
        fields = ["id","name","codename","content_type"]

    def to_representation(self, instance):
        perm_obj = instance
        ct = perm_obj.content_type
        ret = super(PermissionSerializer,self).to_representation(instance)
        ret["content_type"] = {"id":ct.id,"app_label":ct.app_label,"model":ct.model}
        ret["status"] = False
        return ret