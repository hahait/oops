from rest_framework import serializers
from .models import IdcModel,CabinetModel,ServerManufacturerModel,ServerModelModel,ServerModel,NetworkCardModel,IpAddrModel
from rest_framework.validators import UniqueValidator,UniqueTogetherValidator
from utils.oops_log import logInfo,logError

class IdcSerializer(serializers.ModelSerializer):
    '''
        IDC 序列化
    '''

    cabinets = serializers.PrimaryKeyRelatedField(source='cabinetmodel_set',required=False,queryset=CabinetModel.objects.all(),many=True)

    class Meta:
        model = IdcModel
        fields = ["id","name","cn_name","address","phone","email","contact_user","cabinets","create_time","last_update_time"]
        read_only_fields = ["id","create_time","last_update_time"]
        extra_kwargs = {'create_time': {'format': '%Y-%m-%d %H:%M:%S'},
                        'last_update_time': {'format': '%Y-%m-%d %H:%M:%S'}}

    def to_representation(self, instance):
        idc_obj = instance
        ret = super(IdcSerializer,self).to_representation(instance)
        ret["cabinets"] = [{"id": cm.id, "label": cm.label, "description": cm.description, "power": cm.power} for cm in idc_obj.cabinetmodel_set.all()]
        return ret

class CabinetSerializer(serializers.ModelSerializer):
    '''
        机柜序列化
    '''
    class Meta:
        model = CabinetModel
        fields = ["id","label","description","power","idc","create_time","last_update_time"]
        extra_kwargs = {'create_time': {'format': '%Y-%m-%d %H:%M:%S'},
                        'last_update_time': {'format': '%Y-%m-%d %H:%M:%S'}}

    def to_representation(self, instance):
        idc_obj = instance.idc
        ret = super(CabinetSerializer,self).to_representation(instance)
        ret["idc"] = {"id": idc_obj.id,"name": idc_obj.name,"cn_name": idc_obj.cn_name}
        return ret

class ServerManufacturerSerializer(serializers.ModelSerializer):
    '''
        服务器制造商系列化
    '''

    models = serializers.PrimaryKeyRelatedField(source='servermodelmodel_set',required=False,queryset=ServerModelModel.objects.all(),many=True)
    class Meta:
        model = ServerManufacturerModel
        fields = ["id","name","cn_name","phone","email","contact_user","models","create_time","last_update_time"]
        extra_kwargs = {'create_time': {'format': '%Y-%m-%d %H:%M:%S'},
                        'last_update_time': {'format': '%Y-%m-%d %H:%M:%S'}}

    def to_representation(self, instance):
        sm_obj = instance
        ret = super(ServerManufacturerSerializer,self).to_representation(instance)
        ret["models"] = [{"id": m.id, "name": m.name} for m in sm_obj.servermodelmodel_set.all()]
        return  ret

class ServerModelSerializer(serializers.ModelSerializer):
    '''
        服务器型号序列化
    '''
    class Meta:
        model = ServerModelModel
        fields = ["name","manufacturer","create_time","last_update_time"]
        extra_kwargs = {'create_time': {'format': '%Y-%m-%d %H:%M:%S'},
                        'last_update_time': {'format': '%Y-%m-%d %H:%M:%S'}}

    def to_representation(self, instance):
        mf_obj = instance.manufacturer
        ret = super(ServerModelSerializer,self).to_representation(instance)
        ret["manufacturer"] = {"id": mf_obj.id,"name": mf_obj.name,"cn_name": mf_obj.cn_name}
        return ret

