from django.db import models
from django.contrib.auth.models import Group

class IdcModel(models.Model):
    name = models.CharField("简称",max_length=20,null=False,unique=True,help_text="简称")
    cn_name = models.CharField("中文名",max_length=100,null=True,help_text="中文名")
    address = models.CharField("地址",max_length=100,null=True,help_text="地址")
    phone = models.CharField("联系电话",max_length=20,null=True,help_text="联系电话")
    email = models.EmailField("邮箱",null=True,help_text="邮箱")
    contact_user = models.CharField("联系人",max_length=32,null=True,help_text="联系人")
    create_time = models.DateTimeField("添加时间",auto_now_add=True,null=True,help_text="添加时间")
    last_update_time = models.DateTimeField("最后一次更新时间",auto_now=True,null=True,help_text="最后一次修改时间")

    def __str__(self):
        return "%s-%s" %(self.name,self.cn_name)

    class Meta:
        verbose_name = "机房表"
        db_table = "resources_idc"
        permissions = (
            ("view_idc","查看idc列表"),
        )

class CabinetModel(models.Model):
    label = models.CharField("标签", max_length=100, null=False, unique=True, help_text="标签")
    description = models.CharField("描述信息", max_length=100, null=True, help_text="描述信息")
    power = models.CharField("电源信息", max_length=100, null=True, help_text="电源信息")
    idc = models.ForeignKey(IdcModel,verbose_name="所属机房",help_text="所属机房")
    create_time = models.DateTimeField("添加时间", auto_now_add=True, null=True, help_text="添加时间")
    last_update_time = models.DateTimeField("最后一次更新时间", auto_now=True, null=True, help_text="最后一次修改时间")

    def __str__(self):
        return "%s" % (self.label)

    class Meta:
        verbose_name = "机柜表"
        db_table = "resources_cabinet"
        permissions = (
            ("view_cabinet", "查看机柜列表"),
        )

class ServerManufacturerModel(models.Model):
    name = models.CharField("制造商名称",max_length=50,unique=True,db_index=True,help_text="制造商名称")
    cn_name = models.CharField("中文名", max_length=100, null=True,blank=True, help_text="中文名")
    phone = models.CharField("售后联系电话", max_length=20, null=True,blank=True, help_text="售后联系电话")
    email = models.EmailField("售后联系邮箱", null=True, blank=True,help_text="售后联系邮箱")
    contact_user = models.CharField("售后联系人", max_length=32, null=True,blank=True, help_text="售后联系人")
    create_time = models.DateTimeField("添加时间", auto_now_add=True, null=True, help_text="添加时间")
    last_update_time = models.DateTimeField("最后一次更新时间", auto_now=True, null=True, help_text="最后一次修改时间")

    def __str__(self):
        return "%s-%s" %(self.name,self.cn_name)

    class Meta:
        verbose_name = "服务器制造商"
        db_table = "resources_server_manufacturer"
        permissions = (
            ("view_server_manufacturer","查看服务器制造商列表"),
        )

class ServerModelModel(models.Model):
    name = models.CharField("服务器型号名称",max_length=50,db_index=True,help_text="服务器型号名称")
    manufacturer = models.ForeignKey(ServerManufacturerModel,verbose_name="所属制造商",help_text="所属制造商")
    create_time = models.DateTimeField("添加时间", auto_now_add=True, null=True, help_text="添加时间")
    last_update_time = models.DateTimeField("最后一次更新时间", auto_now=True, null=True, help_text="最后一次修改时间")

    def __str__(self):
        return "%s-%s" %(self.manufacturer.name,self.name)

    class Meta:
        verbose_name = "服务器型号"
        db_table = "resources_server_model"
        unique_together = ["name","manufacturer"]
        permissions = (
            ("view_server_model","查看服务器型号列表"),
        )

