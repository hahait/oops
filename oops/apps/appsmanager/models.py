from django.db import models
from resources.models import ServerModel
from django.contrib.auth.models import Group

class AppConfigModel(models.Model):
    WAY_CHOICES = (
        ('0', "tomcat"),
        ('1', 'jar'),
        ('3', 'node'),
        ('4', 'php'),
        ('5', '其他'),
    )

    STATUS_CHOICES = (
        ('0', '运行中'),
        ('1', '待上线'),
        ('2', '已停服'),
    )

    ENV_CHOICES = (
        ("dev", "开发"),
        ("test", "测试"),
        ("online", "生产"),
        ("ops", "运维"),
        ("gray", "预发布"),
    )

    TYPE_CHOICES = (
        ("0", "核心应用"),
        ("1", "一般应用"),
        ("2", "中间件"),
        ("3", "其他"),
    )

    name = models.CharField("应用名", max_length=50, null=False, unique=True, help_text="应用名称")
    server = models.ManyToManyField(ServerModel, verbose_name="所属服务器",null=True, blank=True, help_text="应用所在的服务器")
    manage_team = models.ManyToManyField(Group, verbose_name="管理组",null=True, blank=True, help_text="负责该应用的开发组或运维组")
    env = models.CharField("环境", choices=ENV_CHOICES, max_length=10, null=False, default="online", help_text="应用所属环境")
    describe = models.CharField("描述", max_length=200, null=True, blank=True, help_text="应用功能性描述")
    path = models.CharField("部署路径", max_length=200, null=True, blank=True, help_text="应用部署路径")
    ansible_playbook = models.CharField("发布脚本", max_length=200, null=True, blank=True, help_text="应用发布脚本")
    start_script= models.CharField("启动脚本", max_length=200, null=True, blank=True,  help_text="应用启动脚本")
    log_path = models.CharField("日志路径", max_length=200, null=True, blank=True,  help_text="应用的日志路径")
    git = models.CharField("gitlab地址", max_length=200, null=True, blank=True,  help_text="应用的 gitlab 地址")
    ports = models.CharField("监听端口", max_length=200, null=True, blank=True,  help_text="应用监听端口")
    way = models.CharField("部署方式", max_length=10, choices=WAY_CHOICES, null=True, blank=True,  help_text="应用部署方式")
    type = models.CharField("类型", max_length=10, choices=TYPE_CHOICES, null=True, blank=True, help_text="应用类型")
    status = models.CharField("状态", choices=STATUS_CHOICES, max_length=10, null=True, blank=True,  help_text="应用状态")
    create_time = models.DateTimeField("添加时间", auto_now_add=True, null=True, blank=True,  help_text="添加时间")
    offline_time = models.DateTimeField("下线时间", null=True, blank=True, help_text="应用下线时间")
    last_update_time = models.DateTimeField("最后更新时间", auto_now=True, null=True, blank=True, help_text="应用最后更新时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "应用配置表"
        db_table = 'appsmanager_appconfig'
        ordering = ['-id']