class ServerAutoServializer(serializers.ModelSerializer):
    '''
        服务器信息自动添加和更新 序列化
        注意：这里之所以不指定 unique 是为了使用 POST 方法提交的数据除了创建外还能够更新，否则更新时 字段检查通不过；因此最终只能通过保存数据库时判断唯一性了
        uuid = serializers.CharField(required=True,max_length=50,validators=[UniqueValidator(queryset=ServerModel.objects.all())],label="服务器 UUID",help_text="服务器 UUID")
        hostname = serializers.CharField(required=True, max_length=50, validators=[UniqueValidator(queryset=ServerModel.objects.all())],label="主机名", help_text="主机名")
    '''
    uuid = serializers.CharField(required=True, max_length=50, label="服务器 UUID", help_text="服务器 UUID")
    hostname = serializers.CharField(required=True, max_length=50,label="主机名", help_text="主机名")
    idc = serializers.CharField(required=True, max_length=100, label="机房名称", help_text="机房名称")
    server_brand = serializers.CharField(required=True, max_length=100,label="服务器制造商",help_text="服务器制造商")
    server_model = serializers.CharField(required=True, max_length=100, label="服务器型号", help_text="服务器型号")
    network = serializers.JSONField(required=True, label="服务器网卡信息", help_text="服务器网卡信息")

    class Meta:
        model = ServerModel
        fields = ["uuid","hostname","instance_id","instance_name","server_brand","server_model","sn_code","os_version","cpu_count","type","idc",
                  "mem","swap","disk","disk_mount","instance_type","charge_type","status","idrac_ip","manager_ip",
                  "network","public_ip","online_time","expired_time"]

    def validate_server_brand(self,server_brand):
        try:
            sb_obj = ServerManufacturerModel.objects.get(name__exact=server_brand)
        except ServerManufacturerModel.DoesNotExist:
            return ServerManufacturerModel.objects.create(name=server_brand)
        return sb_obj

    def validate_idc(self,idc):
        try:
            idc_obj = IdcModel.objects.get(name__exact=idc)
        except IdcModel.DoesNotExist:
            return IdcModel.objects.create(name=idc)
        return idc_obj

    def validate(self,attrs):
        sm_str = attrs.get("server_model")
        sb_obj = attrs.get("server_brand")
        if sb_obj and sm_str:
            try:
                sm_obj = sb_obj.servermodelmodel_set.filter(name__exact=sm_str)[0]
            except:
                sm_obj = ServerModelModel.objects.create(name=sm_str,manufacturer=sb_obj)
            finally:
                attrs["server_model"] = sm_obj
        return attrs

    def check_ip(self,network_obj,ips_list):
        '''
            检查 IP对象是不是存在，否则就创建，同时更新网卡对象与IP对象的关联关系
        '''
        ip_obj_list = []
        for ip in ips_list:
            try:
                ip_obj = network_obj.ipaddrmodel_set.get(ip__exact=ip.get("ip"), netmask__exact=ip.get("netmask"))
            except IpAddrModel.DoesNotExist:
                ''' 创建 IpAddr 对象 '''
                logError().error("IpAddrModel 中 查不到 ip: %s netmask: %s 的对象，所以需要创建这个对象..." %(ip['ip'],ip['netmask']))
                ip["networkcard"] = network_obj
                ip_obj = IpAddrModel.objects.create(**ip)
            finally:
                ip_obj_list.append(ip_obj)
        network_obj.ipaddrmodel_set.set(ip_obj_list)
        ''' 删除掉未绑定网卡的IP地址 '''
        IpAddrModel.objects.filter(networkcard_id__isnull=True).delete()

    def create_network_card_obj(self,server_obj,network_card):
        '''
            创建网卡对象
        '''
        network_card["server"] = server_obj
        network_obj = NetworkCardModel.objects.create(**network_card)
        return network_obj

    def check_network(self,server_obj,network_list):
        '''
            检查 网卡 对象是不是存在，否则就创建，同时更新服务器对象与网卡对象的关联关系
        '''
        network_obj_list = []
        for nc in network_list:
            ips_list = nc.pop("ips")
            try:
                nc_obj = server_obj.networkcardmodel_set.get(mac__exact=nc.get("mac"),name__exact=nc.get("name"))
            except NetworkCardModel.DoesNotExist:
                ''' 创建 network '''
                nc_obj = self.create_network_card_obj(server_obj,nc)
            finally:
                network_obj_list.append(nc_obj)
                self.check_ip(nc_obj,ips_list)

        server_obj.networkcardmodel_set.set(network_obj_list)
        ''' 删除掉 未绑定服务器的网卡，也就是无用数据 '''
        NetworkCardModel.objects.filter(server_id__isnull=True).delete()

    def create(self, validated_data):
        '''
            由于涉及到多个串行的关联关系以及服务器信息的上报方式(都是通过POST方式上报到接口)
            自定义 create 方法，这里面包含的数据更新(update)方法
        '''
        network_list = validated_data.pop("network")
        try:
            server_obj = ServerModel.objects.get(uuid__exact=validated_data.get("uuid"))
        except ServerModel.DoesNotExist:
            server_obj = ServerModel.objects.create(**validated_data)
        else:
            ''' 更新服务器信息 '''
            server_obj = self.update(server_obj,validated_data)

        self.check_network(server_obj,network_list)

        return  server_obj

    def to_representation(self, instance):
        ret = {"hostname": instance.hostname,"uuid": instance.uuid}
        return ret