class ServerModel(models.Model):
    TYPE_CHOICES = (
        ("physical", "物理机"),
        ("virtual", "虚拟机"),
        ("cloud", "云主机"),
    )

    STATUS_CHOICES = (
        ("Running","运行中"),
        ("Starting","启动中"),
        ("Maintenance", "维护中"),
        ("Stopping","停止中"),
        ("Stopped","已下线"),
    )

    MONITOR_CHOICES = (
        ("0","正常"),
        ("1","未监控"),
    )

    CHARGE_TYPE_CHOICES = (
        ("PrePaid","包年包月"),
        ("PostPaid","按量付费"),
    )

    RENEWLI_STATUS_CHOICES = (
        ("AutoRenewal","自动续费"),
        ("Normal","手动续费"),
        ("NotRenewal","不在续费"),
        ("RenewalByUsed","按量付费"),
    )

    ENV_CHOICES = (
        ("online", "生产"),
        ("dev", "开发"),
        ("test", "测试"),
        ("gray", "预发布")
    )

    hostname = models.CharField("主机名", max_length=50, null=True, unique=True, db_index=True, help_text="主机名")
    uuid = models.CharField("服务器 UUID",max_length=50,null=True, unique=True,db_index=True,help_text="服务器 UUID")
    ssh_port = models.CharField("SSH 端口号", max_length=5, default="22", help_text="SSH 端口号")
    type = models.CharField("服务器类型", choices=TYPE_CHOICES, max_length=10,default="cloud",help_text="服务器类型")
    env = models.CharField("服务器所属环境", choices=ENV_CHOICES, max_length=10, default="online", help_text="服务器所属环境")
    server_brand = models.ForeignKey(ServerManufacturerModel,verbose_name="服务器制造商",null=True,help_text="服务器制造商")
    server_model = models.ForeignKey(ServerModelModel,verbose_name="服务器型号",null=True,help_text="服务器型号")
    os_version = models.CharField("系统版本", max_length=50, null=True,blank=True, help_text="系统版本")
    cpu_count = models.CharField("CPU核数", max_length=10, null=True,blank=True, help_text="CPU核数")
    mem = models.CharField("内存大小", max_length=20, null=True,blank=True, help_text="内存大小")
    swap = models.CharField("SWAP 空间大小", max_length=10, null=True,blank=True, help_text="SWAP 空间大小")
    disk = models.CharField("物理磁盘大小", max_length=1500, null=True,blank=True, help_text="物理磁盘大小")
    disk_mount = models.CharField("分区挂载情况", max_length=1500, null=True,blank=True, help_text="分区挂载情况")
    idc = models.ForeignKey(IdcModel,verbose_name="归属机房",null=True,blank=True,help_text="归属机房")
    status = models.CharField("服务器状态",choices=STATUS_CHOICES,max_length=20,default="Running",help_text="服务器状态")
    instance_id = models.CharField("实例ID",max_length=50,null=True,blank=True,help_text="实例ID,适用于云服务器")
    instance_name = models.CharField("实例名称",max_length=150,null=True,blank=True,help_text="实例名称,适用于云服务器")
    instance_type = models.CharField("实例规格", max_length=50, null=True,blank=True, help_text="实例规格,适用于云服务器")
    charge_type = models.CharField("付费类型", choices=CHARGE_TYPE_CHOICES, max_length=10, null=True,blank=True,help_text="付费类型,适用于云服务器")
    sn_code = models.CharField("服务器SN号",max_length=50,null=True,blank=True,help_text="服务器SN号,适用于 IDC 中服务器")
    idrac_ip = models.GenericIPAddressField("远程管理卡IP", protocol="IPv4", null=True,blank=True,help_text="远程管理卡IP，适用于IDC服务器")
    manager_ip = models.GenericIPAddressField("管理IP", protocol="IPv4", null=True, blank=True,help_text="管理IP，用于远程管理服务器")
    public_ip = models.GenericIPAddressField("公网IP", protocol="IPv4", null=True, blank=True, help_text="公网IP,适用于云服务未绑定到具体网卡的公网IP")
    cabinet = models.ForeignKey(CabinetModel, null=True,blank=True, verbose_name="机柜编号",help_text="机柜编号,适用于 IDC 中服务器")
    online_time = models.DateTimeField("服务器上架时间",auto_now_add=False,null=True,help_text="服务器上架时间")
    offline_time = models.DateTimeField("服务器下架时间",null=True,help_text="服务器下架时间")
    expired_time = models.DateTimeField("服务器过期/保时间",null=True,help_text="服务器过期/保时间")
    create_time = models.DateTimeField("添加时间", auto_now_add=True, null=True, help_text="添加时间")
    last_update_time = models.DateTimeField("最后一次更新时间",auto_now=True,null=True,help_text="最后一次更新时间")

    def __str__(self):
        return "%s-%s" %(self.hostname,self.manager_ip)

    class Meta:
        verbose_name = "服务器表"
        db_table = "resources_server"
        ordering = ["-id"]

