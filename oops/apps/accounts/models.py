from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfileModel(AbstractUser):
    ROLE_CHOICES = (
        ("0","Head"),
        ("1","Controller"),
        ("2","Manager"),
        ("3","Employee"),
    )
    cn_name = models.CharField("中文名",max_length=50,null=False)
    role = models.CharField("角色",choices=ROLE_CHOICES,max_length=10,null=False,default="3")
    phone = models.CharField("手机号",max_length=11,null=False)
    last_update_time = models.DateTimeField("最后修改时间",auto_now=True)

    def __str__(self):
        return self.cn_name

    class Meta:
        verbose_name = "用户表"
        db_table = "user_profile"