class ServerSerializer(serializers.ModelSerializer):
    '''
        服务器序列化
    '''

    class Meta:
        model = ServerModel
        fields = "__all__"
        read_only_fields = ["uuid","hostname","instance_id","instance_name","server_brand","server_model","sn_code","os_version",
                            "cpu_count","mem","swap","disk","disk_mount","instance_type","charge_type","idrac_ip"]
        extra_kwargs = {'online_time': {'format': '%Y-%m-%d %H:%M:%S'},
                        'offline_time': {'format': '%Y-%m-%d %H:%M:%S'},
                        'expired_time': {'format': '%Y-%m-%d %H:%M:%S'},
                        'last_update_time': {'format': '%Y-%m-%d %H:%M:%S'}}

    def to_representation(self, instance):
        idc_obj = instance.idc
        ret = super(ServerSerializer,self).to_representation(instance)
        ret["idc"] = {"id":idc_obj.id, "name":idc_obj.name, "cn_name":idc_obj.cn_name} if ret.get("idc") else ''
        ret["network"] = [{"name": nc.name, "mac": nc.mac, "status": nc.status, "ips": [{"id": ip.id, "ip": ip.ip} for ip in nc.ipaddrmodel_set.all()]} for nc in instance.networkcardmodel_set.all()]
        ret["server_brand"] = {"name": instance.server_brand.name,"cn_name": instance.server_brand.cn_name}
        ret["server_model"] = {"name": instance.server_model.name}
        ret["cabinet"] = {"id": instance.cabinet.id,"label": instance.cabinet.label} if ret.get("cabinet") else ''
        return ret

class ServerForRelateSerializer(serializers.ModelSerializer):
    '''
        服务器序列化,专用于 关联服务器时使用
    '''

    class Meta:
        model = ServerModel
        fields = ["id","hostname","manager_ip"]

class NetworkCardSerializer(serializers.ModelSerializer):
    '''
        网卡序列化
    '''
    class Meta:
        model = NetworkCardModel
        fields = "__all__"
        read_only_fields = ["mac","name","status","server","create_time","last_update_time"]
        extra_kwargs = {'create_time': {'format': '%Y-%m-%d %H:%M:%S'},
                        'last_update_time': {'format': '%Y-%m-%d %H:%M:%S'}}
        validators = UniqueTogetherValidator(queryset=NetworkCardModel.objects.all(),fields=["mac","name"])

    def to_representation(self, instance):
        server_obj = instance.server
        ret = super(NetworkCardSerializer,self).to_representation(instance)
        ret["server"] = {"hostname": server_obj.hostname, "uuid": server_obj.uuid}
        ret["ips"] = [{"ip": ip.ip} for ip in instance.ipaddrmodel_set.all()]
        return  ret

class IpAddrSerializer(serializers.ModelSerializer):
    '''
        IP地址 序列化
    '''
    class Meta:
        model = IpAddrModel
        fields = "__all__"
        read_only_fields = ["ip","netmask","gateway","networkcard","create_time","last_update_time"]
        extra_kwargs = {'create_time': {'format': '%Y-%m-%d %H:%M:%S'},
                        'last_update_time': {'format': '%Y-%m-%d %H:%M:%S'}}

    def to_representation(self, instance):
        network_obj = instance.networkcard
        ret = super(IpAddrSerializer,self).to_representation(instance)
        ret["networkcard"] = {"mac": network_obj.mac, "name": network_obj.name}
        return  ret