class NetworkCardModel(models.Model):
    STATUS_CHOICES = (
        ("up", "UP"),
        ("down", "DOWN"),
        ("unknow","UNKNOW"),
    )

    mac = models.CharField("MAC 地址",
                           max_length=48,
                           null=False,
                           help_text="MAC 地址;由于 bond 导致 MAC 是可重复的;")
    name = models.CharField("网卡名称", max_length=100, null=False, help_text="网卡名称")
    status = models.CharField("端口状态", choices=STATUS_CHOICES, max_length=10, null=False,default='up',help_text="端口状态")
    server = models.ForeignKey(ServerModel, null=True, verbose_name="所属服务器",help_text="所属服务器")
    create_time = models.DateTimeField("添加时间", auto_now_add=True, null=True, help_text="添加时间")
    last_update_time = models.DateTimeField("最后一次更新时间", auto_now=True, null=True, help_text="最后一次修改时间")

    def __str__(self):
        return "%s-%s" % (self.name,self.mac)

    class Meta:
        verbose_name = "网卡"
        db_table = "resources_network_card"
        unique_together = ["mac","name"]

class IpAddrModel(models.Model):
    ip = models.GenericIPAddressField("IP地址",protocol="IPv4",unique=True,null=False,db_index=True,help_text="IP地址")
    netmask = models.CharField("网络掩码", max_length=100, null=False, help_text="网络掩码")
    networkcard = models.ForeignKey(NetworkCardModel,null=True, verbose_name="所属网卡",help_text="所属网卡")
    create_time = models.DateTimeField("添加时间", auto_now_add=True, null=True, help_text="添加时间")
    last_update_time = models.DateTimeField("最后一次更新时间", auto_now=True, null=True, help_text="最后一次修改时间")

    def __str__(self):
        return "%s" % (self.ip)

    class Meta:
        verbose_name = "IP地址"
        db_table = "resources_ip_addr"
        unique_together = ["ip","netmask"]

class ServerStatisticByDayModel(models.Model):
    myday = models.DateField("统计时间",null=False,unique=True)
    count = models.PositiveSmallIntegerField("服务器数量",null=False)
    last_update_time = models.DateTimeField("应用最后更新时间",auto_now=True,null=True)

    def __str__(self):
        return self.myday

    class Meta:
        verbose_name = "服务器按天统计表"
        db_table = 'resources_server_statistic_by_day'
        ordering = ['myday']

class FirewallRulesModel(models.Model):
    # workform_id = models.ForeignKey(WorkFormModel,verbose_name="关联工单记录",null=True)
    s_hostname = models.CharField("原主机名",max_length=100,null=True,blank=True)
    s_ip = models.CharField("源IP",max_length=15,null=False)
    d_hostname = models.CharField("目标主机名", max_length=100, null=True,blank=True)
    d_ip = models.CharField("目标IP", max_length=15, null=False)
    d_port = models.CharField("目标端口", max_length=100, null=False)
    protocol = models.CharField("网络协议", max_length=100, null=False)
    app_name = models.CharField("app名称", max_length=50, null=True,blank=True)
    applicant = models.CharField("审批人", max_length=50, null=False)
    create_time = models.DateField("创建时间",auto_now_add=True,null=True)
    expiry_date = models.CharField("过期时间", max_length=50, null=False)
    commit_by = models.CharField("提交人", max_length=100, null=False)
    action = models.CharField("执行的动作",max_length=50, null=False)
    comment = models.CharField("备注", max_length=1000, null=False)
    update_user = models.CharField("修改人", max_length=100, null=True)
    last_update_time = models.DateTimeField("最后一次更新时间",auto_now=True,null=True)

    def __str__(self):
        return "%s->%s:%s" %(self.s_ip,self.d_ip,self.d_port)

    class Meta:
        verbose_name = "防火墙规则表"
        db_table = "resources_firewall_rules"
        ordering = ["-id"]
        unique_together = ('s_ip', 'd_ip','d_port','protocol')